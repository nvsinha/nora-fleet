
# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

from typing import Set

from queue import Empty
from threading import Event
from time import sleep

from janus import Queue
from janus import SyncQueueShutDown

from nora_fleet.internals.chat.async_collating_queue import AsyncCollatingQueue
from nora_fleet.service.watcher.interfaces.watcher_thread import WatcherThread
from nora_fleet.service.utils.server_context import ServerContext
from nora_fleet.session.session_invocation_context import SessionInvocationContext


class EventWorkMonitor(WatcherThread):
    """
    WatcherThread implementation that looks for work from event invocations
    that is finishing up so as to shut down their resources correctly.
    """

    def __init__(self, server_context: ServerContext):
        """
        Constructor

        :param server_context: ServerContext for global-ish state
        """
        super().__init__(server_context)
        self.update_period_in_seconds = 0.5
        self.event_work_queue: AsyncCollatingQueue = None
        self.invocation_context_pool: Set[SessionInvocationContext] = set()

    def start(self):
        """
        Perform start up.
        """
        self.event_work_queue = self.server_context.get_event_work_queue()
        super().start()

    def run(self):
        """
        Main loop
        """
        janus_queue: Queue = self.event_work_queue.get_queue()

        while self.keep_running:

            queued_item: SessionInvocationContext = None
            try:
                queued_item = janus_queue.sync_q.get_nowait()

            except Empty:
                if janus_queue.sync_q.closed:
                    self.logger.info("EventWorkMonitor shutting down")
                    return

            except SyncQueueShutDown:
                self.logger.info("SHUTDOWN signal for EventWorkMonitor queue")
                return

            if self.event_work_queue.is_final_item(queued_item):
                self.event_work_queue.close()
                self.logger.info("EventWorkMonitor shutting down from final item")
                return

            if queued_item is not None:
                self.invocation_context_pool.add(queued_item)

            self.process_pool()

            sleep(self.update_period_in_seconds)

    def process_pool(self):
        """
        Process the pool of SessionInvocationContexts we need to monitor
        """
        done_invocations: Set[SessionInvocationContext] = set()

        # See which ones are done
        for invocation_context in self.invocation_context_pool:
            done_event: Event = invocation_context.get_work_done_event()
            if done_event.is_set():
                done_invocations.add(invocation_context)

        # Process the done ones
        for invocation_context in done_invocations:

            # Clean up the resources of the invocation_context
            invocation_context.done_with_work("EventWorkMonitor")

            # No need to check on this guy any more
            self.invocation_context_pool.remove(invocation_context)

# Copyright (c) 2026 Nishant Sinha
#
# Licensed under the MIT License. See LICENSE.txt in the project
# root for full license information.
#
# END COPYRIGHT

"""Resource monitoring — psutil-based process snapshots.

Interim implementation. May be replaced by nora-fleet built-in
monitoring and telemetry when those features become available.
"""

import logging
from typing import Optional

import psutil

from tests.load_tests.config import ResourceSnapshot

logger = logging.getLogger(__name__)


class ResourceMonitor:
    """Captures and logs psutil-based process resource snapshots."""

    @staticmethod
    def find_process(keyword) -> Optional[psutil.Process]:
        """Find a running process whose command line contains the given keyword."""
        for proc in psutil.process_iter(["pid", "cmdline"]):
            try:
                cmdline = " ".join(proc.info.get("cmdline") or [])
                if keyword in cmdline:
                    return psutil.Process(proc.info.get("pid"))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return None

    @staticmethod
    def find_process_by_port(port) -> Optional[psutil.Process]:
        """Find a process listening on the given port."""
        for proc in psutil.process_iter(["pid"]):
            try:
                for conn in proc.net_connections():
                    if conn.status == "LISTEN" and conn.laddr.port == port:
                        return psutil.Process(proc.info.get("pid"))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return None

    @staticmethod
    def snapshot(proc) -> Optional[ResourceSnapshot]:
        """Capture a point-in-time resource snapshot of a process."""
        if proc is None:
            return None
        try:
            mem = proc.memory_info()
            try:
                fds = proc.num_fds()
            except AttributeError:
                fds = proc.num_handles()
            cpu_times = proc.cpu_times()
            return {
                "rss": mem.rss / 1024 / 1024,
                "fds": fds,
                "threads": proc.num_threads(),
                "connections": len(proc.net_connections()),
                "children": len(proc.children()),
                "cpu": proc.cpu_percent(interval=0.1),
                "cpu_seconds": cpu_times.user + cpu_times.system,
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return None

    @staticmethod
    def log_snapshot(label, snap) -> None:
        """Log a single resource snapshot."""
        if snap is None:
            logger.info("  %s: process not found", label)
            return
        logger.info(
            "  %s: RSS=%.1f MB, FDs=%s, Threads=%s, Conns=%s, CPU=%.1f%%, Children=%s",
            label, snap.get("rss"), snap.get("fds"), snap.get("threads"),
            snap.get("connections"), snap.get("cpu"), snap.get("children"),
        )

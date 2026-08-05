#!/usr/bin/env python3
"""
System Status Dashboard

Run this to check real-time system health and metrics.
Shows uptime, announcements processed, signals generated, last activity times.
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path
import psutil

from utils.logger import setup_logger
from database.announcement_repository import AnnouncementRepository
from database.insider_signal_repository import InsiderSignalRepository
from state.state_manager import StateManager


def get_uptime():
    """Get actual process uptime from process_started.txt"""
    try:
        start_file = Path("state/process_started.txt")
        
        if not start_file.exists():
            return "Unknown (not running)"
        
        start_time_str = start_file.read_text().strip()
        start_time = datetime.fromisoformat(start_time_str)
        uptime = datetime.now() - start_time
        
        days = uptime.days
        hours = int((uptime.total_seconds() % 86400) / 3600)
        minutes = int((uptime.total_seconds() % 3600) / 60)
        
        if days > 0:
            return f"{days}d {hours}h"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
    except Exception as e:
        return f"Error: {e}"


def get_announcements_count():
    """Get total announcements processed"""
    try:
        repo = AnnouncementRepository()
        count = repo.count()
        repo.close()
        return count
    except Exception as e:
        return f"Error: {e}"


def get_signals_count():
    """Get total insider signals generated"""
    try:
        repo = InsiderSignalRepository()
        signals = repo.get_all()
        count = len(signals) if signals else 0
        repo.close()
        return count
    except Exception as e:
        return f"Error: {e}"


def get_last_poll_time():
    """Get time of last announcement poll"""
    try:
        state = StateManager()
        # Check the state file modification time
        state_file = Path("state/last_processed.txt")
        
        if not state_file.exists():
            return "Never", None
        
        mtime = state_file.stat().st_mtime
        last_poll = datetime.fromtimestamp(mtime)
        time_ago = datetime.now() - last_poll
        
        if time_ago.total_seconds() < 60:
            return f"{int(time_ago.total_seconds())}s ago", time_ago
        elif time_ago.total_seconds() < 3600:
            return f"{int(time_ago.total_seconds() / 60)}m ago", time_ago
        else:
            hours = time_ago.total_seconds() / 3600
            return f"{int(hours)}h ago", time_ago
    except Exception as e:
        return f"Error: {e}", None


def get_last_telegram_time():
    """Get time of last successful Telegram notification"""
    try:
        log_file = Path("logs/sgx_pipeline.log")
        if not log_file.exists():
            return "Never", None
        
        # Search backwards for last Telegram notification
        with open(log_file, "r") as f:
            lines = f.readlines()
        
        for line in reversed(lines):
            if "Telegram sent successfully" in line or "Notification sent successfully" in line:
                try:
                    timestamp_str = line.split(" | ")[0]
                    last_notify = datetime.fromisoformat(timestamp_str)
                    time_ago = datetime.now() - last_notify
                    
                    if time_ago.total_seconds() < 60:
                        return f"{int(time_ago.total_seconds())}s ago", time_ago
                    elif time_ago.total_seconds() < 3600:
                        return f"{int(time_ago.total_seconds() / 60)}m ago", time_ago
                    else:
                        hours = time_ago.total_seconds() / 3600
                        return f"{int(hours)}h ago", time_ago
                except:
                    pass
        
        return "Never", None
    except Exception as e:
        return f"Error: {e}", None


def get_database_health():
    """Check database health"""
    try:
        repo = AnnouncementRepository()
        repo.close()
        return "Healthy"
    except Exception as e:
        return f"Unhealthy: {e}"


def get_last_error():
    """Get last error from log file"""
    try:
        log_file = Path("logs/sgx_pipeline.log")
        if not log_file.exists():
            return "None"
        
        # Search backwards for last error
        with open(log_file, "r") as f:
            lines = f.readlines()
        
        for line in reversed(lines):
            if " ERROR " in line or " CRITICAL " in line:
                # Extract just the error message
                parts = line.split(" | ")
                if len(parts) >= 4:
                    return parts[-1].strip()[:80]  # Truncate to 80 chars
        
        return "None"
    except Exception as e:
        return f"Error reading logs: {e}"


def format_metric(label, value, color=None):
    """Format a metric for display"""
    print(f"{label:.<25} {value}")


def main():
    """Display system status"""
    setup_logger()
    
    print("\n" + "="*50)
    print("SYSTEM STATUS DASHBOARD")
    print("="*50 + "\n")
    
    # Uptime
    uptime_str = get_uptime()
    format_metric("Running", uptime_str)
    
    # Counts
    announcements = get_announcements_count()
    format_metric("Announcements", announcements)
    
    signals = get_signals_count()
    format_metric("Signals", signals)
    
    # Activity
    last_poll, _ = get_last_poll_time()
    format_metric("Last Poll", last_poll)
    
    last_notify, _ = get_last_telegram_time()
    format_metric("Last Telegram", last_notify)
    
    # Health
    db_health = get_database_health()
    format_metric("Database", db_health)
    
    last_error = get_last_error()
    format_metric("Last Error", last_error)
    
    print("\n" + "="*50 + "\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

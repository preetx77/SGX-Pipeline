#!/usr/bin/env python3
"""
Operational Heartbeat

Sends a Telegram heartbeat with real metrics.
Run periodically (e.g., every 6 hours) to monitor system health.
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path
import psutil

from utils.logger import setup_logger
from database.announcement_repository import AnnouncementRepository
from database.insider_signal_repository import InsiderSignalRepository
from notifications.telegram_notifier import TelegramNotifier
from config.watchlist import WATCHLIST


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
        
        if days > 0:
            return f"{days}d {hours}h"
        else:
            return f"{hours}h"
    except:
        return "Unknown"


def get_announcements():
    """Get announcement count"""
    try:
        repo = AnnouncementRepository()
        count = repo.count()
        repo.close()
        return count
    except:
        return 0


def get_signals():
    """Get signal count"""
    try:
        repo = InsiderSignalRepository()
        signals = repo.get_all()
        count = len(signals) if signals else 0
        repo.close()
        return count
    except:
        return 0


def get_last_signal_time():
    """Get time of last signal"""
    try:
        repo = InsiderSignalRepository()
        signals = repo.get_all()
        repo.close()
        
        if not signals:
            return "Never"
        
        # Get most recent signal timestamp (assuming it's first in list)
        try:
            last_signal = signals[0]
            # Signals should have created_at timestamp
            if hasattr(last_signal, 'created_at'):
                last_time = datetime.fromisoformat(last_signal[8])  # created_at column
                time_ago = datetime.now() - last_time
                
                if time_ago.total_seconds() < 3600:
                    return f"{int(time_ago.total_seconds() / 60)}m ago"
                else:
                    hours = int(time_ago.total_seconds() / 3600)
                    return f"{hours}h ago"
        except:
            pass
        
        return "Recently"
    except:
        return "Unknown"


def get_memory_usage():
    """Get process memory usage"""
    try:
        process = psutil.Process()
        memory_mb = process.memory_info().rss / (1024 * 1024)
        return f"{int(memory_mb)} MB"
    except:
        return "Unknown"


def get_cpu_usage():
    """Get CPU usage percentage"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        return f"{int(cpu_percent)}%"
    except:
        return "Unknown"


def get_health_status():
    """Determine overall health status"""
    try:
        repo = AnnouncementRepository()
        count = repo.count()
        repo.close()
        
        if count > 0:
            return "Healthy"
        else:
            return "Idle"
    except:
        return "Unhealthy"


def build_heartbeat_message():
    """Build the heartbeat message"""
    uptime = get_uptime()
    companies = len(WATCHLIST)
    announcements = get_announcements()
    signals = get_signals()
    last_signal = get_last_signal_time()
    memory = get_memory_usage()
    cpu = get_cpu_usage()
    status = get_health_status()
    
    message = (
        "[HEARTBEAT] SGX PIPELINE\n\n"
        f"Uptime: {uptime}\n"
        f"Companies: {companies}\n"
        f"Announcements: {announcements}\n"
        f"Signals: {signals}\n"
        f"Last Signal: {last_signal}\n"
        f"Memory: {memory}\n"
        f"CPU: {cpu}\n"
        f"Status: {status}\n\n"
        f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    
    return message


def main():
    """Send heartbeat"""
    setup_logger()
    
    print("Sending operational heartbeat...\n")
    
    try:
        message = build_heartbeat_message()
        print(message)
        print("\n")
        
        notifier = TelegramNotifier()
        result = notifier.loop.run_until_complete(notifier._send(message))
        notifier.close()
        
        if result:
            print("Heartbeat sent successfully")
            return 0
        else:
            print("Heartbeat send failed")
            return 1
    except Exception as e:
        print(f"Failed to send heartbeat: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

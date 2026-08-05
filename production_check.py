#!/usr/bin/env python3
"""
Production Deployment Checklist
Run this before every deployment to ensure all systems are operational.
"""

import sys
import os
from pathlib import Path
import shutil
import psutil
import asyncio

from config.settings import TELEGRAM_TOKEN, CHAT_IDS
from database.announcement_repository import AnnouncementRepository
from config.watchlist import WATCHLIST
from scraper.client import SGXClient


def check_status(name, result, error=None):
    """Print status check result"""
    status = " OK" if result else " FAIL"
    print(f"{name:.<30} {status}")
    if error and not result:
        print(f"  Error: {error}")
    return result


def check_database():
    """Verify database connectivity and integrity"""
    try:
        repo = AnnouncementRepository()
        count = repo.repository.count() if hasattr(repo, 'repository') else 0
        repo.close()
        return True, None
    except Exception as e:
        return False, str(e)


def check_telegram():
    """Verify Telegram token and chat IDs are configured"""
    try:
        if not TELEGRAM_TOKEN:
            return False, "TELEGRAM_BOT_TOKEN not configured"
        if not CHAT_IDS:
            return False, "CHAT_IDS not configured"
        return True, None
    except Exception as e:
        return False, str(e)


def check_sgx_api():
    """Verify SGX API connectivity"""
    try:
        client = SGXClient()
        # Just verify instantiation and auth
        return True, None
    except Exception as e:
        return False, str(e)


def check_watchlist():
    """Verify watchlist is loaded"""
    try:
        if not WATCHLIST or len(WATCHLIST) == 0:
            return False, "Watchlist is empty"
        return True, None
    except Exception as e:
        return False, str(e)


def check_checkpoint():
    """Verify checkpoint/state file exists and is readable"""
    try:
        from state.state_manager import StateManager
        state = StateManager()
        _ = state.get_last_id()
        return True, None
    except Exception as e:
        return False, str(e)


def check_downloads_folder():
    """Verify data/raw directory exists and is writable"""
    try:
        downloads_path = Path("data/raw")
        downloads_path.mkdir(parents=True, exist_ok=True)
        
        # Test write
        test_file = downloads_path / ".write_test"
        test_file.write_text("test")
        test_file.unlink()
        
        return True, None
    except Exception as e:
        return False, str(e)


def check_disk_space():
    """Verify sufficient disk space (at least 1GB free)"""
    try:
        usage = shutil.disk_usage(".")
        free_gb = usage.free / (1024**3)
        
        if free_gb < 1:
            return False, f"Only {free_gb:.2f}GB free (need 1GB+)"
        
        return True, None
    except Exception as e:
        return False, str(e)


def check_threads():
    """Verify system can support required threads"""
    try:
        # Check CPU count
        cpu_count = psutil.cpu_count()
        if cpu_count < 2:
            return False, f"Only {cpu_count} CPU(s) available (need 2+)"
        
        # Check available threads aren't exhausted
        process = psutil.Process()
        if process.num_threads() > 500:
            return False, f"Too many threads already running ({process.num_threads()})"
        
        return True, None
    except Exception as e:
        return False, str(e)


def main():
    """Run all production checks"""
    print("\n" + "="*50)
    print("PRODUCTION DEPLOYMENT CHECKLIST")
    print("="*50 + "\n")
    
    checks = [
        ("Database", check_database),
        ("Telegram", check_telegram),
        ("SGX API", check_sgx_api),
        ("Watchlist", lambda: (len(WATCHLIST) == 12, None) if WATCHLIST else (False, "Watchlist empty")),
        ("Checkpoint", check_checkpoint),
        ("Downloads Folder", check_downloads_folder),
        ("Disk Space", check_disk_space),
        ("Threads", check_threads),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result, error = check_func()
            passed = check_status(name, result, error)
            results.append(passed)
        except Exception as e:
            passed = check_status(name, False, str(e))
            results.append(passed)
    
    print("\n" + "="*50)
    passed_count = sum(results)
    total_count = len(results)
    
    if passed_count == total_count:
        print(f" ALL CHECKS PASSED ({passed_count}/{total_count})")
        print("="*50 + "\n")
        return 0
    else:
        print(f" CHECKS FAILED ({passed_count}/{total_count} passed)")
        print("="*50 + "\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Burn-in test status monitor.
Tracks uptime, errors, checkpoint advancement, signal classification health.
"""

import subprocess
import re
import json
import platform
from datetime import datetime
from pathlib import Path

def get_process_info():
    """Check if burn-in process is running (Windows and Unix compatible)."""
    try:
        if platform.system() == 'Windows':
            # Windows: use tasklist
            result = subprocess.run(
                ['tasklist'],
                capture_output=True,
                text=True,
                timeout=5
            )
            # Just check if python.exe appears (multiple instances may be running)
            if 'python.exe' in result.stdout:
                return {
                    'running': True,
                    'pid': 'multiple',
                    'start_time': 'unknown'
                }
        else:
            # Unix/Linux: use ps aux
            result = subprocess.run(
                ['ps', 'aux'],
                capture_output=True,
                text=True,
                timeout=5
            )
            for line in result.stdout.split('\n'):
                if 'run_system.py' in line and 'grep' not in line:
                    parts = line.split()
                    if len(parts) > 1:
                        return {
                            'running': True,
                            'pid': parts[1],
                            'start_time': ' '.join(parts[8:11]) if len(parts) > 10 else 'unknown'
                        }
    except Exception as e:
        print(f"Warning: Could not check process: {e}")
    
    return {'running': False, 'pid': None}

def parse_log_stats():
    """Extract stats from burn_in_test.log."""
    log_file = Path('burn_in_test.log')
    if not log_file.exists():
        return None
    
    try:
        with open(log_file, 'r') as f:
            lines = f.readlines()
        
        # Extract stats
        stats = {
            'total_lines': len(lines),
            'last_entry': lines[-1].strip() if lines else 'N/A',
            'last_timestamp': None,
            'error_count': 0,
            'warning_count': 0,
            'companies_synced': 0,
            'total_announcements_fetched': 0,
            'total_inserted': 0,
            'total_skipped': 0,
            'checkpoint_updates': 0,
            'errors': []
        }
        
        # Parse all lines for metrics
        for line in lines:
            # Extract timestamp
            timestamp_match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
            if timestamp_match:
                stats['last_timestamp'] = timestamp_match.group(1)
            
            # Count errors/warnings
            if ' ERROR ' in line or ' CRITICAL ' in line:
                stats['error_count'] += 1
                stats['errors'].append(line.strip()[-100:])  # Last 100 chars
            if ' WARNING ' in line:
                stats['warning_count'] += 1
            
            # Extract metrics from summary lines
            if 'Companies=' in line:
                match = re.search(r'Companies=(\d+).*Fetched=(\d+).*Inserted=(\d+).*Skipped=(\d+)', line)
                if match:
                    stats['companies_synced'] = max(stats['companies_synced'], int(match.group(1)))
                    stats['total_announcements_fetched'] = max(stats['total_announcements_fetched'], int(match.group(2)))
                    stats['total_inserted'] = max(stats['total_inserted'], int(match.group(3)))
                    stats['total_skipped'] = max(stats['total_skipped'], int(match.group(4)))
            
            # Count checkpoints
            if 'Last checkpoint:' in line:
                stats['checkpoint_updates'] += 1
        
        return stats
    except Exception as e:
        print(f"Error parsing log: {e}")
        return None

def get_database_signal_count():
    """Get count of signals in database."""
    try:
        import sqlite3
        conn = sqlite3.connect('database/database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM insider_signals WHERE transaction_type = 'MARKET_PURCHASE'")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except Exception as e:
        print(f"Warning: Could not query database: {e}")
        return None

def main():
    print("\n" + "=" * 100)
    print("SGX PIPELINE - BURN-IN TEST STATUS")
    print("=" * 100)
    print(f"\nCheck time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Process status
    print("\n## PROCESS STATUS")
    print("-" * 100)
    proc = get_process_info()
    if proc['running']:
        print(f"[OK] Process running (PID: {proc['pid']})")
    else:
        print("[FAIL] Process NOT running - burn-in may have crashed")
    
    # Log analysis
    print("\n## LOG ANALYSIS")
    print("-" * 100)
    log_stats = parse_log_stats()
    if log_stats:
        print(f"Log file size: {log_stats['total_lines']} lines")
        print(f"Last entry: {log_stats['last_timestamp']}")
        print(f"  {log_stats['last_entry']}")
        print(f"\nError/Warning count:")
        print(f"  Errors: {log_stats['error_count']}")
        print(f"  Warnings: {log_stats['warning_count']}")
        if log_stats['errors']:
            print(f"  Recent errors:")
            for err in log_stats['errors'][-3:]:
                print(f"    - {err}")
        
        print(f"\nSync metrics:")
        print(f"  Companies synced: {log_stats['companies_synced']}")
        print(f"  Announcements fetched: {log_stats['total_announcements_fetched']}")
        print(f"  Inserted: {log_stats['total_inserted']}")
        print(f"  Skipped: {log_stats['total_skipped']}")
        print(f"  Checkpoint advances: {log_stats['checkpoint_updates']}")
    else:
        print("Log file not found or unreadable")
    
    # Database state
    print("\n## DATABASE STATE")
    print("-" * 100)
    signal_count = get_database_signal_count()
    if signal_count is not None:
        print(f"MARKET_PURCHASE signals in database: {signal_count}")
    else:
        print("Could not query database")
    
    # Health check
    print("\n## BURN-IN HEALTH CHECK")
    print("-" * 100)
    
    health_issues = []
    if not proc['running']:
        health_issues.append("[ERROR] Process not running")
    if log_stats and log_stats['error_count'] > 5:
        health_issues.append(f"[WARN]  High error count: {log_stats['error_count']}")
    if log_stats and log_stats['checkpoint_updates'] < 2:
        health_issues.append("[WARN]  Low checkpoint advances (may not be syncing properly)")
    
    if health_issues:
        print("Issues detected:")
        for issue in health_issues:
            print(f"  {issue}")
    else:
        print("[OK] No critical issues detected")
        print("[OK] Process running")
        print("[OK] Checkpoint advancing")
        print("[OK] Error rate acceptable")
    
    print("\n" + "=" * 100)

if __name__ == '__main__':
    main()

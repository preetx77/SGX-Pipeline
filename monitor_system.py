import os
import sys
import logging
from pathlib import Path
from datetime import datetime, timedelta
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class SystemMonitor:
    def __init__(self):
        self.log_file = Path("logs/sgx_pipeline.log")
        self.process_started_file = Path("state/process_started.txt")
        self.db_file = Path("data/database.db")
        
    def get_process_status(self):
        if not self.process_started_file.exists():
            return "OFFLINE", None
        try:
            start_time_str = self.process_started_file.read_text().strip()
            start_time = datetime.fromisoformat(start_time_str)
            return "ONLINE", start_time
        except Exception as e:
            logging.error(f"Error reading process: {e}")
            return "UNKNOWN", None
    
    def get_last_activity(self):
        if not self.log_file.exists():
            return None
        try:
            with open(self.log_file, 'r', errors='ignore') as f:
                lines = f.readlines()
            if not lines:
                return None
            for line in reversed(lines):
                try:
                    parts = line.split(' | ')
                    if len(parts) >= 2:
                        timestamp_str = parts[0].strip()
                        last_activity = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                        return last_activity
                except:
                    continue
            return None
        except Exception as e:
            logging.error(f"Error: {e}")
            return None
    
    def get_database_size(self):
        if not self.db_file.exists():
            return 0
        try:
            size_bytes = self.db_file.stat().st_size
            return size_bytes / (1024 * 1024)
        except:
            return 0
    
    def get_log_statistics(self):
        stats = {
            "total_log_lines": 0,
            "requests_count": 0,
            "companies_synced": 0,
            "errors": 0,
            "dns_failures": 0,
            "connection_drops": 0,
            "rate_limits": 0,
            "db_errors": 0,
            "validation_passed": False,
            "announcements_inserted": 0,
            "announcements_skipped": 0,
        }
        
        if not self.log_file.exists():
            return stats
        
        try:
            with open(self.log_file, 'r', errors='ignore') as f:
                lines = f.readlines()
            
            stats["total_log_lines"] = len(lines)
            
            for line in lines:
                if "REQUEST:" in line:
                    stats["requests_count"] += 1
                if "Completed" in line and "Inserted=" in line:
                    stats["companies_synced"] += 1
                    try:
                        if "Inserted=" in line:
                            inserted = int(line.split("Inserted=")[1].split(",")[0])
                            stats["announcements_inserted"] += inserted
                        if "Skipped=" in line:
                            skipped = int(line.split("Skipped=")[1].split(",")[0])
                            stats["announcements_skipped"] += skipped
                    except:
                        pass
                if "ERROR" in line or "FAILED" in line:
                    stats["errors"] += 1
                if "getaddrinfo failed" in line:
                    stats["dns_failures"] += 1
                if "Resetting dropped connection" in line:
                    stats["connection_drops"] += 1
                if "429" in line and "HTTP" in line:
                    stats["rate_limits"] += 1
                if "database" in line.lower() and "error" in line.lower():
                    stats["db_errors"] += 1
                if "Watchlist validation PASSED" in line:
                    stats["validation_passed"] = True
        except Exception as e:
            logging.error(f"Error: {e}")
        
        return stats
    
    def get_uptime(self, start_time):
        if not start_time:
            return None
        uptime = datetime.now() - start_time
        hours = uptime.total_seconds() / 3600
        minutes = (uptime.total_seconds() % 3600) / 60
        return hours, minutes
    
    def test_telegram(self):
        try:
            from notifications.telegram_notifier import TelegramNotifier
            notifier = TelegramNotifier()
            message = "[!] TEST"
            result = notifier.loop.run_until_complete(notifier._send(message))
            return "WORKING" if result else "FAILED"
        except Exception as e:
            return f"ERROR"
    
    def display_status(self, status, start_time, last_activity, stats):
        print("\nSYSTEM STATUS")
        print("-" * 90)
        
        status_symbol = "[ON]" if status == "ONLINE" else "[OFF]"
        print(f"  Status: {status_symbol} {status}")
        
        if start_time:
            print(f"  Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            uptime = self.get_uptime(start_time)
            if uptime:
                hours, minutes = uptime
                print(f"  Uptime: {int(hours)}h {int(minutes)}m")
        
        if last_activity:
            time_since = datetime.now() - last_activity
            minutes_since = time_since.total_seconds() / 60
            print(f"  Last Activity: {last_activity.strftime('%Y-%m-%d %H:%M:%S')} ({int(minutes_since)}m ago)")
        
        db_size = self.get_database_size()
        print(f"  Database Size: {db_size:.2f} MB")
        
        print("\nVALIDATION & WATCHLIST")
        print("-" * 90)
        validation = "[OK]" if stats.get('validation_passed') else "[PENDING]"
        print(f"  Watchlist: {validation} - Companies Synced: {stats.get('companies_synced', 0)}")
        
        print("\nACTIVITY METRICS")
        print("-" * 90)
        print(f"  Total Requests: {stats.get('requests_count', 0)}")
        print(f"  Announcements: {stats.get('announcements_inserted', 0)} new, {stats.get('announcements_skipped', 0)} cached")
        print(f"  Total Errors: {stats.get('errors', 0)}")
        
        print("\nERROR BREAKDOWN")
        print("-" * 90)
        print(f"  DNS: {stats.get('dns_failures', 0)} | Drops: {stats.get('connection_drops', 0)} | 429s: {stats.get('rate_limits', 0)} | DB: {stats.get('db_errors', 0)}")
        
        print("\nNETWORK")
        print("-" * 90)
        telegram_status = self.test_telegram()
        print(f"  Telegram: {telegram_status}")
    
    def send_telegram_alert(self, status, start_time, stats):
        try:
            from notifications.telegram_notifier import TelegramNotifier
            notifier = TelegramNotifier()
            
            uptime_str = "Not started"
            if start_time:
                uptime = self.get_uptime(start_time)
                if uptime:
                    hours, minutes = uptime
                    uptime_str = f"{int(hours)}h {int(minutes)}m"
            
            message = f"""SGX Pipeline Status Report
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Status: {status}
Started: {start_time.strftime('%Y-%m-%d %H:%M:%S') if start_time else 'N/A'}
Uptime: {uptime_str}
Companies Synced: {stats.get('companies_synced', 0)}
Requests: {stats.get('requests_count', 0)}
Errors: {stats.get('errors', 0)}
Database: {self.get_database_size():.2f} MB"""
            
            result = notifier.loop.run_until_complete(notifier._send(message))
            return result
        except Exception as e:
            logging.error(f"Alert failed: {e}")
            return False
    
    def run(self, send_telegram=True):
        print("\n" + "="*90)
        print(f"SGX PIPELINE MONITOR - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*90)
        
        status, start_time = self.get_process_status()
        last_activity = self.get_last_activity()
        stats = self.get_log_statistics()
        
        self.display_status(status, start_time, last_activity, stats)
        
        if send_telegram:
            print("\nSENDING TELEGRAM ALERT...")
            success = self.send_telegram_alert(status, start_time, stats)
            print(f"Result: {'OK' if success else 'FAILED'}")
        
        print("\n" + "="*90 + "\n")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-telegram', action='store_true')
    args = parser.parse_args()
    
    monitor = SystemMonitor()
    monitor.run(send_telegram=not args.no_telegram)

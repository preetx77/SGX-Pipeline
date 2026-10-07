
import os, sys, logging, socket, time, json
from pathlib import Path
from datetime import datetime, timedelta

try:
    import psutil
except ImportError:
    psutil = None

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)-8s | %(message)s')

class AdvancedMonitor:
    def __init__(self):
        self.log_file = Path("logs/sgx_pipeline.log")
        self.process_started_file = Path("state/process_started.txt")
        self.db_file = Path("data/database.db")
        
    def get_system_performance(self):
        if not psutil:
            return {"cpu": "N/A", "ram": "N/A", "available": False}
        try:
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory().percent
            return {"cpu": f"{cpu}%", "ram": f"{ram}%", "available": True, "cpu_num": cpu, "ram_num": ram}
        except:
            return {"cpu": "N/A", "ram": "N/A", "available": False}
    
    def test_network_speed(self):
        try:
            start = time.time()
            socket.create_connection(("api.sgx.com", 443), timeout=3)
            elapsed = (time.time() - start) * 1000
            return f"{elapsed:.0f}ms", "OK"
        except socket.timeout:
            return "Timeout", "SLOW"
        except:
            return "Unreachable", "OFFLINE"
    
    def get_company_coverage(self):
        try:
            from config.watchlist_500 import WATCHLIST
            total = len(WATCHLIST)
            queried = 0
            
            if self.log_file.exists():
                logs = self.log_file.read_text(errors='ignore')
                for company in WATCHLIST:
                    if f"REQUEST: {company.code}" in logs or f"Syncing {company.code}" in logs:
                        queried += 1
            
            pct = (queried / total * 100) if total > 0 else 0
            return {"total": total, "queried": queried, "never_queried": total-queried, "coverage": f"{pct:.1f}%"}
        except:
            return {"total": 500, "queried": 0, "never_queried": 500, "coverage": "0%"}
    
    def calculate_health_score(self, stats, perf):
        score = 100.0
        score -= min(stats.get('errors', 0) * 2, 20)
        score -= min((stats.get('connection_drops', 0) + stats.get('dns_failures', 0)) * 1.5, 15)
        score -= min(stats.get('rate_limits', 0) * 0.5, 10)
        if stats.get('requests_count', 0) > 10000:
            score += 5
        if perf.get('available'):
            if perf.get('cpu_num', 0) > 80:
                score -= 5
            if perf.get('ram_num', 0) > 80:
                score -= 5
        return max(0, min(100, score))
    
    def get_uptime(self, start_time):
        if not start_time:
            return None
        uptime = datetime.now() - start_time
        return uptime.total_seconds() / 3600, (uptime.total_seconds() % 3600) / 60
    
    def get_process_status(self):
        if not self.process_started_file.exists():
            return "OFFLINE", None
        try:
            start_time = datetime.fromisoformat(self.process_started_file.read_text().strip())
            return "ONLINE", start_time
        except:
            return "UNKNOWN", None
    
    def get_last_activity(self):
        if not self.log_file.exists():
            return None
        try:
            with open(self.log_file, 'r', errors='ignore') as f:
                for line in reversed(f.readlines()):
                    try:
                        ts = line.split(' | ')[0].strip()
                        return datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
                    except:
                        continue
        except:
            pass
        return None
    
    def get_log_statistics(self):
        stats = {"total_log_lines": 0, "requests_count": 0, "companies_synced": 0, "errors": 0,
                 "dns_failures": 0, "connection_drops": 0, "rate_limits": 0, "db_errors": 0,
                 "validation_passed": False, "announcements_inserted": 0, "announcements_skipped": 0}
        
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
                        inserted = int(line.split("Inserted=")[1].split(",")[0])
                        stats["announcements_inserted"] += inserted
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
        except:
            pass
        
        return stats
    
    def test_telegram(self):
        try:
            from notifications.telegram_notifier import TelegramNotifier
            notifier = TelegramNotifier()
            result = notifier.loop.run_until_complete(notifier._send("[!] TEST"))
            return "WORKING" if result else "FAILED"
        except:
            return "ERROR"
    
    def display_full_report(self):
        print("\n" + "="*90)
        print(f"SGX PIPELINE - ADVANCED MONITOR | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*90)
        
        status, start_time = self.get_process_status()
        last_activity = self.get_last_activity()
        stats = self.get_log_statistics()
        perf = self.get_system_performance()
        coverage = self.get_company_coverage()
        health = self.calculate_health_score(stats, perf)
        
        print("\n[1] SYSTEM STATUS")
        print("-" * 90)
        print(f"  Status: [{status[0:2]}] {status}")
        if start_time:
            print(f"  Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            uptime = self.get_uptime(start_time)
            if uptime:
                print(f"  Uptime: {int(uptime[0])}h {int(uptime[1])}m")
        if last_activity:
            mins_since = (datetime.now() - last_activity).total_seconds() / 60
            print(f"  Last Activity: {int(mins_since)}m ago")
        print(f"  Database Size: {self.db_file.stat().st_size / (1024*1024) if self.db_file.exists() else 0:.2f} MB")
        
        print("\n[2] PERFORMANCE METRICS")
        print("-" * 90)
        print(f"  CPU Usage: {perf['cpu']}")
        print(f"  RAM Usage: {perf['ram']}")
        speed, status_code = self.test_network_speed()
        print(f"  Network Speed (SGX): {speed} ({status_code})")
        
        print("\n[3] COMPANY COVERAGE TRACKING")
        print("-" * 90)
        print(f"  Total Companies: {coverage['total']}")
        print(f"  Queried: {coverage['queried']}")
        print(f"  Never Queried: {coverage['never_queried']}")
        print(f"  Coverage: {coverage['coverage']}")
        
        print("\n[4] ACTIVITY METRICS")
        print("-" * 90)
        print(f"  Total Requests: {stats.get('requests_count', 0)}")
        print(f"  Companies Synced: {stats.get('companies_synced', 0)}")
        print(f"  Announcements New: {stats.get('announcements_inserted', 0)}")
        print(f"  Announcements Cached: {stats.get('announcements_skipped', 0)}")
        print(f"  Total Errors: {stats.get('errors', 0)}")
        
        print("\n[5] ERROR BREAKDOWN")
        print("-" * 90)
        print(f"  DNS: {stats.get('dns_failures', 0)} | Drops: {stats.get('connection_drops', 0)} | 429s: {stats.get('rate_limits', 0)} | DB: {stats.get('db_errors', 0)}")
        
        print("\n[6] NETWORK & TELEGRAM")
        print("-" * 90)
        tg = self.test_telegram()
        print(f"  Telegram: {tg}")
        
        print("\n[7] HEALTH SCORE")
        print("-" * 90)
        health_bar = int(health / 5)
        bar = "[" + "#" * health_bar + "-" * (20 - health_bar) + "]"
        h_status = "EXCELLENT" if health >= 90 else "GOOD" if health >= 70 else "OK" if health >= 50 else "POOR"
        print(f"  Score: {bar} {health:.0f}/100 ({h_status})")
        
        print("\n" + "="*90 + "\n")
    
    def run(self, send_tg=True):
        stats = self.get_log_statistics()
        perf = self.get_system_performance()
        coverage = self.get_company_coverage()
        
        self.display_full_report()
        
        if send_tg:
            try:
                from notifications.telegram_notifier import TelegramNotifier
                health = self.calculate_health_score(stats, perf)
                status, start_time = self.get_process_status()
                uptime_str = f"{int(self.get_uptime(start_time)[0])}h" if start_time else "N/A"
                
                msg = f"""Advanced Report
Status: {status} | Uptime: {uptime_str}
Coverage: {coverage['coverage']}
Requests: {stats['requests_count']}
Errors: DNS={stats['dns_failures']} Drops={stats['connection_drops']} 429s={stats['rate_limits']}
Health: {health:.0f}/100
CPU: {perf['cpu']} | RAM: {perf['ram']}"""
                
                notifier = TelegramNotifier()
                notifier.loop.run_until_complete(notifier._send(msg))
                print("Telegram: OK")
            except Exception as e:
                print(f"Telegram: FAILED ({str(e)[:30]})")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-telegram', action='store_true')
    args = parser.parse_args()
    
    monitor = AdvancedMonitor()
    monitor.run(send_tg=not args.no_telegram)

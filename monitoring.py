"""
Advanced monitoring system for SGX Pipeline.
Tracks process health, performance metrics, and anomalies in real-time.

Uses logs/sgx_pipeline.log (main runtime log) by default.
For burn-in tests, pass log_file="burn_in_test.log"
"""

import sqlite3
import re
from datetime import datetime, timedelta
from pathlib import Path


class PipelineMonitor:
    """Monitor pipeline health and performance metrics."""
    
    def __init__(self, log_file="logs/sgx_pipeline.log", db_file="database/database.db"):
        self.log_file = Path(log_file)
        self.db_file = db_file
    
    def get_log_stats(self):
        """Extract metrics from log file."""
        if not self.log_file.exists():
            return None
        
        stats = {
            'total_lines': 0,
            'last_timestamp': None,
            'is_active': False,
            'announcements_checked': 0,
            'companies_synced': 0,
            'inserted': 0,
            'skipped': 0,
            'error_count': 0,
            'warning_count': 0,
            'timeouts': 0,
            'dns_failures': 0,
            'rate_limits': 0,
        }
        
        try:
            with open(self.log_file, 'r') as f:
                lines = f.readlines()
            
            stats['total_lines'] = len(lines)
            
            # Only check last hour of logs to avoid historic data
            one_hour_ago = datetime.now() - timedelta(hours=1)
            
            for line in lines:
                # Extract timestamp
                ts_match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
                if ts_match:
                    stats['last_timestamp'] = ts_match.group(1)
                    # Skip lines older than 1 hour
                    try:
                        line_ts = datetime.strptime(ts_match.group(1), '%Y-%m-%d %H:%M:%S')
                        if line_ts < one_hour_ago:
                            continue
                    except:
                        pass
                
                # Track activity
                if 'Checking for new announcements' in line:
                    stats['announcements_checked'] += 1
                
                # Track sync activity
                if 'Companies=' in line:
                    match = re.search(r'Companies=(\d+).*Fetched=(\d+).*Inserted=(\d+).*Skipped=(\d+)', line)
                    if match:
                        stats['companies_synced'] = int(match.group(1))
                        stats['inserted'] = int(match.group(3))
                        stats['skipped'] = int(match.group(4))
                
                # Track errors/warnings
                if 'ERROR' in line:
                    stats['error_count'] += 1
                if 'WARNING' in line:
                    stats['warning_count'] += 1
                
                # Track specific failures
                if 'Timeout' in line:
                    stats['timeouts'] += 1
                if 'getaddrinfo failed' in line:
                    stats['dns_failures'] += 1
                if '429' in line:
                    stats['rate_limits'] += 1
            
            # Check if process is active (log updated in last 2 minutes)
            if stats['last_timestamp']:
                last_ts = datetime.strptime(stats['last_timestamp'], '%Y-%m-%d %H:%M:%S')
                time_diff = (datetime.now() - last_ts).total_seconds()
                stats['is_active'] = time_diff < 120
                stats['last_activity_seconds_ago'] = int(time_diff)
        
        except Exception as e:
            return None
        
        return stats
    
    def get_database_stats(self):
        """Get statistics from database."""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            stats = {}
            
            cursor.execute("SELECT COUNT(*) FROM insider_signals WHERE transaction_type = 'MARKET_PURCHASE'")
            stats['market_purchase_signals'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM announcements")
            stats['announcements_processed'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM documents")
            stats['documents_stored'] = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT COUNT(*) FROM insider_signals 
                WHERE shares IS NOT NULL AND transaction_type = 'MARKET_PURCHASE'
            """)
            with_shares = cursor.fetchone()[0]
            total = max(stats['market_purchase_signals'], 1)
            stats['extraction_success_rate'] = f"{100*with_shares/total:.1f}%"
            
            conn.close()
            return stats
        
        except Exception as e:
            return None
    
    def check_health(self):
        """Comprehensive health check."""
        issues = []
        warnings = []
        
        log_stats = self.get_log_stats()
        db_stats = self.get_database_stats()
        
        if not log_stats:
            issues.append("Log file not accessible")
            return {'issues': issues, 'warnings': warnings}
        
        # Check 1: Process activity
        if not log_stats['is_active']:
            issues.append(f"Process inactive for {log_stats['last_activity_seconds_ago']}s")
        
        # Check 2: Error rate
        if log_stats['error_count'] > 10:
            issues.append(f"High error count: {log_stats['error_count']}")
        elif log_stats['error_count'] > 0:
            warnings.append(f"Recent errors: {log_stats['error_count']}")
        
        # Check 3: DNS failures
        if log_stats['dns_failures'] > 3:
            warnings.append(f"DNS failures: {log_stats['dns_failures']}")
        
        # Check 4: Rate limiting
        if log_stats['rate_limits'] > 0:
            warnings.append(f"Rate limit hits: {log_stats['rate_limits']}")
        
        # Check 5: Timeouts
        if log_stats['timeouts'] > 5:
            warnings.append(f"Timeouts: {log_stats['timeouts']}")
        
        return {
            'issues': issues,
            'warnings': warnings,
            'log_stats': log_stats,
            'db_stats': db_stats,
        }
    
    def print_report(self):
        """Print comprehensive monitoring report."""
        health = self.check_health()
        
        print("\n" + "=" * 100)
        print("SGX PIPELINE - MONITORING REPORT")
        print("=" * 100)
        print(f"Report Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Critical Issues
        if health['issues']:
            print(f"[CRITICAL] Issues ({len(health['issues'])}):")
            for issue in health['issues']:
                print(f"  [FAIL] {issue}")
        else:
            print(f"[OK] No critical issues")
        
        # Warnings
        if health['warnings']:
            print(f"\n[WARNING] ({len(health['warnings'])}):")
            for warning in health['warnings']:
                print(f"  [WARN] {warning}")
        else:
            print(f"\n[OK] No warnings")
        
        # Log Metrics
        log_m = health.get('log_stats', {})
        if log_m:
            print(f"\n[LOG METRICS]")
            print(f"  Process active: {'YES' if log_m.get('is_active') else 'NO'}")
            print(f"  Last activity: {log_m.get('last_activity_seconds_ago', 'N/A')}s ago")
            print(f"  Announcements checked: {log_m.get('announcements_checked', 0)}")
            print(f"  Companies synced: {log_m.get('companies_synced', 0)}")
            print(f"  Inserted/Skipped: {log_m.get('inserted', 0)}/{log_m.get('skipped', 0)}")
            print(f"  Errors/Warnings: {log_m.get('error_count', 0)}/{log_m.get('warning_count', 0)}")
            print(f"  DNS failures: {log_m.get('dns_failures', 0)}")
            print(f"  Rate limits: {log_m.get('rate_limits', 0)}")
            print(f"  Timeouts: {log_m.get('timeouts', 0)}")
        
        # DB Metrics
        db_m = health.get('db_stats', {})
        if db_m:
            print(f"\n[DATABASE METRICS]")
            print(f"  Market purchase signals: {db_m.get('market_purchase_signals', 0)}")
            print(f"  Announcements processed: {db_m.get('announcements_processed', 0)}")
            print(f"  Documents stored: {db_m.get('documents_stored', 0)}")
            print(f"  Extraction success rate: {db_m.get('extraction_success_rate', 'N/A')}")
        
        print("\n" + "=" * 100)


if __name__ == '__main__':
    monitor = PipelineMonitor()
    monitor.print_report()

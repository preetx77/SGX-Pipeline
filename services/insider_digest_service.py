"""
Insider Digest Service

Generates daily digest summaries of insider signals
by querying the database for signals within a date range.

Built from accumulated database records, not live state.
"""

from datetime import datetime, timedelta
from database.insider_signal_repository import InsiderSignalRepository
from database.database import DatabaseManager
import logging


class InsiderDigestService:
    """
    Generates plain-text digest summaries of insider activity.
    
    Queries the insider_signals table for signals within a date range,
    groups by stock code and decision, and formats as plain text.
    """

    def __init__(self):
        self.repository = InsiderSignalRepository()
        self.db = DatabaseManager()

    def generate_digest(self, date=None):
        """
        Generate digest for a specific date (defaults to today).
        
        Args:
            date: datetime.date object or None for today
            
        Returns:
            Plain text digest string
        """
        if date is None:
            date = datetime.now().date()

        # Query signals for the specified date
        query = """
            SELECT 
                company_name,
                stock_code,
                decision,
                COUNT(*) as count,
                SUM(CASE WHEN shares IS NOT NULL THEN shares ELSE 0 END) as total_shares,
                SUM(CASE WHEN value IS NOT NULL THEN value ELSE 0 END) as total_value,
                GROUP_CONCAT(announcement_id, ', ') as announcement_ids
            FROM insider_signals 
            WHERE DATE(created_at) = ?
            GROUP BY stock_code, decision
            ORDER BY stock_code ASC, decision DESC
        """

        try:
            results = self.db.fetchall(query, (date,))
        except Exception as e:
            logging.error(f"Failed to query signals for digest: {e}")
            return None

        if not results:
            return self._format_empty_digest(date)

        # Format digest
        return self._format_digest(date, results)

    def _format_digest(self, date, results):
        """Format query results into plain text digest."""
        
        lines = []
        lines.append(f"SGX INSIDER DIGEST - {date.strftime('%d %b %Y')}")
        lines.append("=" * 60)
        lines.append("")

        # Group by stock code
        by_stock = {}
        for company, code, decision, count, total_shares, total_value, anns in results:
            if code not in by_stock:
                by_stock[code] = {
                    'company': company,
                    'signals': []
                }
            
            by_stock[code]['signals'].append({
                'decision': decision,
                'count': count,
                'shares': total_shares if total_shares else 0,
                'value': total_value if total_value else 0.0
            })

        # Format by stock code
        for code in sorted(by_stock.keys()):
            stock_info = by_stock[code]
            company = stock_info['company']
            
            # Handle bad company names (e.g., "MULTIPLE")
            if not company or company == "MULTIPLE" or company.strip() == "":
                company = f"[Stock {code}]"
            
            lines.append(f"📊 {code} - {company}")
            
            for sig in stock_info['signals']:
                decision = sig['decision']
                count = sig['count']
                shares = sig['shares']
                value = sig['value']
                
                # Color-coded marker
                if decision == 'BUY':
                    marker = "🟢 BUY"
                elif decision == 'SELL':
                    marker = "🔴 SELL"
                else:
                    marker = "⚪ IGNORE"
                
                # Format line with transaction details if available
                details = []
                if shares > 0:
                    details.append(f"{shares:,} shares")
                if value > 0:
                    details.append(f"SGD {value:,.2f}")
                
                detail_str = f" ({', '.join(details)})" if details else ""
                
                lines.append(f"  {marker} - {count} signal(s){detail_str}")
            
            lines.append("")

        lines.append("=" * 60)
        lines.append(f"Generated: {datetime.now().strftime('%d %b %Y at %H:%M:%S')}")

        return "\n".join(lines)

    def _format_empty_digest(self, date):
        """Format digest when no signals found."""
        lines = []
        lines.append(f"SGX INSIDER DIGEST - {date.strftime('%d %b %Y')}")
        lines.append("=" * 60)
        lines.append("")
        lines.append("No insider signals for this date.")
        lines.append("")
        lines.append("=" * 60)
        lines.append(f"Generated: {datetime.now().strftime('%d %b %Y at %H:%M:%S')}")
        
        return "\n".join(lines)

    def close(self):
        """Close database connections."""
        self.repository.close()
        self.db.close()

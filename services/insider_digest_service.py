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
        """Format query results into plain text digest with proper grouping and totals."""
        
        lines = []
        lines.append(f"SGX INSIDER DIGEST - {date.strftime('%d %b %Y')}")
        lines.append("=" * 70)
        lines.append("")

        # Fetch full detail for each signal (need director names and filer_type)
        db_results = self.db.fetchall("""
            SELECT 
                announcement_id,
                company_name,
                stock_code,
                director_name,
                filer_type,
                is_corporate_entity,
                decision,
                signal_type,
                shares,
                price,
                value
            FROM insider_signals 
            WHERE DATE(created_at) = ?
            ORDER BY decision DESC, company_name ASC
        """, (date,))

        if not db_results:
            return self._format_empty_digest(date)

        # Group by decision first, then by stock
        buy_signals = []
        sell_signals = []
        ignore_signals = []

        for row in db_results:
            ann_id, company, code, director, filer_type, is_corp, decision, sig_type, shares, price, value = row
            
            # Handle bad company names
            if not company or company == "MULTIPLE" or company.strip() == "":
                company = f"[Stock {code}]"
            
            # Determine filer label
            if not filer_type or filer_type == "DIRECTOR":
                filer_label = "Director"
            elif filer_type == "SUBSTANTIAL_SHAREHOLDER":
                if is_corp:
                    filer_label = "Substantial Shareholder (Corporate)"
                else:
                    filer_label = "Substantial Shareholder"
            else:
                filer_label = filer_type
            
            signal_info = {
                'announcement_id': ann_id,
                'company': company,
                'code': code,
                'director': director or '[Name Unknown]',
                'filer_label': filer_label,
                'decision': decision,
                'sig_type': sig_type,
                'shares': shares,
                'price': price,
                'value': value
            }
            
            if decision == 'BUY':
                buy_signals.append(signal_info)
            elif decision == 'SELL':
                sell_signals.append(signal_info)
            else:
                ignore_signals.append(signal_info)

        # Track totals
        total_buys = len(buy_signals)
        total_sells = len(sell_signals)
        total_ignores = len(ignore_signals)
        total_signals = total_buys + total_sells + total_ignores

        # Format BUY section
        if buy_signals:
            lines.append("🟢 BUYS")
            lines.append("-" * 70)
            buy_shares = 0
            buy_value = 0.0
            for sig in buy_signals:
                filer = sig['director']
                company = sig['company']
                code = sig['code']
                filer_label = sig['filer_label']
                shares = sig['shares']
                price = sig['price']
                value = sig['value']
                
                # Format details
                details = []
                if shares:
                    details.append(f"{shares:,} shares")
                    buy_shares += shares
                if price:
                    details.append(f"@ SGD {price:.4f}")
                if value:
                    details.append(f"= SGD {value:,.2f}")
                    buy_value += value
                
                detail_str = " | ".join(details) if details else "(no details)"
                lines.append(f"  {code} {company}")
                lines.append(f"    {filer_label}: {filer}")
                lines.append(f"    {detail_str}")
                lines.append("")
            
            lines.append(f"  Subtotal: {total_buys} buy(s), {buy_shares:,} shares")
            if buy_value > 0:
                lines.append(f"  Value: SGD {buy_value:,.2f}")
            lines.append("")

        # Format SELL section
        if sell_signals:
            lines.append("🔴 SELLS")
            lines.append("-" * 70)
            sell_shares = 0
            sell_value = 0.0
            for sig in sell_signals:
                filer = sig['director']
                company = sig['company']
                code = sig['code']
                filer_label = sig['filer_label']
                shares = sig['shares']
                price = sig['price']
                value = sig['value']
                
                # Format details
                details = []
                if shares:
                    details.append(f"{shares:,} shares")
                    sell_shares += shares
                if price:
                    details.append(f"@ SGD {price:.4f}")
                if value:
                    details.append(f"= SGD {value:,.2f}")
                    sell_value += value
                
                detail_str = " | ".join(details) if details else "(no details)"
                lines.append(f"  {code} {company}")
                lines.append(f"    {filer_label}: {filer}")
                lines.append(f"    {detail_str}")
                lines.append("")
            
            lines.append(f"  Subtotal: {total_sells} sell(s), {sell_shares:,} shares")
            if sell_value > 0:
                lines.append(f"  Value: SGD {sell_value:,.2f}")
            lines.append("")

        # Format IGNORE section (if any)
        if ignore_signals:
            lines.append("⚪ CORPORATE ACTIONS / SHAREHOLDER FILINGS")
            lines.append("-" * 70)
            for sig in ignore_signals:
                code = sig['code']
                company = sig['company']
                filer = sig['director']
                filer_label = sig['filer_label']
                sig_type = sig['sig_type']
                shares = sig['shares']
                
                details = []
                if sig_type:
                    details.append(f"Type: {sig_type}")
                if shares:
                    details.append(f"{shares:,} shares")
                
                detail_str = " | ".join(details) if details else ""
                lines.append(f"  {code} {company}")
                lines.append(f"    {filer_label}: {filer}")
                if detail_str:
                    lines.append(f"    {detail_str}")
                lines.append("")
            
            lines.append(f"  Subtotal: {total_ignores} action(s)")
            lines.append("")

        # Summary totals
        lines.append("=" * 70)
        lines.append("SUMMARY")
        lines.append(f"  Buys: {total_buys}")
        lines.append(f"  Sells: {total_sells}")
        lines.append(f"  Corporate Actions/Filings: {total_ignores}")
        lines.append(f"  Total: {total_signals} signal(s)")
        lines.append("")
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

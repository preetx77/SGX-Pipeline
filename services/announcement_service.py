# announcement service
# coordinates the SGX client and repository

import logging
from datetime import datetime, timedelta
from scraper.client import SGXClient
from database.announcement_repository import AnnouncementRepository
from services.attachment_service import AttachmentService
from core.classifier import classify
from core.analysis import AnnouncementAnalysis
from services.insider_pipeline import InsiderPipeline
from services.document_pipeline import DocumentService
from core.event_type import EventType
from models.document import DocumentType

class AnnouncementService:

    def __init__(self):
        self.client = SGXClient()
        self.repository = AnnouncementRepository()
        self.attachment_service = AttachmentService()
        self.insider_pipeline = InsiderPipeline()
        self.document_service = DocumentService()


    def sync_company(self, company):
        """Sync announcements for a single company"""
        
        latest_timestamp = self.repository.get_latest_timestamp(company.code)
        
        end = datetime.now()
        
        if latest_timestamp:
            # latest_timestamp is in milliseconds, convert to seconds
            from datetime import datetime as dt
            latest_date = dt.fromtimestamp(latest_timestamp / 1000)
            start = latest_date - timedelta(days=1)
        else:
            start = end - timedelta(days=90)
        
        period_start = start.strftime("%Y%m%d_000000")
        period_end = end.strftime("%Y%m%d_235959")
        
        logging.info(f"Syncing {company.name} ({company.code})")
        logging.info(f"Period: {period_start} to {period_end}")
        
        try:
            announcements = self.client.get_company_announcement(
                company.name,
                period_start=period_start,
                period_end=period_end
            )
        except Exception as e:
            logging.error(f"Failed to fetch announcements for {company.name}: {e}")
            return {
                "company": company.name,
                "stock_code": company.code,
                "period_start": period_start,
                "period_end": period_end,
                "announcements_fetched": 0,
                "announcements_inserted": 0,
                "announcements_skipped": 0,
                "error": str(e)
            }

        logging.info(f"Fetched {len(announcements)} announcements for {company.name}")
        
        inserted = 0
        skipped = 0
        attachment_discovered = 0
        attachment_inserted = 0
        attachment_downloaded = 0
        attachment_skipped = 0
        
        for announcement in announcements:

            # -------------------------
            # Classify announcement
            # -------------------------
            classification = classify(announcement)

            analysis = AnnouncementAnalysis(classification = classification)

            logging.debug(
                f"[{company.name}] {announcement.title} | "
                f"Type: {analysis.classification.event_type.value} | "
                f"Priority: {analysis.classification.priority.label}"
            )

            # Save announcement
            is_new = self.repository.insert(announcement)

            if not is_new:
                skipped += 1
                continue

            inserted += 1
            logging.info(f"New announcement: {announcement.announcement_id}")

            # Process insider dealings (director disclosures)
            if "disclosure of interest" in announcement.category.lower():
                try:
                    attachment_result = self.attachment_service.process_announcement(announcement)

                    attachments = (
                        attachment_result["downloaded"] +
                        attachment_result["existing"]
                    )

                    for attachment in attachments:

                        try:
                            document_result = self.document_service.process(
                                announcement,
                                attachment
                            )

                            document = document_result["document"]

                            if document.document_type != DocumentType.DIRECTOR_DEALINGS:
                                continue

                            self.insider_pipeline.process(
                                announcement,
                                [document]
                            )
                        except Exception as e:
                            logging.error(f"Failed to process document {attachment.filename}: {e}")

                    attachment_discovered += len(attachment_result["attachments"])
                    attachment_inserted += len(attachment_result["new"])
                    attachment_downloaded += len(attachment_result["downloaded"])
                    attachment_skipped += len(attachment_result["existing"])

                except Exception as e:
                    logging.error(f"Failed to process attachments for {announcement.announcement_id}: {e}")
            
            # Process corporate events (special meetings, voluntary announcements)
            elif any(keyword in announcement.category.lower() for keyword in 
                    ["extraordinary", "special general meeting", "voluntary announcement", 
                     "circular", "notice"]):
                try:
                    logging.info(f"Corporate event detected: {announcement.category}")
                    # Create a corporate event notification
                    self._notify_corporate_event(announcement)
                except Exception as e:
                    logging.error(f"Failed to process corporate event: {e}")

        logging.info(
            f"Completed {company.name}: "
            f"Inserted={inserted}, Skipped={skipped}, "
            f"Attachments discovered={attachment_discovered}, "
            f"Downloaded={attachment_downloaded}"
        )

        return {
            "company": company.name,
            "stock_code": company.code,
            "period_start": period_start,
            "period_end": period_end,
            "announcements_fetched": len(announcements),
            "announcements_inserted": inserted,
            "announcements_skipped": skipped,
            "attachments_discovered": attachment_discovered,
            "attachments_inserted": attachment_inserted,
            "attachments_downloaded": attachment_downloaded,
            "attachments_skipped": attachment_skipped
        }

    def _notify_corporate_event(self, announcement):
        """Send notification for corporate events"""
        from notifications.telegram_notifier import TelegramNotifier
        
        try:
            notifier = TelegramNotifier()
            
            # Format corporate event message
            message = f"""📢 SGX CORPORATE EVENT

┌─ {announcement.stock_code} ─────────────────────┐

{announcement.company_name}

Event: {announcement.category}

Title: {announcement.title}

Date: {announcement.submission_date}

└────────────────────────────────────┘"""
            
            # Send to all chat IDs
            for chat_id in notifier.chat_ids:
                try:
                    import asyncio
                    asyncio.run(notifier._send(message))
                    logging.info(f"Corporate event notification sent to {chat_id}")
                except Exception as e:
                    logging.error(f"Failed to send corporate event notification: {e}")
                    
            notifier.close()
        except Exception as e:
            logging.error(f"Failed to initialize notifier for corporate event: {e}")

    def sync_watchlist(
        self,
        watchlist,
        period_start=None,
        period_end=None
    ):
        """Sync announcements for multiple companies in watchlist"""
        
        # If dates not provided, use defaults
        if period_start is None or period_end is None:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=90)
            
            period_start = start_date.strftime("%Y%m%d_%H%M%S")
            period_end = end_date.strftime("%Y%m%d_%H%M%S")
        
        summary = {
            "total_companies": len(watchlist),
            "total_fetched": 0,
            "total_inserted": 0,
            "total_skipped": 0,
            "companies": []
        }
        
        for company in watchlist:
            try:
                result = self.sync_company(company)
                
                # Update totals
                summary["total_fetched"] += result["announcements_fetched"]
                summary["total_inserted"] += result["announcements_inserted"]
                summary["total_skipped"] += result["announcements_skipped"]
                
                # Add company result
                summary["companies"].append({
                    "company": company.name,
                    "stock_code": company.code,
                    "fetched": result["announcements_fetched"],
                    "inserted": result["announcements_inserted"],
                    "skipped": result["announcements_skipped"]
                })
                
            except Exception:
                logging.exception(
                    "Failed syncing %s (%s)",
                    company.name,
                    company.code
                )

                summary["companies"].append({
                    "company": company.name,
                    "stock_code": company.code,
                    "error": "Sync failed"
                })
        
        return summary

    def close(self):
        self.repository.close()
        self.attachment_service.close()

import asyncio
import logging

from telegram import Bot
from config.settings import TELEGRAM_TOKEN, CHAT_IDS
from notifications.message_builder import MessageBuilder
from notifications.announcement_builder import AnnouncementBuilder


class TelegramNotifier:

    def __init__(self):

        logging.info(f"Initializing TelegramNotifier")
        
        if not TELEGRAM_TOKEN:
            raise ValueError("Telegram token not configured in .env (TELEGRAM_BOT_TOKEN)")

        if not CHAT_IDS:
            logging.warning("No chat IDs configured (CHAT_IDS empty)")

        self.bot = Bot(token=TELEGRAM_TOKEN)
        self.chat_ids = CHAT_IDS
        self.builder = MessageBuilder()
        self.announcement_builder = AnnouncementBuilder()

        # Create one event loop for this notifier
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    async def _send(self, message: str):

        success_count = 0
        fail_count = 0

        for chat_id in self.chat_ids:
            try:
                await self.bot.send_message(
                    chat_id=chat_id,
                    text=message
                )
                success_count += 1
                logging.info(f"Telegram sent successfully to {chat_id}")

            except Exception as e:
                fail_count += 1
                logging.error(f"Failed to send Telegram to {chat_id}: {e}")

        if fail_count > 0:
            logging.warning(
                f"Telegram notification: {success_count} succeeded, {fail_count} failed"
            )
        
        return success_count > 0

    def notify(self, signal):
        """Send signal notification via Telegram"""
        try:
            message = self.builder.build(signal)
            result = self.loop.run_until_complete(
                self._send(message)
            )
            if result:
                logging.info(f"Signal notification sent for {signal.announcement_id}")
            else:
                logging.warning(f"Signal notification failed for {signal.announcement_id}")
            return result
        except Exception as e:
            logging.error(f"Failed to build/send signal notification: {e}")
            raise

    def notify_announcement(self, company, announcement):
        """Send announcement notification via Telegram"""
        try:
            message = self.announcement_builder.build(
                company,
                announcement
            )

            result = self.loop.run_until_complete(
                self._send(message)
            )
            if result:
                logging.info(f"Announcement notification sent for {announcement.announcement_id}")
            else:
                logging.warning(f"Announcement notification failed for {announcement.announcement_id}")
            return result
        except Exception as e:
            logging.error(f"Failed to build/send announcement notification: {e}")
            raise

    def notify_digest(self, digest_text):
        """Send plain-text digest notification via Telegram"""
        try:
            result = self.loop.run_until_complete(
                self._send(digest_text)
            )
            if result:
                logging.info("Digest notification sent successfully")
            else:
                logging.warning("Digest notification failed")
            return result
        except Exception as e:
            logging.error(f"Failed to send digest notification: {e}")
            raise

    def close(self):
        """Close the event loop and cleanup resources"""
        try:
            self.loop.close()
            logging.info("TelegramNotifier closed")
        except Exception as e:
            logging.warning(f"Error closing TelegramNotifier: {e}")
import asyncio

from telegram import Bot

from config.settings import TELEGRAM_TOKEN, CHAT_IDS
from notifications.message_builder import MessageBuilder


class TelegramNotifier:

    def __init__(self):

        print("TelegramNotifier created:", id(self))
        
        if not TELEGRAM_TOKEN:
            raise ValueError("Telegram token not configured.")

        self.bot = Bot(token=TELEGRAM_TOKEN)
        self.chat_ids = CHAT_IDS
        self.builder = MessageBuilder()

        # Create one event loop for this notifier
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    async def _send(self, message: str):

        for chat_id in self.chat_ids:
            try:
                await self.bot.send_message(
                    chat_id=chat_id,
                    text=message
                )

            except Exception as e:
                print(f"Failed to send to {chat_id}: {e}")

    def notify(self, signal):
        message = self.builder.build(signal)
        self.loop.run_until_complete(
            self._send(message)
        )

    def close(self):
        self.loop.close()
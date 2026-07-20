import asyncio
import os

from telegram import Bot
from notifications.message_builder import MessageBuilder


class TelegramNotifier:

    def __init__(self, chat_id: int):

        token = os.getenv("TELEGRAM_BOT_TOKEN")

        if not token:
            raise ValueError(
                "TELEGRAM_BOT_TOKEN environment variable not found."
            )

        self.bot = Bot(token=token)
        self.chat_id = chat_id
        self.builder = MessageBuilder()

    async def _send(self, message: str):
        await self.bot.send_message(
            chat_id=self.chat_id,
            text=message
        )

    def notify(self, signal):
        message = self.builder.build(signal)
        asyncio.run(self._send(message))
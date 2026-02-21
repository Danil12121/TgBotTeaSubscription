import asyncio
import datetime
import logging
import os
import bd_create
import notifications

from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters.callback_data import CallbackData
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
print(BOT_TOKEN)
ADMIN_ID = [123456789, 987654321]

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()


users = {} #{user_id: {"username": str, "status": "unpaid" | "pending" | "paid"}}

admin_messages = {} #{"admin_id": int, "message_id": int}

class AdminConfirmCallback(CallbackData, prefix="admin_tx"):
    action: str
    user_id: int
    tx_number: str


class PaymentState(StatesGroup):
    waiting_for_transaction = State()


async def main():
    logging.basicConfig(level=logging.INFO)
    scheduler = AsyncIOScheduler()

    scheduler.add_job(notifications.monthly_notification, 'cron', day=1, hour=12, minute=0)

    scheduler.add_job(notifications.weekly_notification, 'cron', day=8, hour=12, minute=0)

    scheduler.start()

    dp.include_router(router)

    await bd_create()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
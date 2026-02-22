from src.service_locator import get_repositories
from datetime import datetime
from src.repository.user_repo import UserRepository
async def weekly_notification(logging, users, dp, bot, PaymentState):
    
    logging.info("Запуск еженедельной проверки неоплативших...")
    async_session_maker = await get_repositories()
    async with async_session_maker() as session:
        user_repo = UserRepository(session)
        for user_id, data in users.items():
            if data["status"] == "unpaid":
                try:
                    state = dp.fsm.resolve_context(bot=bot, chat_id=user_id, user_id=user_id)
                    await state.set_state(PaymentState.waiting_for_transaction)
                    price = await user_repo.get_by_tg_id(user_id)
                    await bot.send_message(user_id,
                                    f" Напоминаем: у вас есть неоплаченный счет в {price} рублей. Пожалуйста, отправьте номер транзакции.")
                    await user_repo.update_last_notification(user_id, last_notification_date=datetime.utcnow())
                except Exception as e:
                    logging.error(f"Не удалось отправить сообщение {user_id}: {e}")

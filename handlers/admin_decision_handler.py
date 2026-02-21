from aiogram.types import CallbackQuery
from aiogram import Router
from datetime import datetime

router = Router()

async def admin_handler(router: Router, bot, admin_messages, AdminConfirmCallback, ADMIN_ID, get_repositories):
    @router.callback_query(AdminConfirmCallback.filter())
    async def admin_decision_handler(callback: CallbackQuery, callback_data: AdminConfirmCallback):
        repos = await get_repositories() 
        user_id = callback_data.user_id
        action = callback_data.action
        number = callback_data.tx_number
        admin_id = callback.from_user.id

        if action == "approve":
            await repos.transaction_repo.add(user_id, number, datetime.now(), admin_id)

            await bot.send_message(user_id, "Ваша оплата успешно подтверждена!")
            await callback.message.edit_text(callback.message.text + "\n\n ПОДТВЕРЖДЕНО")

        elif action == "reject":
            await bot.send_message(user_id,
                                " Ваша транзакция отклонена. Пожалуйста, проверьте данные и отправьте номер снова.")
            await callback.message.edit_text(callback.message.text + "\n\n ОТКЛОНЕНО")

        if number in admin_messages:
            for msg_data in admin_messages[number]:
                if msg_data["admin_id"] != admin_id:
                    try:
                        await bot.delete_message(chat_id=msg_data["admin_id"], message_id=msg_data["message_id"])
                    except Exception as e:
                        logging.error(f"Не удалось удалить сообщение у админа {msg_data['admin_id']}: {e}")

            del admin_messages[number]

        await callback.answer()

    return router
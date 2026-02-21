from datetime import datetime

import main
from aiogram.types import CallbackQuery

@main.router.callback_query(main.AdminConfirmCallback.filter())
async def admin_decision_handler(callback: CallbackQuery, callback_data: main.AdminConfirmCallback):
    user_id = callback_data.user_id
    action = callback_data.action
    number = callback_data.tx_number
    admin_id = callback.from_user.id

    if action == "approve":
        update_transaction_table(user_id, number, datetime.now(), admin_id)

        await main.bot.send_message(user_id, "Ваша оплата успешно подтверждена!")
        await callback.message.edit_text(callback.message.text + "\n\n **ПОДТВЕРЖДЕНО**")

    elif action == "reject":
        await main.bot.send_message(user_id,
                               " Ваша транзакция отклонена. Пожалуйста, проверьте данные и отправьте номер снова.")
        await callback.message.edit_text(callback.message.text + "\n\n **ОТКЛОНЕНО**")

    if number in main.admin_messages:
        for msg_data in main.admin_messages[number]:
            if msg_data["admin_id"] != admin_id:
                try:
                    await main.bot.delete_message(chat_id=msg_data["admin_id"], message_id=msg_data["message_id"])
                except Exception as e:
                    main.logging.error(f"Не удалось удалить сообщение у админа {msg_data['admin_id']}: {e}")

        del main.admin_messages[number]

    await callback.answer()
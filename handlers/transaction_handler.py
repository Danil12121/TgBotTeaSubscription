from aiogram.filters import StateFilter
from aiogram.utils.keyboard import InlineKeyboardBuilder
import main
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

@main.router.message(StateFilter(main.PaymentState.waiting_for_transaction))
async def transaction_handler(message: Message, state: FSMContext):
    tx_number = message.text
    user_id = message.from_user.id
    username = message.from_user.username or str(user_id)

    builder = InlineKeyboardBuilder()
    builder.button(text="Подтвердить",
                   callback_data=main.AdminConfirmCallback(action="approve", user_id=user_id, tx_number=tx_number))
    builder.button(text="Отклонить",
                   callback_data=main.AdminConfirmCallback(action="reject", user_id=user_id, tx_number=tx_number))
    builder.adjust(2)

    admin_text = f"Пользователь: @{username}\nID: {user_id}\n Номер транзакции: {tx_number}"

    main.admin_messages[tx_number] = []

    for admin_id in main.ADMIN_ID:
        msg = await main.bot.send_message(chat_id=admin_id, text=admin_text, reply_markup=builder.as_markup())
        main.admin_messages[tx_number].append({"admin_id": admin_id, "message_id": msg.message_id})

    await message.answer("Транзакция отправлена администратору на проверку.")
    await state.clear()
from aiogram.filters import StateFilter
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router
from src.repository.user_repo import UserRepository
async def transaction_handler(router: Router, bot, admin_messages, AdminConfirmCallback, ADMIN_ID, PaymentState, get_repositories):
    @router.message(StateFilter(PaymentState.waiting_for_transaction))
    async def transaction_handler(message: Message, state: FSMContext):
        tx_number = message.text
        user_id = message.from_user.id
        username = message.from_user.username or str(user_id)
        async_session_maker = await get_repositories()
        async with async_session_maker() as session:
            user_repo = UserRepository(session)
            price = await user_repo.get_by_tg_id(user_id) 

            builder = InlineKeyboardBuilder()
            builder.button(text="Подтвердить",
                        callback_data=AdminConfirmCallback(action="approve", user_id=user_id, tx_number=tx_number, price = price))
            builder.button(text="Отклонить",
                        callback_data=AdminConfirmCallback(action="reject", user_id=user_id, tx_number=tx_number, price = price))
            builder.adjust(2)
            
            admin_text = f"Пользователь: @{username}\nID: {user_id}\nВзнос: {price}\nНомер транзакции: {tx_number}"

            admin_messages[tx_number] = []

            for admin_id in ADMIN_ID:
                msg = await bot.send_message(chat_id=admin_id, text=admin_text, reply_markup=builder.as_markup())
                admin_messages[tx_number].append({"admin_id": admin_id, "message_id": msg.message_id})

            await message.answer("Транзакция отправлена администратору на проверку.")
            await state.clear()

    return router
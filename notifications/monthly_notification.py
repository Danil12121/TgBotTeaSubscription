import main

async def monthly_notification():
    main.logging.info("Запуск ежемесячной рассылки...")
    for user_id, data in main.users.items():
        main.users[user_id]["status"] = "unpaid"

        try:
            state = main.dp.fsm.resolve_context(bot=main.bot, chat_id=user_id, user_id=user_id)
            await state.set_state(main.PaymentState.waiting_for_transaction)

            await main.bot.send_message(user_id,
                                   " Пришло время ежемесячной оплаты! Пожалуйста, оплатите и отправьте **номер транзакции** ответным сообщением.")
        except Exception as e:
            main.logging.error(f"Не удалось отправить сообщение {user_id}: {e}")

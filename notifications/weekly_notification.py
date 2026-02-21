import main

async def weekly_notification():
    main.logging.info("Запуск еженедельной проверки неоплативших...")
    for user_id, data in main.users.items():
        if data["status"] == "unpaid":
            try:
                state = main.dp.fsm.resolve_context(bot=main.bot, chat_id=user_id, user_id=user_id)
                await state.set_state(main.PaymentState.waiting_for_transaction)

                await main.bot.send_message(user_id,
                                " Напоминаем: у вас есть неоплаченный счет. Пожалуйста, отправьте **номер транзакции**.")
                update_last_notification(user_id)
            except Exception as e:
                main.logging.error(f"Не удалось отправить сообщение {user_id}: {e}")

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from shivu import application, top_global_groups_collection, pm_users
OWNER_ID = 7078181502

async def broadcast(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("You are not authorized to use this command.")
        return

    message_to_broadcast = update.message.reply_to_message

    if message_to_broadcast is None:
        await update.message.reply_text("Please reply to a message to broadcast.")
        return

    keyboard = [
        [
            InlineKeyboardButton("GCs", callback_data='broadcast_gc'),
            InlineKeyboardButton("Users", callback_data='broadcast_users'),
            InlineKeyboardButton("All", callback_data='broadcast_all')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Where do you want to broadcast?", reply_markup=reply_markup)

async def broadcast_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    choice = query.data.split('_')[1]
    
    if choice == 'gc':
        chats = await top_global_groups_collection.distinct("group_id")
    elif choice == 'users':
        chats = await pm_users.distinct("_id")
    else:  # 'all'
        gc_chats = await top_global_groups_collection.distinct("group_id")
        user_chats = await pm_users.distinct("_id")
        chats = list(set(gc_chats + user_chats))

    message_to_broadcast = query.message.reply_to_message
    total_chats = len(chats)
    successful_sends = 0
    failed_sends = 0

    status_message = await query.message.reply_text("Broadcast starting...")

    for chat_id in chats:
        try:
            await context.bot.forward_message(chat_id=chat_id,
                                              from_chat_id=message_to_broadcast.chat_id,
                                              message_id=message_to_broadcast.message_id)
            successful_sends += 1
        except Exception as e:
            print(f"Failed to send message to {chat_id}: {e}")
            failed_sends += 1

        if (successful_sends + failed_sends) % 5 == 0 or (successful_sends + failed_sends) == total_chats:
            await status_message.edit_text(
                f"Broadcast in progress...\n"
                f"✅ Successful: {successful_sends}\n"
                f"❎ Failed: {failed_sends}\n"
                f"Total: {total_chats}"
            )

    await status_message.edit_text(
        f"Broadcast complete.\n"
        f"✅ Successful: {successful_sends}\n"
        f"❎ Failed: {failed_sends}\n"
        f"Total: {total_chats}"
    )

async def pbroadcast(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("You are not authorized to use this command.")
        return

    pinned_message = await update.message.chat.get_pinned_message()
    
    if pinned_message is None:
        await update.message.reply_text("No pinned message found in this chat.")
        return

    keyboard = [
        [
            InlineKeyboardButton("GCs", callback_data='pbroadcast_gc'),
            InlineKeyboardButton("Users", callback_data='pbroadcast_users'),
            InlineKeyboardButton("All", callback_data='pbroadcast_all')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Where do you want to broadcast the pinned message?", reply_markup=reply_markup)

async def pbroadcast_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    choice = query.data.split('_')[1]
    
    if choice == 'gc':
        chats = await top_global_groups_collection.distinct("group_id")
    elif choice == 'users':
        chats = await pm_users.distinct("_id")
    else:  # 'all'
        gc_chats = await top_global_groups_collection.distinct("group_id")
        user_chats = await pm_users.distinct("_id")
        chats = list(set(gc_chats + user_chats))

    pinned_message = await query.message.chat.get_pinned_message()
    if pinned_message is None:
        await query.message.reply_text("The pinned message is no longer available.")
        return

    total_chats = len(chats)
    successful_sends = 0
    successful_pins = 0
    failed_sends = 0

    status_message = await query.message.reply_text("Broadcast starting...")

    for chat_id in chats:
        try:
            sent_message = await context.bot.forward_message(chat_id=chat_id,
                                                             from_chat_id=pinned_message.chat_id,
                                                             message_id=pinned_message.message_id)
            successful_sends += 1
            try:
                await context.bot.pin_chat_message(chat_id=chat_id, message_id=sent_message.message_id)
                successful_pins += 1
            except Exception as e:
                print(f"Failed to pin message in chat {chat_id}: {e}")
        except Exception as e:
            print(f"Failed to send message to {chat_id}: {e}")
            failed_sends += 1

        if (successful_sends + failed_sends) % 5 == 0 or (successful_sends + failed_sends) == total_chats:
            await status_message.edit_text(
                f"Broadcast in progress...\n"
                f"✅ Broadcast: {successful_sends}\n"
                f"✅ Pins: {successful_pins}\n"
                f"❎ Failed: {failed_sends}\n"
                f"Total: {total_chats}"
            )

    await status_message.edit_text(
        f"Broadcast complete.\n"
        f"✅ Broadcast: {successful_sends}\n"
        f"✅ Pins: {successful_pins}\n"
        f"❎ Failed: {failed_sends}\n"
        f"Total: {total_chats}"
    )

application.add_handler(CommandHandler("lolcast", broadcast, block=False))
application.add_handler(CommandHandler("plolcast", pbroadcast, block=False))
application.add_handler(CallbackQueryHandler(broadcast_callback, pattern='^broadcast_', block=False))
application.add_handler(CallbackQueryHandler(pbroadcast_callback, pattern='^pbroadcast_', block=False))

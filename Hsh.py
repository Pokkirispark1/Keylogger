@Client.on_message((filters.group | filters.private) & filters.text & filters.incoming)
async def give_filter(client, message):
    if (message.chat.type != enums.ChatType.PRIVATE and message.chat.id not in ALLOWED_CHATS):
        return
    elif message.chat.id != SUPPORT_CHAT_ID:
        if message.text.startswith("/"): return
        wait_msg = await message.reply_text("<b>Pʟᴇᴀsᴇ Wᴀɪᴛ ⏳...</b>", parse_mode=enums.ParseMode.HTML, quote=True)
        glob = await global_filters(client, message)
        manual = await manual_filters(client, message)
        await auto_filter(client, message, wait_msg)
        if manual:
            await manual.delete()
        if glob:
            await glob.delete()
    else: #a better logic to avoid repeated lines of code in auto_filter function
        search = message.text
        _, _, total_results = await get_search_results(query=search.lower(), offset=0)
        if total_results == 0:
            return
        else:
            return await message.reply_text(
                text=f"<b>Hᴇʏ {message.from_user.mention}, {str(total_results)} ʀᴇsᴜʟᴛs ᴀʀᴇ ғᴏᴜɴᴅ ɪɴ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ ғᴏʀ ʏᴏᴜʀ ᴏ̨ᴜᴇʀʏ {search}. Kɪɴᴅʟʏ ᴜsᴇ ɪɴʟɪɴᴇ sᴇᴀʀᴄʜ ᴏʀ ᴍᴀᴋᴇ ᴀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴀᴅᴅ ᴍᴇ ᴀs ᴀᴅᴍɪɴ ᴛᴏ ɢᴇᴛ ᴍᴏᴠɪᴇ ғɪʟᴇs. Tʜɪs ɪs ᴀ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ sᴏ ᴛʜᴀᴛ ʏᴏᴜ ᴄᴀɴ'ᴛ ɢᴇᴛ ғɪʟᴇs ғʀᴏᴍ ʜᴇʀᴇ...\n\nFᴏʀ Mᴏᴠɪᴇs, Jᴏɪɴ @free_movies_all_languages</b>",
                parse_mode=enums.ParseMode.HTML
            )

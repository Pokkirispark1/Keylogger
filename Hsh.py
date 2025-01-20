@Client.on_message((filters.group | filters.private) & filters.text & filters.incoming)
async def give_filter(client, message):
    if message.chat.type != enums.ChatType.PRIVATE and message.chat.id not in ALLOWED_CHATS:
        return
    elif message.chat.id != SUPPORT_CHAT_ID:
        if message.text.startswith("/"): 
            return
        
        # Send "Please wait ⏳..." message
        reply_msg = await message.reply_text(
            f"<b><i>Please wait {message.text} ⏳...</i></b>", 
            parse_mode=enums.ParseMode.HTML, 
            quote=True
        )
        
        # Process filters
        glob = await global_filters(client, message)
        manual = await manual_filters(client, message)
        
        # Assume auto_filter updates the "Please wait" message
        results = await auto_filter(client, message, reply_msg)

        # If no results from auto_filter, update the "Please wait" message
        if not results:
            await reply_msg.edit_text(
                text=f"<b>Sorry, no results found for your query: {message.text}</b>",
                parse_mode=enums.ParseMode.HTML
            )
    else:
        # Logic for SUPPORT_CHAT_ID
        search = message.text
        temp_files, temp_offset, total_results = await get_search_results(chat_id=message.chat.id, query=search.lower(), offset=0, filter=True)
        if total_results == 0:
            return await message.reply_text(
                text="<b>No results found for your query.</b>",
                parse_mode=enums.ParseMode.HTML
            )
        else:
            await message.reply_text(
                text=f"<b>Hᴇʏ {message.from_user.mention}, {str(total_results)} ʀᴇsᴜʟᴛs ᴀʀᴇ ғᴏᴜɴᴅ ɪɴ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ ғᴏʀ ʏᴏᴜʀ ᴏ̨ᴜᴇʀʏ {search}. \n\nTʜɪs ɪs ᴀ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ sᴏ ᴛʜᴀᴛ ʏᴏᴜ ᴄᴀɴ'ᴛ ɢᴇᴛ ғɪʟᴇs ғʀᴏᴍ ʜᴇʀᴇ...\n\nJᴏɪɴ ᴀɴᴅ Sᴇᴀʀᴄʜ Hᴇʀᴇ - {GRP_LNK}</b>",
                parse_mode=enums.ParseMode.HTML
            )

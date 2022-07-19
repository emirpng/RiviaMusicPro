import asyncio
import os
import shutil
import subprocess
from sys import version as pyver

from pyrogram import Client, filters
from pyrogram.types import (InlineKeyboardMarkup, InputMediaPhoto, Message,
                            Voice)

from config import get_queue
from Hero import SUDOERS, app, db_mem, random_assistant
from Hero.Database import (get_active_chats, get_active_video_chats,
                            get_assistant, is_active_chat, save_assistant)
from Hero.Decorators.checker import checker, checkerCB
from Hero.Inline import primary_markup,choose_markup
from Hero.Utilities.assistant import get_assistant_details

loop = asyncio.get_event_loop()

__MODULE__ = "ꜱᴜᴅᴏ ᴀꜱɪꜱᴛᴀɴ"
__HELP__ = """

**ɴᴏᴛ:**
Sadece Sudo kullanıcıları için


`/joinasistan` [Sohbet kullanıcı adı veya id]
- Asistan gruplara katılır


`/leaveasistan` [Sohbet kullanıcı adı veya id]
- Asistan belirli bir gruptan ayrılır


`/leavebot` [Sohbet kullanıcı adı veya id]
- Bot belirli bir gruptan ayrılır
"""

@app.on_callback_query(filters.regex("gback_list_chose_stream"))
async def gback_list_chose_stream(_, CallbackQuery):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    videoid, duration, user_id = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(
            "Bu sizin için değil, lütfen kendi şarkınızı arayın.", show_alert=True
        )
    buttons = choose_markup(videoid, duration, user_id)
    await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex("pr_go_back_timer"))
async def pr_go_back_timer(_, CallbackQuery):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    videoid, user_id = callback_request.split("|")
    if await is_active_chat(CallbackQuery.message.chat.id):
        if db_mem[CallbackQuery.message.chat.id]["videoid"] == videoid:
            dur_left = db_mem[CallbackQuery.message.chat.id]["left"]
            duration_min = db_mem[CallbackQuery.message.chat.id]["total"]
            buttons = primary_markup(videoid, user_id, dur_left, duration_min)
            await CallbackQuery.edit_message_reply_markup(
                reply_markup=InlineKeyboardMarkup(buttons)
            )


@app.on_callback_query(filters.regex("timer_checkup_markup"))
async def timer_checkup_markup(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    videoid, user_id = callback_request.split("|")
    if await is_active_chat(CallbackQuery.message.chat.id):
        if db_mem[CallbackQuery.message.chat.id]["videoid"] == videoid:
            dur_left = db_mem[CallbackQuery.message.chat.id]["left"]
            duration_min = db_mem[CallbackQuery.message.chat.id]["total"]
            return await CallbackQuery.answer(
                f"ʀᴇᴍᴀɪɴɪɴɢ {dur_left} ᴏᴜᴛ ᴏғ {duration_min} ᴍɪɴs...",
                show_alert=True,
            )
        return await CallbackQuery.answer(f"ɴᴏᴛ ᴘʟᴀʏɪɴɢ...", show_alert=True)
    else:
        return await CallbackQuery.answer(
            f"Aktif bir sesli sohbet yok.", show_alert=True
        )


@app.on_message(filters.command("sira"))
async def activevc(_, message: Message):
    global get_queue
    if await is_active_chat(message.chat.id):
        mystic = await message.reply_text("ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ɢᴇᴛᴛɪɴɢ ǫᴜᴇᴜᴇ...")
        dur_left = db_mem[message.chat.id]["left"]
        duration_min = db_mem[message.chat.id]["total"]
        got_queue = get_queue.get(message.chat.id)
        if not got_queue:
            await mystic.edit(f"Sıra bulunamadı")
        fetched = []
        for get in got_queue:
            fetched.append(get)

        ### Results
        current_playing = fetched[0][0]
        user_name = fetched[0][1]

        msg = "**Sıra Listesi**\n\n"
        msg += "**Çalmakta Olan:**"
        msg += "\n▶️" + current_playing[:30]
        msg += f"\n   ╚Tarafından:- {user_name}"
        msg += f"\n   ╚Süre:- ʀᴇᴍᴀɪɴɪɴɢ `{dur_left}` ᴏᴜᴛ ᴏғ `{duration_min}` ᴍɪɴs."
        fetched.pop(0)
        if fetched:
            msg += "\n\n"
            msg += "**Sıradakiler:**\n"
            for song in fetched:
                name = song[0][:30]
                usr = song[1]
                dur = song[2]
                msg += f"\n⏸️ {name}"
                msg += f"\n   ╠Süre : {dur}"
                msg += f"\n   ╚Ekleyen : {usr}\n"
        if len(msg) > 4096:
            await mystic.delete()
            filename = "queue.txt"
            with open(filename, "w+", encoding="utf8") as out_file:
                out_file.write(str(msg.strip()))
            await message.reply_document(
                document=filename,
                caption=f"**ᴏᴜᴛᴘᴜᴛ:**\n\n`Sıra Listesi`",
                quote=False,
            )
            os.remove(filename)
        else:
            await mystic.edit(msg)
    else:
        await message.reply_text(f"Sıra bulunamadı")


@app.on_message(filters.command(["vc", "aktifvc"]) & filters.user(SUDOERS))
async def activevc(_, message: Message):
    served_chats = []
    try:
        chats = await get_active_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
    except Exception as e:
        await message.reply_text(f"**Hata:-** {e}")
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await app.get_chat(x)).title
        except Exception:
            title = "Özel Grup"
        if (await app.get_chat(x)).username:
            user = (await app.get_chat(x)).username
            text += (
                f"<b>{j + 1}.</b>  [{title}](https://t.me/{user})[`{x}`]\n"
            )
        else:
            text += f"<b>{j + 1}. {title}</b> [`{x}`]\n"
        j += 1
    if not text:
        await message.reply_text("Aktif bir sesli sohbet yok.")
    else:
        await message.reply_text(
            f"**Akfif Sesli Sohbetler:-**\n\n{text}",
            disable_web_page_preview=True,
        )


@app.on_message(filters.command(["ac", "aktifvc"]) & filters.user(SUDOERS))
async def activevi_(_, message: Message):
    served_chats = []
    try:
        chats = await get_active_video_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
    except Exception as e:
        await message.reply_text(f"**Hata:-** {e}")
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await app.get_chat(x)).title
        except Exception:
            title = "Private Group"
        if (await app.get_chat(x)).username:
            user = (await app.get_chat(x)).username
            text += (
                f"<b>{j + 1}.</b>  [{title}](https://t.me/{user})[`{x}`]\n"
            )
        else:
            text += f"<b>{j + 1}. {title}</b> [`{x}`]\n"
        j += 1
    if not text:
        await message.reply_text("Aktif bir sesli sohbet yok")
    else:
        await message.reply_text(
            f"**Aktif Video Görüşmeleri:-**\n\n{text}",
            disable_web_page_preview=True,
        )


@app.on_message(filters.command(["join", "asistan"]) & filters.user(SUDOERS))
async def basffy(_, message):
    if len(message.command) != 2:
        await message.reply_text(
            "**ᴜsᴀɢᴇ:**\n`/asistan` [Sohbet kullanıcı adı veya id]"
        )
        return
    chat = message.text.split(None, 2)[1]
    try:
        chat_id = (await app.get_chat(chat)).id
    except:
        return await message.reply_text(
            "ᴀᴅᴅ ʙᴏᴛ ᴛᴏ ᴛʜɪs ᴄʜᴀᴛ ғɪʀsᴛ ᴜɴᴋɴᴏᴡɴ ᴄʜᴀᴛ ғᴏʀ ᴛʜᴇ ʙᴏᴛ..."
        )
    _assistant = await get_assistant(chat_id, "assistant")
    if not _assistant:
        return await message.reply_text(
            "Önceden kaydedilmiş asistan bulunamadı.\n\nAsistanı {Chat} grubu içinde /play komutu üzerinden ayarlayabilirsiniz."
        )
    else:
        ran_ass = _assistant["saveassistant"]
    ASS_ID, ASS_NAME, ASS_USERNAME, ASS_ACC = await get_assistant_details(
        ran_ass
    )
    try:
        await ASS_ACC.join_chat(chat_id)
    except Exception as e:
        await message.reply_text(f"Hata oluştu...\n**Olası neden olabilir:**:{e}")
        return
    await message.reply_text("ᴊᴏɪɴᴇᴅ...")


@app.on_message(filters.command("leavebot") & filters.user(SUDOERS))
async def baaaf(_, message):
    if len(message.command) != 2:
        await message.reply_text(
            "**ᴜsᴀɢᴇ:**\n`/leavebot` [Sohbet kullanıcı adı veya id]"
        )
        return
    chat = message.text.split(None, 2)[1]
    try:
        await app.leave_chat(chat)
    except Exception as e:
        await message.reply_text(f"Hata oluştu...\n**Olası neden olabilir:**:{e}")
        print(e)
        return
    await message.reply_text("Bot sohbetten başarıyla ayrıldı.")


@app.on_message(filters.command(["leave", "ayril"]) & filters.user(SUDOERS))
async def baujaf(_, message):
    if len(message.command) != 2:
        await message.reply_text(
            "**ᴜsᴀɢᴇ:**\n`/leave` [Sohbet kullanıcı adı veya id]"
        )
        return
    chat = message.text.split(None, 2)[1]
    try:
        chat_id = (await app.get_chat(chat)).id
    except:
        return await message.reply_text(
            "ᴀᴅᴅ ʙᴏᴛ ᴛᴏ ᴛʜɪs ᴄʜᴀᴛ ғɪʀsᴛ ᴜɴᴋɴᴏᴡɴ ᴄʜᴀᴛ ғᴏʀ ᴛʜᴇ ʙᴏᴛ..."
        )
    _assistant = await get_assistant(chat, "assistant")
    if not _assistant:
        return await message.reply_text(
            "Önceden kaydedilmiş asistan bulunamadı.\n\nAsistanı {Chat} grubu içinde /play komutu üzerinden ayarlayabilirsiniz."
        )
    else:
        ran_ass = _assistant["kayitasistan"]
    ASS_ID, ASS_NAME, ASS_USERNAME, ASS_ACC = await get_assistant_details(
        ran_ass
    )
    try:
        await ASS_ACC.leave_chat(chat_id)
    except Exception as e:
        await message.reply_text(f"Hata oluştu\n**Olası sebep olabilir**:{e}")
        return
    await message.reply_text("ʟᴇғᴛ...")

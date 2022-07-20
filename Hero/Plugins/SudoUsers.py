import asyncio
import os
import shutil
import subprocess
from sys import version as pyver

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message

from config import LOG_SESSION, OWNER_ID
from Hero import BOT_ID, BOT_USERNAME, MUSIC_BOT_NAME, OWNER_ID, SUDOERS, app
from Hero.Database import (add_gban_user, add_off, add_on, add_sudo,
                            get_active_chats, get_served_chats, get_sudoers,
                            is_gbanned_user, remove_active_chat,
                            remove_gban_user, remove_served_chat, remove_sudo,
                            set_video_limit)

__MODULE__ = "sᴜᴅᴏ ᴜsᴇʀs"
__HELP__ = """
/sudolist 
    Check the sudo user list of Bot. 
**Note:**
Only for Sudo Users. 
/addsudo [Username or Reply to a user]
- To Add A User In Bot's Sudo Users.
/delsudo [Username or Reply to a user]
- To Remove A User from Bot's Sudo Users.
/maintenance [enable / disable]
- When enabled Bot goes under maintenance mode. No one can play Music now!
/logger [enable / disable]
- When enabled Bot logs the searched queries in logger group.
/clean
- Clean Temp Files and Logs.
"""
# Add Sudo Users!


@app.on_message(filters.command("addsudo") & filters.user(OWNER_ID))
async def useradd(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "Balas pesan pengguna atau berikan nama pengguna/id_pengguna."
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        message.from_user
        sudoers = await get_sudoers()
        if user.id in sudoers:
            return await message.reply_text("Sudah menjadi Pengguna Sudo.")
        added = await add_sudo(user.id)
        if added:
            await message.reply_text(
                f"Ditambahkan **{user.mention}** Sebagai Pengguna sudo"
            )
            return os.execvp("python3", ["python3", "-m", "Hero"])
        await edit_or_reply(message, text="Terjadi kesalahan, periksa log.")
        return
    message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    sudoers = await get_sudoers()
    if user_id in sudoers:
        return await message.reply_text("Sudah menjadi Pengguna Sudo.")
    added = await add_sudo(user_id)
    if added:
        await message.reply_text(f"Ditambahkan **{mention}** Sebagai Pengguna Sudo")
        return os.execvp("python3", ["python3", "-m", "Hero"])
    await edit_or_reply(message, text="Terjadi kesalahan, periksa log.")
    return


@app.on_message(filters.command("delsudo") & filters.user(OWNER_ID))
async def userdel(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "Membalas pesan pengguna atau memberikan nama pengguna/id_pengguna."
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        message.from_user
        if user.id not in await get_sudoers():
            return await message.reply_text(f"Not a part of Music's Sudo.")
        removed = await remove_sudo(user.id)
        if removed:
            await message.reply_text(f"Menghapus **{user.mention}** dari Sudo.")
            return os.execvp("python3", ["python3", "-m", "Hero"])
        await message.reply_text(f"Sesuatu yang salah terjadi.")
        return
    message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    if user_id not in await get_sudoers():
        return await message.reply_text(f"Bukan bagian dari Sudo Musik.")
    removed = await remove_sudo(user_id)
    if removed:
        await message.reply_text(f"Menghapus **{mention}** dari Sudo.")
        return os.execvp("python3", ["python3", "-m", "Hero"])
    await message.reply_text(f"Something wrong happened.")


@app.on_message(filters.command("sudolist"))
async def sudoers_list(_, message: Message):
    sudoers = await get_sudoers()
    text = "**Daftar Pengguna Sudo**\n\n"
    for count, user_id in enumerate(sudoers, 1):
        try:
            user = await app.get_users(user_id)
            user = user.first_name if not user.mention else user.mention
        except Exception:
            continue
        text += f"• {user}\n"
    if not text:
        await message.reply_text("Tidak Ada Pengguna Sudo")
    else:
        await message.reply_text(text)

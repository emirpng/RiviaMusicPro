from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaPhoto, Message)

from Hero import db_mem


def others_markup(videoid, user_id):
    if videoid not in db_mem:
        db_mem[videoid] = {}
    db_mem[videoid]["check"] = 1
    buttons = [
        [
            InlineKeyboardButton(
                text="🔎 Sözler Aranıyor",
                callback_data=f"lyrics {videoid}|{user_id}",
            )
        ],
        [
            InlineKeyboardButton(
                text="✚ Playlist'iniz",
                callback_data=f"your_playlist {videoid}|{user_id}",
            ),
            InlineKeyboardButton(
                text="✚ Grubun Playlist'i",
                callback_data=f"group_playlist {videoid}|{user_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="⬇️ Müzik/Video İndir",
                callback_data=f"audio_video_download {videoid}|{user_id}",
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Geri Dön",
                callback_data=f"pr_go_back_timer {videoid}|{user_id}",
            ),
            InlineKeyboardButton(
                text="🗑 Menüyü Kapat",
                callback_data=f"close",
            ),
        ],
    ]
    return buttons


def download_markup(videoid, user_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="⬇️ Ses Al",
                callback_data=f"gets audio|{videoid}|{user_id}",
            ),
            InlineKeyboardButton(
                text="⬇️ Video Al",
                callback_data=f"gets video|{videoid}|{user_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Geri Dön", callback_data=f"goback {videoid}|{user_id}"
            ),
            InlineKeyboardButton(text="🗑 Menüyü Kapat", callback_data=f"close"),
        ],
    ]
    return buttons

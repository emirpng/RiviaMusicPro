from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaPhoto, Message)

stats1 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="Sistem Durumu", callback_data=f"sys_stats"
            ),
            InlineKeyboardButton(
                text="Depolama Durumu", callback_data=f"sto_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Bot Durumu", callback_data=f"bot_stats"
            ),
            InlineKeyboardButton(
                text="MongoDB Durumu", callback_data=f"mongo_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Asistan Durumu", callback_data=f"assis_stats"
            )
        ],
    ]
)

stats2 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="Genel Durum", callback_data=f"gen_stats"
            ),
            InlineKeyboardButton(
                text="Depolama Durumu", callback_data=f"sto_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Bot Durumu", callback_data=f"bot_stats"
            ),
            InlineKeyboardButton(
                text="MongoDB Durumu", callback_data=f"mongo_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Asistan Durumu", callback_data=f"assis_stats"
            )
        ],
    ]
)

stats3 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="Sistem Durumu", callback_data=f"sys_stats"
            ),
            InlineKeyboardButton(
                text="Genel Durum", callback_data=f"gen_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Bot Durumu", callback_data=f"bot_stats"
            ),
            InlineKeyboardButton(
                text="MongoDB Durumu", callback_data=f"mongo_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Asistan Durumu", callback_data=f"assis_stats"
            )
        ],
    ]
)

stats4 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="Sistem Durumu", callback_data=f"sys_stats"
            ),
            InlineKeyboardButton(
                text="Depolama Durumu", callback_data=f"sto_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Genel Durum", callback_data=f"gen_stats"
            ),
            InlineKeyboardButton(
                text="MongoDB Durumu", callback_data=f"mongo_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Asistan Durumu", callback_data=f"assis_stats"
            )
        ],
    ]
)

stats5 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="Sistem Durumu", callback_data=f"sys_stats"
            ),
            InlineKeyboardButton(
                text="Depolama Durumu", callback_data=f"sto_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Bot Durumu", callback_data=f"bot_stats"
            ),
            InlineKeyboardButton(
                text="Genel Durum", callback_data=f"gen_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Asistan Durumu", callback_data=f"assis_stats"
            )
        ],
    ]
)

stats6 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="Sistem Durumu", callback_data=f"sys_stats"
            ),
            InlineKeyboardButton(
                text="Depolama Durumu", callback_data=f"sto_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Bot Durumu", callback_data=f"bot_stats"
            ),
            InlineKeyboardButton(
                text="MongoDB Durumu", callback_data=f"mongo_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Genel Durum", callback_data=f"gen_stats"
            )
        ],
    ]
)


stats7 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="ɢᴇᴛᴛɪɴɢ ᴀssɪsᴛᴀɴᴛ sᴛᴀᴛs...",
                callback_data=f"wait_stats",
            )
        ]
    ]
)

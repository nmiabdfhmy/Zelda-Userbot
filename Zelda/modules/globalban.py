# Copyright (C) 2020 Catuserbot <https://github.com/sandy1709/catuserbot>
# Ported by @mrismanaziz
# FROM ZELDA USERBOT <https://github.com/nmiabdfhmy/Zelda-Userbot>
# t.me/SharingUserbot
#

import asyncio
from datetime import datetime

from telethon import events
from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import Channel

import Zelda.modules.sql_helper.gban_sql as gban_sql
from Zelda import BOTLOG_CHATID
from Zelda import CMD_HANDLER as cmd
from Zelda import CMD_HELP, DEVS, ALIVE_NAME, bot
from Zelda.events import register
from Zelda.utils import edit_or_reply, get_user_from_event, zelda_cmd

from .admin import BANNED_RIGHTS, UNBAN_RIGHTS


async def admin_groups(grp):
    admgroups = []
    async for dialog in grp.client.iter_dialogs():
        entity = dialog.entity
        if (
            isinstance(entity, Channel)
            and entity.megagroup
            and (entity.creator or entity.admin_rights)
        ):
            admgroups.append(entity.id)
    return admgroups


def mentionuser(name, userid):
    return f"[{name}](tg://user?id={userid})"


@zelda_cmd(pattern="gban(?: |$)(.*)")
@register(incoming=True, from_users=DEVS, pattern=r"^\.cgban(?: |$)(.*)")
async def gban(event):
    if event.fwd_from:
        return
    gbun = await edit_or_reply(event, "`Memproses Global Ban...`")
    start = datetime.now()
    user, reason = await get_user_from_event(event, gbun)
    if not user:
        return
    if user.id == (await event.client.get_me()).id:
        await gbun.edit("**Ngapain NgeGban diri sendiri Goblok 🐽**")
        return
    if user.id in DEVS:
        await gbun.edit("**Gagal GBAN karena dia adalah Pembuat saya 🗿**")
        return
    if gban_sql.is_gbanned(user.id):
        await gbun.edit(
            f"**Si** [Jamet](tg://user?id={user.id}) **ini sudah ada di daftar gbanned**"
        )
    else:
        gban_sql.freakgban(user.id, reason)
    san = []
    san = await admin_groups(event)
    count = 0
    fiz = len(san)
    if fiz == 0:
        await gbun.edit("**Anda Tidak mempunyai GC yang anda admin 🥺**")
        return
    await gbun.edit(
        f"**Memulai Global Ban** [Si Jamet](tg://user?id={user.id}) **dari** `{len(san)}` **Groups**"
    )
    for i in range(fiz):
        try:
            await event.client(EditBannedRequest(san[i], user.id, BANNED_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"**Anda tidak memiliki izin Banned di :**\n**Group Chat :** `{event.chat_id}`",
            )
    end = datetime.now()
    timetaken = (end - start).seconds
    if reason:
        await gbun.edit(
            f"**Added to GBAN List by {ALIVE_NAME}**\n"
            f"`Name        :` [{user.first_name}](tg://user?id={user.id})\n"
            f"`From        :` {count} Groups\n"
            f"`Taking Time :` {timetaken} Seconds\n"
            f"`Reason      :` {reason}\n"
            f"`Status      :` Success Banned\n"
            f"#ZELDAUSERBOT"
        )
    else:
        await gbun.edit(
            f"**Added to GBAN List by {ALIVE_NAME}**\n"
            f"`Name        :` [{user.first_name}](tg://user?id={user.id})\n"
            f"`From        :` {count} Groups\n"
            f"`Taking Time :` {timetaken} Seconds\n"
            f"`Status      :` Success Banned\n"
            f"#ZELDAUSERBOT"
        )


@zelda_cmd(pattern="ungban(?: |$)(.*)")
@register(incoming=True, from_users=DEVS, pattern=r"^\.cungban(?: |$)(.*)")
async def ungban(event):
    if event.fwd_from:
        return
    ungbun = await edit_or_reply(event, "`Membatalkan Global Ban...`")
    start = datetime.now()
    user, reason = await get_user_from_event(event, ungbun)
    if not user:
        return
    if gban_sql.is_gbanned(user.id):
        gban_sql.freakungban(user.id)
    else:
        await ungbun.edit(
            f"**Si** [Jamet](tg://user?id={user.id}) **ini tidak ada dalam daftar gban Anda**"
        )
        return
    san = []
    san = await admin_groups(event)
    count = 0
    fiz = len(san)
    if fiz == 0:
        await ungbun.edit("**Anda Tidak mempunyai GC yang anda admin 🥺**")
        return
    await ungbun.edit(
        f"**Memulai pembatalan Global Ban** [Si Jamet](tg://user?id={user.id}) **dari** `{len(san)}` **Groups**"
    )
    for i in range(fiz):
        try:
            await event.client(EditBannedRequest(san[i], user.id, UNBAN_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"**Anda tidak memiliki izin Banned di :**\n**Group Chat :** `{event.chat_id}`",
            )
    end = datetime.now()
    timetaken = (end - start).seconds
    if reason:
        await ungbun.edit(
            f"**Removed from GBAN List by {ALIVE_NAME}**\n"
            f"`Name        :` [{user.first_name}](tg://user?id={user.id})\n"
            f"`From        :` {count} Groups\n"
            f"`Taking Time :` {timetaken} Seconds\n"
            f"`Reason      :` {reason}\n"
            f"`Status      :` Success Ubanned\n"
            f"#ZELDAUSERBOT"
        )
    else:
        await ungbun.edit(
            f"**Removed from GBAN List by {ALIVE_NAME}**\n"
            f"`Name        :` [{user.first_name}](tg://user?id={user.id})\n"
            f"`From        :` {count} Groups\n"
            f"`Taking Time :` {timetaken} Seconds\n"
            f"`Status      :` Success Unbanned\n"
            f"#ZELDAUSERBOT"
        )


@zelda_cmd(pattern="listgban$")
async def gablist(event):
    if event.fwd_from:
        return
    gbanned_users = gban_sql.get_all_gbanned()
    GBANNED_LIST = "**List Global Banned Saat Ini**\n"
    if len(gbanned_users) > 0:
        for a_user in gbanned_users:
            if a_user.reason:
                GBANNED_LIST += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) **Reason** `{a_user.reason}`\n"
            else:
                GBANNED_LIST += (
                    f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) `No Reason`\n"
                )
    else:
        GBANNED_LIST = "Belum ada Pengguna yang Di-Gban"
    await edit_or_reply(event, GBANNED_LIST)


@bot.on(events.ChatAction)
async def _(event):
    if event.user_joined or event.added_by:
        user = await event.get_user()
        chat = await event.get_chat()
        if gban_sql.is_gbanned(user.id) and chat.admin_rights:
            try:
                await event.client.edit_permissions(
                    chat.id,
                    user.id,
                    view_messages=False,
                )
                await event.reply(
                    f"**#GBanned_User** Joined.\n\n** • First Name:** [{user.first_name}](tg://user?id={user.id})\n • **Action:** `Banned`"
                )
            except BaseException:
                pass


# Ported by @mrismanaziz
# FROM ZELDA USERBOT <https://github.com/nmiabdfhmy/Zelda-Userbot>
# t.me/SharingUserbot


CMD_HELP.update(
    {
        "gban": f"**Plugin : **`gban`\
        \n\n  •  **Syntax :** `{cmd}gban` <username/id>\
        \n  •  **Function : **Melakukan Banned Secara Global Ke Semua Grup Dimana anda Sebagai Admin.\
        \n\n  •  **Syntax :** `{cmd}ungban` <username/id>\
        \n  •  **Function : **Membatalkan Global Banned\
        \n\n  •  **Syntax :** `{cmd}listgban`\
        \n  •  **Function : **Menampilkan List Global Banned\
    "
    }
)

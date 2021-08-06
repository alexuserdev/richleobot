import asyncio

import asyncpg
from telethon import TelegramClient

from telethon.tl.functions.messages import CreateChatRequest
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.functions.messages import CheckChatInviteRequest
from telethon.tl.types import PeerUser

import logging


from tgbot.config import DbConfig



async def create_chat(deal_id):
    print("1000-7")
    client = ("5", 1671038, "97c54e3be8961de2db1b51e5cfda2d03")
    client = TelegramClient(client[0], client[1], client[2])
    await client.start()
    print("100-8")
    user0 = await client.get_entity("@RichleoBot")
    print("IIIIIIIIII")
    res = await client(CreateChatRequest(title=f"Escrow exchange №{deal_id}", users=[user0]))
    print("GEGE")
    chat_id = -res.updates[1].participants.chat_id
    link = await client(ExportChatInviteRequest(chat_id))
    await client.edit_admin(chat_id, user=user0, change_info=True, post_messages=True, edit_messages=True, delete_messages=True,
                            ban_users=True, invite_users=True, is_admin=True)
    conn = await asyncpg.connect(DbConfig.host, password=DbConfig.password)
    await conn.execute(f"insert into escrow_chats(id, link) values ({deal_id}, '{link.link}')")
    return link.link, chat_id

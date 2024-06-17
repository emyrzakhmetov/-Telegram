from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.messages import SendMediaRequest
from telethon.tl.types import InputPeerChannel, InputMediaPhoto, InputMediaDocument
import os
import time
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, FloodWaitError
from telethon.tl.functions.messages import GetHistoryRequest
import html

api_id = ''#айди приложения из https://my.telegram.org/apps
api_hash = ''#хэш приложения из https://my.telegram.org/apps
phone = ''#номер телефона телеграм аккаунта
source_channel_username = ''#ссылка на основной канал
target_channel_username = ''#Ссылка на резервный канал


#Все выше данные вписываются внутрь одинарных ковычек

client = TelegramClient('session_name', api_id, api_hash)


async def main():
    await client.start()
    print("Client Created")

    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

    source_channel = await client.get_entity(source_channel_username)
    target_channel = await client.get_entity(target_channel_username)

    offset_id = 0
    limit = 100

    while True:
        print("Current Offset ID is:", offset_id)
        history = await client(GetHistoryRequest(
            peer=source_channel,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        if not history.messages:
            break
        messages = history.messages

        for message in messages:
            try:
                if message.photo:
                    caption = (message.message or '')[:1024]
                    await client.send_file(
                        target_channel,
                        file=message.photo,
                        caption=caption
                    )
                elif message.document:
                    caption = (message.message or '')[:1024]
                    await client.send_file(
                        target_channel,
                        file=message.document,
                        caption=caption
                    )
                elif message.video:
                    caption = (message.message or '')[:1024]
                    await client.send_file(
                        target_channel,
                        file=message.video,
                        caption=caption
                    )
                elif message.audio:
                    caption = (message.message or '')[:1024]
                    await client.send_file(
                        target_channel,
                        file=message.audio,
                        caption=caption
                    )
                elif message.voice:
                    caption = (message.message or '')[:1024]
                    await client.send_file(
                        target_channel,
                        file=message.voice,
                        caption=caption
                    )
                elif message.contact:
                    contact_info = f'Contact: {message.contact.phone_number} - {message.contact.first_name} {message.contact.last_name}'
                    await client.send_message(
                        target_channel,
                        message=contact_info[:1024]
                    )
                elif message.message:
                    await client.send_message(
                        target_channel,
                        message=message.message
                    )
                else:
                    print(f"Skipping empty or unsupported message with id {message.id}")

            except FloodWaitError as e:
                print(f"Flood wait error: sleeping for {e.seconds} seconds")
                time.sleep(e.seconds)

        offset_id = messages[-1].id

with client:
    client.loop.run_until_complete(main())
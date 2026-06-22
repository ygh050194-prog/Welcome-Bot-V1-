import asyncio
import logging
import sys
import json
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keep_alive import keep_alive

# CONFIGURATION
TOKEN = "8661845324:AAEh3Y669m5V7A8mSFhe9D2SxxuvjDcCCbQ"
ADMIN_ID = 8910295767
CHATS_FILE = "chats.json"

# DATABASE FUNCTIONS
def load_chats():
    if os.path.exists(CHATS_FILE):
        try:
            with open(CHATS_FILE, "r") as f:
                return set(json.load(f))
        except:
            return set()
    return set()

def save_chat(chat_id):
    chats = load_chats()
    if chat_id not in chats:
        chats.add(chat_id)
        with open(CHATS_FILE, "w") as f:
            json.dump(list(chats), f)

dp = Dispatcher()

# COMMAND: /start
@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    save_chat(message.chat.id)
    welcome_text = (
        f"<b>\ud83c\udf1f \ud835\udc16\ud835\udc04\ud835\udc0b\ud835\udc02\ud835\udc0e\ud835\udc0c\ud835\udc04 \ud835\udc13\ud835\udc0e \ud835\udc04\ud835\udc0d\ud835\udc11\ud835\udc08\ud835\udc10\ud835\udc14\ud835\udc04 \ud835\udc01\ud835\udc0e\ud835\udc13 \ud83c\udf1f</b>\n\n"
        f"Hello <b>{message.from_user.full_name}</b>! \ud83d\udc4b\n\n"
        f"\u1000\u103b\u103d\u1014\u103a\u1010\u1031\u102c\u103a (သို့မဟုတ်) \u1000\u103b\u103d\u1014\u103a\u1019ကတော့ Enrique Family ရဲ့ Welcome Bot ဖြစ်ပါတယ်။\n"
        f"\u101eျောပျော်ရွှင်ရွှင်နဲ့ မိသားစုထဲမှာ စကားပြောနိုင်ဖို့ အဖွဲ့ဝင်အသစ်တွေကို ကြိုဆိုပေးမှာပါရှင်။ \u2728\n\n"
        f"\u1021ောက်က Button တွေကိုနှိပ်ပြီး ကျွန်မတို့နဲ့ ချိတ်ဆက်နိုင်ပါတယ်ရှင်။ \ud83d\udc47"
    )
    
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="\ud83d\udce2 Support", url="https://t.me/ENRIQUE_FAMILY"),
        types.InlineKeyboardButton(text="\ud83d\udc64 Owner", url="https://t.me/Official_Enr_Keno")
    )
    
    await message.answer(welcome_text, reply_markup=builder.as_markup())

# COMMAND: /group
@dp.message(Command("group"))
async def command_group_handler(message: types.Message):
    text = "\ud83d\udc65 <b>Enrique Family Group \u1000\u102d\u102f Join \u1011ားပေးပါဦးနော်။</b>"
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="\ud83c\udf10 Join Group", url="https://t.me/ENRIQUE_FAMILY"))
    await message.answer(text, reply_markup=builder.as_markup())

# COMMAND: /help
@dp.message(Command("help"))
async def command_help_handler(message: types.Message):
    help_text = (
        "\ud83d\udca1 <b>\u1021\u101eံုးပြုနည်း လမ်းညွှန်</b>\n\n"
        "၁။ ပထမဦးစွာ Bot ကို သင်၏ Group ထဲသို့ ထည့်သွင်းပါ။\n"
        "၂။ Bot ကို Group တွင် <b>Admin</b> ရာထူး ပေးထားပါ။\n"
        "၃။ Bot သည် အဖွဲ့ဝင်အသစ်ဝင်လာလျှင် (Welcome) နှင့် ထွက်သွားလျှင် (Goodbye) အတွက် အလိုအလျောက် အလုပ်လုပ်ပေးပါမည်။\n\n"
        "\u101eိလိုတာရှိရင် Support Group မှာ မေးမြန်းနိုင်ပါတယ်ရှင်။"
    )
    await message.answer(help_text)

# COMMAND: /broadcast
@dp.message(Command("broadcast"))
async def broadcast_handler(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("\u1024 Command \u1000\u102d\u102f Owner \u101eာ အသုံးပြုနိုင်ပါသည်။")
        return
    
    command_args = message.text.split(maxsplit=1)
    if len(command_args) < 2:
        await message.answer("Example: `/broadcast Hello everyone!`")
        return
    
    text_to_send = command_args[1]
    chats = load_chats()
    count = 0
    for chat_id in chats:
        try:
            await message.bot.send_message(chat_id, f"<b>\ud83d\udce2 \ud835\udc00\ud835\udc0d\ud835\udc0d\ud835\udc0e\ud835\udc14\ud835\udc0d\ud835\udc02\ud835\udc04\ud835\udc0c\ud835\udc04\ud835\udc0d\ud835\udc13</b>\n\n{text_to_send}")
            count += 1
            await asyncio.sleep(0.05) # Avoid flood limit
        except:
            pass
    await message.answer(f"Broadcast \u1015ို့ပြီးပါပြီ။ စုစုပေါင်း: {count} \u1014ေရာ")

# EVENT: NEW MEMBER JOINED
@dp.message(F.new_chat_members)
async def on_user_joined(message: types.Message):
    save_chat(message.chat.id)
    
    # Check if the bot itself was added
    bot_id = (await message.bot.get_me()).id
    is_bot_added = any(member.id == bot_id for member in message.new_chat_members)
    
    if is_bot_added:
        text = (
            "\u1019ဂ်လာပါရှင့် Admin အရင်ပေးပြီးမှ အသုံးပြုလို့ရပါတယ်ရှင့်။\n\n"
            "\u1000\u103b\u103d\u1014\u103a\u1019ကတော့ Welcome/Goodbye အတွက် Auto အလုပ်လုပ်ပေးသွားမှာ ဖြစ်ပါတယ်ရှင့်။"
        )
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(text="\ud83d\udce2 Support", url="https://t.me/ENRIQUE_FAMILY"))
        await message.answer(text, reply_markup=builder.as_markup())
    else:
        # Welcome message for new users
        for user in message.new_chat_members:
            welcome_msg = (
                f"\ud83c\udf8a <b>\ud835\udc16\ud835\udc04\ud835\udc0b\ud835\udc02\ud835\udc0e\ud835\udc0c\ud835\udc04 \ud835\udc13\ud835\udc0e \ud835\udc04\ud835\udc0d\ud835\udc11\ud835\udc08\ud835\udc10\ud835\udc14\ud835\udc04 \ud835\udc05\ud835\udc00\ud835\udc0c\ud835\udc08\ud835\udc0b\ud835\udc18</b> \ud83c\udf8a\n\n"
                f"Hello <a href='tg://user?id={user.id}'>{user.full_name}</a>! \ud83e\udd29\n"
                f"\u1000\u103b\u103d\u1014\u103a\u1010\u1031\u102c\u103aတို့ရဲ့ မိသားစုထဲကို ကြိုဆိုပါတယ်။\n"
                f"\u101eျောပျော်ရွှင်ရွှင်နဲ့ စကားပြောလို့ရပါပြီခင်ဗျာ။ \u2728"
            )
            await message.answer(welcome_msg)

# EVENT: MEMBER LEFT
@dp.message(F.left_chat_member)
async def on_user_left(message: types.Message):
    user = message.left_chat_member
    goodbye_msg = (
        f"\ud83d\udc4b <b>\ud835\udc06\ud835\udc0e\ud835\udc0e\ud835\udc03\ud835\udc01\ud835\udc18\ud835\udc04 \ud835\udc0c\ud835\udc08\ud835\udc12\ud835\udc12 \ud835\udc18\ud835\udc0e\ud835\udc14</b>\n\n"
        f"Bye Bye {user.full_name}! \ud83e\udd7a\n"
        f"\u1014ောကလည်း ပြန်ဆုံကြမယ်နော်။ \u1000ောင်းသောနေ့လေးဖြစ်ပါစေ။ \ud83c\udf08"
    )
    await message.answer(goodbye_msg)

async def main() -> None:
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    print("Bot is starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    keep_alive() # Start Web Server for Render
    asyncio.run(main())

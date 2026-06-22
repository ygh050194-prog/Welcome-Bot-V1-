import asyncio
import logging
import sys
import json
import os
import datetime
import pytz

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keep_alive import keep_alive

TOKEN = "8661845324:AAEh3Y669m5V7A8mSFhe9D2SxxuvjDcCcbQ"
ADMIN_ID = 8910295767
CHATS_FILE = "chats.json"

MYANMAR_TIMEZONE = pytz.timezone('Asia/Yangon')

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

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    save_chat(message.chat.id)
    
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="➕ Add to Group", url=f"https://t.me/enr_welcome_bot?startgroup=true"))
    builder.row(
        types.InlineKeyboardButton(text="🆘 Support", url="https://t.me/Official_Enr_Keno"),
        types.InlineKeyboardButton(text="👤 Owner", url="https://t.me/shwethoonoolay")
    )
    
    welcome_text = (
        "❓ **Bot ကို ဘယ်လိုအသုံးပြုရမလဲ?**\n\n"
        "၁။ ဦးစွာ ကျွန်မကို သင်၏ Group ထဲသို့ ထည့်သွင်းပါ။\n"
        "၂။ ထို့နောက် ကျွန်မကို Admin ရာထူး ပေးထားပါ။\n"
        "၃။ Bot သည် အဖွဲ့ဝင်အသစ်ဝင်လာလျှင် (Welcome) နှင့် ထွက်သွားလျှင် (Goodbye) အတွက် အလိုအလျောက် အလုပ်လုပ်ပေးပါမည်။\n\n"
        "**အသုံးပြုနိုင်သော Command များ -**\n"
        "• /start - Bot ကို စတင်ရန်\n"
        "• /group - Group Link ရယူရန်\n"
        "• /help - အသုံးပြုပုံ လမ်းညွှန်ချက်\n"
        "-------------------------------\n"
        "🌟 【 E N R I Q U E   K E N O 】 >> BOT CREATOR << ရေ ကြိုဆိုပါတယ်ရှင့်! 🌟\n\n"
        "ကျွန်မကတော့ သင့်ရဲ့ Group တွေကို အကောင်းဆုံး စောင့်ရှောက်ပေးမယ့် **Auto Welcome/Goodbye Bot** လေး ဖြစ်ပါတယ်ရှင့်။\n\n"
        "Add to Group ကို နှိပ်ပြီး အသုံးပြုနိုင်ပါတယ်ရှင့်။"
    )
    await message.answer(welcome_text, reply_markup=builder.as_markup(), parse_mode=ParseMode.MARKDOWN)

@dp.message(Command("group"))
async def send_group_link(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🔗 Join Our Group", url="https://t.me/Official_Enr_Keno"))
    await message.answer("ကျွန်မတို့ရဲ့ Official Group Link ကို အောက်က Button မှာ နှိပ်ပြီး ဝင်ရောက်နိုင်ပါတယ်ရှင် 👇", reply_markup=builder.as_markup())

@dp.message(Command("broadcast"))
async def admin_broadcast(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    text_to_send = message.text.replace("/broadcast", "").strip()
    if not text_to_send:
        await message.answer("❌ Broadcast လုပ်မယ့်စာသား ထည့်ပေးပါဦး။ ဥပမာ- `/broadcast မင်္ဂလာပါ`")
        return

    chats = load_chats()
    success_count = 0

    for chat_id in chats:
        try:
            await bot.send_message(chat_id, f"📢 **ANNOUNCEMENT**\n\n{text_to_send}", parse_mode=ParseMode.MARKDOWN)
            success_count += 1
            await asyncio.sleep(0.05)
        except Exception:
            pass

    await message.answer(f"✅ Broadcast ပို့ပြီးပါပြီ။ စုစုပေါင်း: {success_count} နေရာ")

@dp.message(F.new_chat_members)
async def on_user_join(message: types.Message):
    save_chat(message.chat.id)
    bot_id = (await bot.get_me()).id
    is_bot_added = any(member.id == bot_id for member in message.new_chat_members)
    
    if not is_bot_added:
        for user in message.new_chat_members:
            now_utc = datetime.datetime.now(pytz.utc)
            now_myanmar = now_utc.astimezone(MYANMAR_TIMEZONE)
            current_time = now_myanmar.strftime("%I:%M %p")
            current_date = now_myanmar.strftime("%d/%m/%Y")
            
            group_name = message.chat.title if message.chat.title else "Group"
            
            welcome_msg = (
                f"🌟 **{user.full_name}** ရေ {group_name} ကနေ နွေးထွေးစွာ ကြိုဆိုပါတယ်ရှင့်! 🌟\n\n"
                f" f'**Username:** @{user.username if user.username else \"-\"}\n"
                f" f'**ID:** `{user.id}`\n"
                f" f'**Time:** `{current_time}`\n"
                f" f'**Date:** `{current_date}`\n\n"
                "💞 ရည်းစားလည်းဝင်ရှာ၊ စကားလည်းပြောရင်း လူလေးတို့ ပျော်ရွှင်စွာ စကားပြောနိုင်ပါတယ်ရှင့်။ ✨"
            )
            await message.answer(welcome_msg, parse_mode=ParseMode.MARKDOWN)

@dp.message(F.left_chat_member)
async def on_user_left(message: types.Message):
    user = message.left_chat_member
    goodbye_msg = f"👋 **{user.full_name}** က Group ကနေ ထွက်သွားပါပြီ။ နောက်တစ်ခေါက် ပြန်ဆုံကြမယ်လို့ မျှော်လင့်ပါတယ်ရှင့်။ ✨"
    await message.answer(goodbye_msg, parse_mode=ParseMode.MARKDOWN)

async def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    keep_alive()
    await dp.start_polling(bot)

app = bot

if __name__ == "__main__":
    asyncio.run(main())
            

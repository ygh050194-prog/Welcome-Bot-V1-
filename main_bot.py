import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keep_alive import keep_alive

# Bot Token
TOKEN = "8661845324:AAEh3Y669m5V7A8mSFhe9D2SxxuvjDcCCbQ"
ADMIN_ID = 8910295767

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Chat IDs (Broadcast အတွက်)
chat_ids = set()

# /start command
# /start command နေရာမှာ ဒါလေးနဲ့ အစားထိုးပါ
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    chat_ids.add(message.chat.id)
    # အသုံးပြုသူရဲ့ နာမည်ကို ယူခြင်း
    user_name = message.from_user.full_name
    
    text = (
        f"🌟 **{user_name} ရေ ကြိုဆိုပါတယ်ရှင့်!** 🌟\n\n"
        "ကျွန်မကတော့ သင့်ရဲ့ Group တွေကို အကောင်းဆုံး စောင့်ရှောက်ပေးမယ့် "
        "Welcome/Goodbye Bot လေး ဖြစ်ပါတယ်ရှင်။\n\n"
        "အောက်က Button လေးတွေကို နှိပ်ပြီး ကျွန်မတို့နဲ့ ချိတ်ဆက်နိုင်ပါတယ်ရှင်။ ✨"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🆘 Support", url="https://t.me/ENRIQUE_FAMILY"),
            InlineKeyboardButton(text="👤 Owner", url="https://t.me/Official_Enr_Keno")
        ]
    ])
    await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")
    
# /broadcast command (Owner only)
@dp.message(Command("broadcast"))
async def broadcast_command(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    text = message.text.replace("/broadcast", "").strip()
    if not text:
        await message.answer("❌ ပို့ချင်တဲ့စာသားကို /broadcast ရဲ့ နောက်မှာ ရေးပေးပါရှင်။")
        return
    count = 0
    for chat_id in list(chat_ids):
        try:
            await bot.send_message(chat_id, text)
            count += 1
            await asyncio.sleep(0.05)
        except:
            continue
    await message.answer(f"✅ စုစုပေါင်း {count} နေရာကို စာပို့ပြီးပါပြီရှင်။")

# Group ထဲဝင်လာလျှင်
@dp.my_chat_member()
async def on_bot_added(event: types.ChatMemberUpdated):
    if event.new_chat_member.status in ["member", "administrator"]:
        text = (
            "🙏 **မဂ်လာပါရှင့်!**\n\n"
            "ကျွန်မကို အသုံးပြုဖို့အတွက် **Admin** အရင်ပေးထားဖို့ လိုအပ်ပါတယ်ရှင်။\n"
            "ကျွန်မက Welcome/Goodbye အတွက် အလိုအလျောက် အလုပ်လုပ်ပေးသွားမှာ ဖြစ်ပါတယ်ရှင်။"
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🆘 Support", url="https://t.me/ENRIQUE_FAMILY")]
        ])
        await bot.send_message(event.chat.id, text, reply_markup=keyboard)

# Welcome (Member Join)
@dp.message(F.new_chat_members)
async def welcome_member(message: types.Message):
    for member in message.new_chat_members:
        welcome_text = (
            f"🎊 **Welcome {member.full_name}!** 🎊\n\n"
            f"**{message.chat.title}** မှ နွေးထွေးစွာ ကြိုဆိုပါတယ်ရှင်။\n"
            "ပျော်ရွှင်စွာ စကားပြောဆိုနိုင်ပါတယ်ရှင်။ ✨"
        )
        await message.answer(welcome_text)

# Goodbye (Member Leave)
@dp.message(F.left_chat_member)
async def goodbye_member(message: types.Message):
    member = message.left_chat_member
    goodbye_text = (
        f"👋 **Goodbye {member.full_name}!**\n\n"
        "နောက်တစ်ခါ ပြန်ဆုံကြမယ်လို့ မျှော်လင့်ပါတယ်ရှင်။"
    )
    await message.answer(goodbye_text)

async def main():
    keep_alive()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    

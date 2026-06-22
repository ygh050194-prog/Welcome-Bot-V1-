import asyncio
import logging
import datetime # datetime module ကို ထည့်သွင်းပါ
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keep_alive import keep_alive

# Bot Token & Admin ID
TOKEN = "8661845324:AAEh3Y669m5V7A8mSFhe9D2SxxuvjDcCCbQ"
ADMIN_ID = 8910295767

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN)
dp = Dispatcher()
chat_ids = set()

# /start command
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    chat_ids.add(message.chat.id)
    
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    
    # လက်ရှိအချိန်နှင့် နေ့ရက်ကို ရယူခြင်း
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p") # ဥပမာ: 09:30 PM
    current_day = now.strftime("%d/%m/%Y") # ဥပမာ: 22/06/2026

    # Welcome စာသား
    text = (
        f"🌟 **{user_name} ရေ ကြိုဆိုပါတယ်ရှင့်!** 🌟\n\n"
        f"**ID:** `{user_id}`\n"
        f"**Time:** `{current_time}`\n"
        f"**Date:** `{current_day}`\n\n"
        "ကျွန်မကတော့ သင့်ရဲ့ Group တွေကို အကောင်းဆုံး စောင့်ရှောက်ပေးမယ့် "
        "Welcome/Goodbye Bot လေး ဖြစ်ပါတယ်ရှင်။\n\n"
        "**💖 ရည်းစားလည်းဝင်ရှာ၊ စကားလည်းပြောရင်း၊ လူလေးရှိရင် ထည့်ကူပေးလို့ရပါတယ်နော်! 💖**\n\n"
        "အောက်က ခလုတ်လေးတွေကို နှိပ်ပြီး ကျွန်မတို့နဲ့ ချိတ်ဆက်နိုင်ပါတယ်ရှင်။ ✨"
    )
    
    # Inline Keyboard Buttons
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Add to Group", url="https://t.me/enr_welcome_bot?startgroup=true")
        ],
        [
            InlineKeyboardButton(text="🆘 Support", url="https://t.me/ENRIQUE_FAMILY"),
            InlineKeyboardButton(text="👤 Owner", url="https://t.me/Official_Enr_Keno")
        ]
    ])
    
    await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")

# /group command
@dp.message(Command("group"))
async def group_handler(message: types.Message):
    text = "📢 **ကျွန်မတို့ရဲ့ Official Group ကို Join ရန် အောက်ပါ Link ကို နှိပ်ပါရှင် -**\n\n👉 https://t.me/ENRIQUE_FAMILY"
    await message.answer(text, parse_mode="Markdown")

# /help command
@dp.message(Command("help"))
async def help_handler(message: types.Message):
    text = (
        "❓ **Bot ကို ဘယ်လိုအသုံးပြုရမလဲ?**\n\n"
        "၁။ ဦးစွာ ကျွန်မကို သင်၏ Group ထဲသို့ ထည့်သွင်းပါ (Add to Group)။\n"
        "၂။ ထို့နောက် ကျွန်မကို **Admin** ပေးပြီး Message ဖတ်ရှုခွင့် ပြုလုပ်ပေးပါ။\n"
        "၃။ ဒါဆိုရင် အဖွဲ့ဝင်အသစ်ဝင်လာတာနဲ့ (Welcome)၊ ထွက်သွားတာနဲ့ (Goodbye) ကို ကျွန်မက အလိုအလျောက် လုပ်ဆောင်ပေးမှာ ဖြစ်ပါတယ်ရှင်။\n\n"
        "**အသုံးပြုနိုင်သော Command များ -**\n"
        "• /start - Bot ကို စတင်ရန်\n"
        "• /group - Group Link ရယူရန်\n"
        "• /help - အသုံးပြုပုံ လမ်းညွှန်ချက်"
    )
    await message.answer(text, parse_mode="Markdown")

# /broadcast command (Owner only)
@dp.message(Command("broadcast"))
async def broadcast_handler(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ သင်သည် Broadcast ပို့ခွင့်ရှိသော Owner မဟုတ်ပါရှင်။")
        return
    broadcast_text = message.text.replace("/broadcast", "").strip()
    if not broadcast_text:
        await message.answer("❌ ပို့လိုသော စာသားကို ရေးပေးပါရှင်။")
        return
    
    success = 0
    for cid in list(chat_ids):
        try:
            await bot.send_message(cid, broadcast_text)
            success += 1
            await asyncio.sleep(0.05)
        except Exception as e:
            logger.error(f"Failed to send broadcast to {cid}: {e}")
            continue
    await message.answer(f"✅ စုစုပေါင်း {success} နေရာသို့ ပို့ဆောင်ပြီးပါပြီရှင်။")

# Group ထဲဝင်လာလျှင်
@dp.my_chat_member()
async def bot_added_handler(event: types.ChatMemberUpdated):
    if event.new_chat_member.status in ["member", "administrator"]:
        chat_ids.add(event.chat.id)
        text = (
            "🙏 **မင်္ဂလာပါရှင့်!**\n\n"
            "ကျွန်မကို အသုံးပြုဖို့အတွက် **Admin** အရင်ပေးထားဖို့ လိုအပ်ပါတယ်ရှင်။\n"
            "ကျွန်မက Welcome/Goodbye အတွက် အလိုအလျောက် အလုပ်လုပ်ပေးသွားမှာ ဖြစ်ပါတယ်ရှင်။"
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🆘 Support", url="https://t.me/ENRIQUE_FAMILY")]
        ])
        await bot.send_message(event.chat.id, text, reply_markup=keyboard, parse_mode="Markdown")

# Welcome (Member Join)
@dp.message(F.new_chat_members)
async def welcome_handler(message: types.Message):
    for member in message.new_chat_members:
        # Group နာမည်ကို ရယူခြင်း
        group_name = message.chat.title if message.chat.title else "ဤ Group"
        text = (
            f"🎊 **Welcome {member.full_name}!** 🎊\n\n"
            f"**{group_name}** မှ နွေးထွေးစွာ ကြိုဆိုပါတယ်ရှင်။\n"
            "ပျော်ရွှင်စွာ စကားပြောဆိုနိုင်ပါတယ်ရှင်။ ✨"
        )
        await message.answer(text, parse_mode="Markdown")

# Goodbye (Member Leave)
@dp.message(F.left_chat_member)
async def goodbye_handler(message: types.Message):
    member = message.left_chat_member
    text = (
        f"👋 **Goodbye {member.full_name}!**\n\n"
        "နောက်တစ်ခါ ပြန်ဆုံကြမယ်လို့ မျှော်လင့်ပါတယ်ရှင်။"
    )
    await message.answer(text, parse_mode="Markdown")

async def main():
    keep_alive()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    

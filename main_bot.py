dp asyncio
import logging
import sys
import json
import os
import datetime
import pytz # Import pytz for timezone handling
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

# Set Myanmar Standard Time (MST) timezone
MYANMAR_TIMEZONE = pytz.timezone('Asia/Yangon')

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
    
    user_name = message.from_user.full_name
    
    welcome_text = (
        f"🌟 **{user_name} ရေ ကြိုဆိုပါတယ်ရှင့်!** 🌟\n\n"
        "ကျွန်မကတော့ သင့်ရဲ့ Group တွေကို အကောင်းဆုံး စောင့်ရှောက်ပေးမယ့် "
        "Auto Welcome/Goodbye Bot လေး ဖြစ်ပါတယ်ရှင့်။\n\n"
        "Add to Group ကို နှိပ်ပြီး အသုံးပြုနိုင်ပါတယ်ရှင့်။"
    )
    
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="➕ Add to Group", url="https://t.me/enr_welcome_bot?startgroup=true")
    )
    builder.row(
        types.InlineKeyboardButton(text="🆘 Support", url="https://t.me/ENRIQUE_FAMILY"),
        types.InlineKeyboardButton(text="👤 Owner", url="https://t.me/Official_Enr_Keno")
    )
    
    await message.answer(welcome_text, reply_markup=builder.as_markup(), parse_mode=ParseMode.MARKDOWN)

# COMMAND: /group
@dp.message(Command("group"))
async def command_group_handler(message: types.Message):
    # စာသားပုံစံ အမှားကင်းအောင် HTML Tags များဖြင့် ပြင်ဆင်ထားပါသည်
    text = "📢 <b>ကျွန်မတို့ရဲ့ Official Group ကို Join ရန် အောက်ပါ Link ကို နှိပ်ပါရှင် -</b>\n\n👉 https://t.me/ENRIQUE_FAMILY"
    
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="🌐 Join Group", url="https://t.me/ENRIQUE_FAMILY"))
    
    # parse_mode ကို ParseMode.HTML သို့ တိကျစွာ ပြောင်းလဲထားပါသည်
    await message.answer(text, reply_markup=builder.as_markup(), parse_mode=ParseMode.HTML)
    

# COMMAND: /broadcast
@dp.message(Command("broadcast"))
async def broadcast_handler(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ သင်သည် Broadcast ပို့ခွင့်ရှိသော Owner မဟုတ်ပါရှင်။")
        return
    
    command_args = message.text.split(maxsplit=1)
    if len(command_args) < 2:
        await message.answer("Example: `/broadcast Hello everyone!`")
        return
    
    text_to_send = command_args[1]
    chats = load_chats()
    count = 0
    for chat_id in chats:
        COMMANDMAND:
            await message.bot.send_message(chat_id, f"**📢 ANNOUNCEMENT**\n\n{text_to_send}", parse_mode=ParseMode.MARKDOWN)
            count += 1
            await asyncio.sleep(0.05) # Avoid flood limit
        except Exception as e:
            logging.error(f"Failed to send broadcast to {chat_id}: {e}")
            pass
    await message.answer(f"✅ Broadcast ပို့ပြီးပါပြီ။ စုစုပေါင်း: {count} နေရာ")

# EVENT: Bot added to group or promoted/demoted
@dp.my_chat_member()
async def bot_member_status_handler(event: types.ChatMemberUpdated):
    bot_id = (await event.bot.get_me()).id
    
    # Bot added to group
    if event.new_chat_member.status == "member" and event.new_chat_member.user.id == bot_id:
        save_chat(event.chat.id)
        text = (
            "မဂ်လာပါရှင့် အသုံးပြုဖို့ Admin အရင် ပေးပါ\n\n"
            "သင့် Group တွင် Welcome/Goodbye အတွက် auto အလုပ်လုပ်ပေးသွားမှာဖြစ်ပါတယ်ရှင်"
        )
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(text="🆘 Support", url="https://t.me/ENRIQUE_FAMILY"))
        await event.bot.send_message(event.chat.id, text, reply_markup=builder.as_markup(), parse_mode=ParseMode.MARKDOWN)
    
    # Bot promoted to administrator
    elif event.new_chat_member.status == "administrator" and event.new_chat_member.user.id == bot_id:
        text = "🤖 **Bot System စတင်အလုပ်လုပ်နေပါပြီ**"
        await event.bot.send_message(event.chat.id, text, parse_mode=ParseMode.MARKDOWN)

# EVENT: NEW MEMBER JOINED
@dp.message(F.new_chat_members)
async def on_user_joined(message: types.Message):
    save_chat(message.chat.id)
    
    # Check if the bot itself was added (handled by bot_member_status_handler)
    bot_id = (await message.bot.get_me()).id
    is_bot_added = any(member.id == bot_id for member in message.new_chat_members)
    
    if not is_bot_added:
        for user in message.new_chat_members:
            # Get current time in Myanmar timezone
            now_utc = datetime.datetime.now(pytz.utc)
            now_myanmar = now_utc.astimezone(MYANMAR_TIMEZONE)
            current_time = now_myanmar.strftime("%I:%M %p") # e.g., 09:30 PM
            current_date = now_myanmar.strftime("%d/%m/%Y") # e.g., 22/06/2026
            
            group_name = message.chat.title if message.chat.title else "Group"
            
            welcome_msg = (
                f"🌟 **{user.full_name} ရေ {group_name} မှ ကြိုဆိုပါတယ်ရှင့်!** 🌟\n\n"
                f"**Username:** @{user.username if user.username else 'N/A'}\n"
                f"**ID:** `{user.id}`\n"
                f"**Time:** `{current_time}`\n"
                f"**Date:** `{current_date}`\n\n"
                "💖 ရည်းစားလည်းဝင်ရှာ၊ စကားလည်းပြောရင်း၊ လူလေးရှိရင် ထည့်ကူပေးလို့ရပါတယ်နော်! 💖\n\n"
                "ပျော်ရွှင်စွာ စကားပြောဆိုနိုင်ပါတယ်ရှင့်။ ✨"
            )
            await message.answer(welcome_msg, parse_mode=ParseMode.MARKDOWN)

# EVENT: MEMBER LEFT
@dp.message(F.left_chat_member)
async def on_user_left(message: types.Message):
    user = message.left_chat_member
    goodbye_msg = (
        f"👋 **{user.full_name}** က Group ကနေ ထွက်သွားပါပြီ။\n\n"
        "နောက်တစ်ခါ ပြန်ဆုံကြမယ်လို့ မျှော်လင့်ပါတယ်ရှင်။ ✨"
    )
    await message.answer(goodbye_msg, parse_mode=ParseMode.MARKDOWN)

async def main() -> None:
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    print("Bot is starting...")
    await dp.start_polling(bot)

app = bot

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    keep_alive()  # Start Web Server for Render
    asyncio.run(main())
    

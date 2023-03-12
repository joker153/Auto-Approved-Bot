from os import environ
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, User, ChatJoinRequest
from pymongo import MongoClient

# Set up MongoDB connection
MONGO_URL = environ.get("MONGO_URL")
if MONGO_URL:
    db_client = MongoClient(MONGO_URL)
    db = db_client["AutoApproved"]
    approved_col = db["approved_users"]
else:
    approved_col = None

# Set up Pyrogram client
pr0fess0r_99 = Client(
    "Auto Approved Bot",
    bot_token=environ["BOT_TOKEN"],
    api_id=int(environ["API_ID"]),
    api_hash=environ["API_HASH"]
)

# Get broadcast and log channels
BROADCAST_ID = environ.get("BROADCAST_ID")
LOG_CHANNEL_ID = environ.get("LOG_CHANNEL_ID")

# Get approved welcome text and setting
TEXT = environ.get("APPROVED_WELCOME_TEXT", "Hello {mention}\nWelcome To {title}\n\nYou have been Auto-Approved.")
APPROVED = environ.get("APPROVED_WELCOME", "on").lower()

# Define function to send log message
async def log_message(text):
    if LOG_CHANNEL_ID:
        await pr0fess0r_99.send_message(chat_id=LOG_CHANNEL_ID, text=text)

# Define function to broadcast message
async def broadcast_message(text):
    if BROADCAST_ID:
        await pr0fess0r_99.send_message(chat_id=BROADCAST_ID, text=text)

@pr0fess0r_99.on_message(filters.private & filters.command(["start"]))
async def start(client: pr0fess0r_99, message: Message):
    approvedbot = await client.get_me() 
    button = [[ InlineKeyboardButton("📦 Repo", url="https://github.com/PR0FESS0R-99/Auto-Approved-Bot"), InlineKeyboardButton("Updates 📢", url="t.me/Mo_Tech_YT") ],
              [ InlineKeyboardButton("➕️ Add Me To Your Chat ➕️", url=f"http://t.me/{approvedbot.username}?startgroup=botstart") ]]
    await client.send_message(chat_id=message.chat.id, text=f"**__Hello {message.from_user.mention} I am Auto Approver Join Request Bot Just [Add Me To Your Group Channel](http://t.me/{approvedbot.username}?startgroup=botstart) || Repo https://github.com/PR0FESS0R-99/Auto-Approved-Bot||**__", reply_markup=InlineKeyboardMarkup(button), disable_web_page_preview=True)

@pr0fess0r_99.on_chat_join_request(filters.group | filters.channel)
async def autoapprove(client: pr0fess0r_99, message: ChatJoinRequest):
    chat = message.chat # Chat
    user = message.from_user # User
    await client.approve_chat_join_request(chat_id=chat.id, user_id=user.id)
    if approved_col:
        approved_col.insert_one({"user_id": user.id, "chat_id": chat.id})
    if APPROVED == "on":
        welcome_text = TEXT.format(mention=user.mention, title=chat.title)
        await client.send_message(chat_id=user.id, text=welcome_text)
        await log_message(f"Auto-approved {user.mention} to {chat.title}")
    await broadcast_message(f"{user.mention} joined {chat.title}")

print("Auto Approved Bot")
pr0fess0r

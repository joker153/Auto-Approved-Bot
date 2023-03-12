from os import environ
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, User, ChatJoinRequest
from pymongo import MongoClient

# Mongo DB details
DATABASE_NAME = environ["DATABASE_NAME"]
DATABASE_URI = environ["DATABASE_URI"]
mongo_client = MongoClient(DATABASE_URI)
mongo_db = mongo_client[DATABASE_NAME]

# Log channel
LOG_CHANNEL = environ.get("LOG_CHANNEL")

pr0fess0r_99 = Client(
    "Auto Approved Bot",
    bot_token=environ["BOT_TOKEN"],
    api_id=int(environ["API_ID"]),
    api_hash=environ["API_HASH"],
)

APPROVED = environ.get("APPROVED_WELCOME", "on").lower()
WELCOME_TEXT = environ.get("APPROVED_WELCOME_TEXT", "Hello {mention}\nWelcome To {title}\n\nYour Auto Approved")
JOIN_CHANNEL_TEXT = environ.get("JOIN_CHANNEL_TEXT", "Join Our Movie Channel")
JOIN_CHANNEL_LINK = environ.get("JOIN_CHANNEL_LINK")
PIC = environ.get("PIC")

# Function to get the number of bot users
def get_users_count():
    try:
        return mongo_db["users"].count_documents({})
    except:
        return 0

# Function to get the number of blocked users
def get_blocked_users_count():
    try:
        return mongo_db["blocked_users"].count_documents({})
    except:
        return 0

# Function to get the number of successful broadcasts
def get_broadcast_success_count():
    try:
        return mongo_db["broadcasts"].count_documents({})
    except:
        return 0

@pr0fess0r_99.on_message(filters.private & filters.command(["start"]))
async def start(client: pr0fess0r_99, message: Message):
    approvedbot = await client.get_me() 
    button = [[ InlineKeyboardButton("➕️ Add Me To Your Chat ➕️", url=f"http://t.me/{approvedbot.username}?startgroup=botstart") ]]
    await client.send_photo(
        chat_id=message.chat.id,
        photo=PIC,
        caption=f"**__Hello {message.from_user.mention} ɪ ᴀᴍ ᴀɴ ᴀᴜᴛᴏ ᴀᴘᴘʀᴏᴠᴇʀ ᴊᴏɪɴ ʀᴇQᴜᴇꜱᴛ ʙᴏᴛ \n\n ɪ ᴄᴀɴ ᴀᴘᴘʀᴏᴠᴇ ᴜꜱᴇʀꜱ ɪɴ ɢʀᴏᴜᴘꜱ/ᴄʜᴀɴɴᴇʟꜱ.ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀᴛ ᴀɴᴅ ᴘʀᴏᴍᴏᴛᴇ ᴍᴇ ᴛᴏ ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴀᴅᴅ ᴍᴇᴍʙᴇʀꜱ ᴘᴇʀᴍɪꜱꜱɪᴏɴ.",
        reply_markup=InlineKeyboardMarkup(button),
        disable_web_page_preview=True
    )
    # Save user in the database
    mongo_db["users"].insert_one({"user_id": message.from_user.id})

@pr0fess0r_99.on_chat_join_request(filters.group | filters.channel)
async def autoapprove(client: pr0fess0r_99, message: ChatJoinRequest):
    chat = message.chat
    user = message.from_user
    print(f"{user.first_name} Joined 🤝") # Logs
    await client.approve_chat_join_request(chat_id=chat.id, user_id=user.id)
    if APPROVED == "on":
        welcome_text = WELCOME_TEXT.format(mention=user.mention, title=chat.title)
        button = None
        if JOIN_CHANNEL_LINK:
            button = InlineKeyboardMarkup([[InlineKeyboardButton(JOIN_CHANNEL_TEXT, url=JOIN_CHANNEL_LINK)]])
        await client.send_message(chat_id=user.id, text=welcome_text, reply_markup=button)

@pr0fess0r_99.on_message(filters.private & filters.command(["broadcast"]))
async def broadcast(client: pr0fess0r_99, message: Message):
    if len(message.text.split()) == 1:
        await message.reply_text("Please specify a message to broadcast.")
        return

    text = message.text.split(None, 1)[1]
    users_count = get_users_count()
    blocked_users_count = get_blocked_users_count()
    broadcast_success_count = get_broadcast_success_count()


print("Auto Approved Bot")
pr0fess0r_99.run()

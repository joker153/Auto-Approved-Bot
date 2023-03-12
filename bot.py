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
LOG_CHANNEL = environ["LOG_CHANNEL"]

pr0fess0r_99 = Client(
    "Auto Approved Bot",
    bot_token=environ["BOT_TOKEN"],
    api_id=int(environ["API_ID"]),
    api_hash=environ["API_HASH"],
)

APPROVED = environ.get("APPROVED_WELCOME", "on").lower()
TEXT = environ.get("APPROVED_WELCOME_TEXT", "Hello {mention}\nWelcome To {title}\n\nYour Auto Approved")

@pr0fess0r_99.on_message(filters.private & filters.command(["start"]))
async def start(client: pr0fess0r_99, message: Message):
    approvedbot = await client.get_me() 
    button = [[ InlineKeyboardButton("➕️ Add Me To Your Chat ➕️", url=f"http://t.me/{approvedbot.username}?startgroup=botstart") ]]
    await client.send_message(
        chat_id=message.chat.id,
        text=f"**__Hello {message.from_user.mention} I am an Auto Approver Join Request Bot. Just [Add Me To Your Group or Channel](http://t.me/{approvedbot.username}?startgroup=botstart).__**",
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
        await client.send_message(chat_id=user.id, text=TEXT.format(mention=user.mention, title=chat.title))
    # Send log message to log channel
    await client.send_message(chat_id=LOG_CHANNEL, text=f"{user.mention} joined {chat.title}")

@pr0fess0r_99.on_message(filters.command(["broadcast"]) & filters.user(list(int(x) for x in environ.get("ADMIN_IDS", "").split())))
async def broadcast(client: pr0fess0r_99, message: Message):
    all_users = mongo_db["users"].find()
    for user in all_users:
        try:
            await client.send_message(chat_id=user["user_id"], text=message.text.split("/broadcast ", maxsplit=1)[1])
        except Exception as e:
            print(e)
    await message.reply_text("Broadcast completed!")

print("Auto Approved Bot")
pr0fess0r_99.run()

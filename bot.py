from os import environ
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, User, ChatJoinRequest

pr0fess0r_99=Client(
    "Auto Approved Bot",
    bot_token=environ["BOT_TOKEN"],
    api_id=int(environ["API_ID"]),
    api_hash=environ["API_HASH"]
)

TEXT = environ.get("APPROVED_WELCOME_TEXT", "Hello {mention}\nWelcome To {title}\n\nYour Auto Approved")
APPROVED = environ.get("APPROVED_WELCOME", "on").lower()

@pr0fess0r_99.on_message(filters.private & filters.command(["start"]))
async def start(client: pr0fess0r_99, message: Message):
    approvedbot = await client.get_me() 
    button = [[ InlineKeyboardButton("📦 Repo", url="https://github.com/PR0FESS0R-99/Auto-Approved-Bot"), InlineKeyboardButton("Updates 📢", url="t.me/Mo_Tech_YT") ],
              [ InlineKeyboardButton("➕️ Add Me To Your Chat ➕️", url=f"http://t.me/{approvedbot.username}?startgroup=botstart") ]]
    await client.send_message(chat_id=message.chat.id, text=f"**__Hello {message.from_user.mention} I am an Auto Approver Join Request Bot. Just [add me to your group/channel](http://t.me/{approvedbot.username}?startgroup=botstart) || Repo https://github.com/PR0FESS0R-99/Auto-Approved-Bot ||**__", reply_markup=InlineKeyboardMarkup(button), disable_web_page_preview=True)

@pr0fess0r_99.on_chat_join_request(filters.group | filters.channel)
async def autoapprove(client: pr0fess0r_99, message: ChatJoinRequest):
    chat = message.chat
    user = message.from_user
    print(f"{user.first_name} joined {chat.title}")  # Logs
    await client.approve_chat_join_request(chat_id=chat.id, user_id=user.id)
    if APPROVED == "on":
        await client.send_message(chat_id=chat.id, text=TEXT.format(mention=user.mention, title=chat.title))

print("Auto Approved Bot")
pr0fess0r_99.run()

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import random
import os

players = []
roles = ['مافیا', 'شهروند', 'دکتر', 'کارآگاه']

def start(update: Update, context: CallbackContext):
    players.clear()
    update.message.reply_text("🎮 بازی مافیا شروع شد! برای ورود، /join بزنید.")

def join(update: Update, context: CallbackContext):
    user = update.effective_user
    if user.id not in [p['id'] for p in players]:
        players.append({'id': user.id, 'name': user.full_name})
        update.message.reply_text(f"{user.full_name} به بازی اضافه شد ✅")
    else:
        update.message.reply_text("شما قبلاً وارد بازی شدید.")

def assign(update: Update, context: CallbackContext):
    if len(players) < 4:
        update.message.reply_text("❗️حداقل ۴ بازیکن نیاز داریم.")
        return

    random.shuffle(players)
    selected_roles = roles + ['شهروند'] * (len(players) - len(roles))
    random.shuffle(selected_roles)

    for i, player in enumerate(players):
        context.bot.send_message(chat_id=player['id'], text=f"نقش شما: {selected_roles[i]} 🎭")

    update.message.reply_text("🎲 نقش‌ها ارسال شدند. بازی شروع شد!")

def main():
    token = os.environ.get("BOT_TOKEN")
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("startmafia", start))
    dp.add_handler(CommandHandler("join", join))
    dp.add_handler(CommandHandler("assign", assign))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

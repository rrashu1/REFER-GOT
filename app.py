import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from referral import do_referral_start
from wallet import handle_withdraw, show_wallet
from db import init_db, get_user, session
from dotenv import load_dotenv

load_dotenv()

def start(update: Update, ctx: CallbackContext):
    do_referral_start(update, ctx)

def wallet(update: Update, ctx: CallbackContext):
    show_wallet(update, ctx)

def withdraw(update: Update, ctx: CallbackContext):
    handle_withdraw(update, ctx)

def text_handler(update: Update, ctx: CallbackContext):
    if ctx.user_data.get('awaiting_bkash'):
        number = update.message.text
        ctx.user_data['awaiting_bkash'] = False
        user = get_user(update.effective_user.id)
        user.balance_usdt -= 0.5
        session.commit()
        update.message.reply_text(f"✅ তোমার উইথড্র রিকুয়েস্ট রেকর্ড হয়েছে:\n📞 bKash: {number}\n💵 Amount: $0.50\n⏳ ২৪ ঘন্টার মধ্যে প্রক্রিয়া করা হবে।")

if __name__ == '__main__':
    init_db()
    updater = Updater(os.getenv("BOT_TOKEN"), use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("wallet", wallet))
    dp.add_handler(CommandHandler("withdraw", withdraw))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, text_handler))
    updater.start_polling()
    updater.idle()

from db import get_user

def show_wallet(update, ctx):
    user = get_user(update.effective_user.id)
    update.message.reply_text(f"💰 Balance: ${user.balance_usdt:.2f} USDT")

def handle_withdraw(update, ctx):
    user = get_user(update.effective_user.id)
    if user.balance_usdt < 0.5:
        update.message.reply_text("❌ কমপক্ষে $0.50 হলে তবেই উইথড্র করতে পারবে।")
        return
    ctx.user_data['awaiting_bkash'] = True
    update.message.reply_text("📲 তোমার bKash নাম্বার পাঠাও যেখানে টাকা নিবে।")

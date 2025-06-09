from db import get_or_create_user, get_user_by_ref_code, update_balances

def do_referral_start(update, ctx):
    user = get_or_create_user(update.effective_user.id)
    if ctx.args:
        ref_code = ctx.args[0]
        referrer = get_user_by_ref_code(ref_code)
        if referrer and referrer.telegram_id != user.telegram_id:
            update_balances(user, referrer)
            update.message.reply_text("🎉 You and your referrer both got $0.01 USDT!")
        else:
            update.message.reply_text("Welcome back!")
    else:
        update.message.reply_text("Welcome to the bot! Share your referral link!")

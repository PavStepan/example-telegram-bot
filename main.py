from telegram import Update, MenuButtonWebApp, WebAppInfo
from telegram.ext import ContextTypes, Application, CommandHandler
from config import get_web_url, get_bot_token
from database import add_userdata_in_db, add_gift_link, add_referral_link
from utils import update_to_user, update_to_settings


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with a button that opens a web app."""
    web_menu = MenuButtonWebApp(text="some text",
                                web_app=WebAppInfo(
                                    url=web_url + "/?user_id={}/".format(
                                        update.effective_message.chat_id)))
    await context.bot.setChatMenuButton(chat_id=update.effective_message.chat_id, menu_button=web_menu)
    caption = "some caption"
    await context.bot.send_video(chat_id=update.effective_message.chat_id,
                                 video=open(base_path + "intro.MP4", 'rb'),
                                 caption=caption)

    user_data = update_to_user(update)
    settings_data = update_to_settings(update)

    add_userdata_in_db(user_data, 'Users')
    add_userdata_in_db(settings_data, 'Settings')

    if len(context.args) > 0:
        if context.args[0].startswith("gift_"):
            giver_id = context.args[0].split('_')[1]
            add_gift_link(update.message.chat['id'], giver_id)
        else:
            add_referral_link(update.message.chat['id'], context.args[0])


def main(bot_token) -> None:
    application = Application.builder().token(bot_token).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    base_path = ''
    web_url = get_web_url()
    token = get_bot_token()
    main(token)

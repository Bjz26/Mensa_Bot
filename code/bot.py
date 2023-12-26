from meal_plan import get_vegan_meals_for_date
from database_manager import add_subscriber, remove_subscriber, create_subsciber_table, get_all_subscribers
import logging
from datetime import date, timedelta
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import holidays


bot_token = 'Your_API_KEY'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def log_info(update, function_name):
    logging.info(f'u_intx: {update.effective_chat.first_name + " (" + update.effective_chat.username+")"} ({update.effective_chat.id}) has called the function {function_name}.')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hallo, Willkommen bei VegaLea, dem veganen Mensabot für die Leipziger Uni-Mensen. Schön, dass du da bist 👋 \nSchreibe /help, um zu erfahren, was dieser Bot kann.")
    await log_info(update, 'start')

async def get_meal_plan_today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=get_vegan_meals_for_date(date.today()))
    await log_info(update, 'get_meal_plan_today')

async def daily_subscription_activate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = add_subscriber(update.effective_chat.id)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    await log_info(update, 'daily_subscription_activate')

async def daily_subscription_deactivate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = remove_subscriber(update.effective_chat.id)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    await log_info(update, 'daily_subscription_deactivate')

async def get_meal_plan_tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=get_vegan_meals_for_date(date.today() + timedelta(days=1)))
    await log_info(update, 'get_meal_plan_tomorrow')

async def get_help_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hallo, ich bin der Mensa Bot VegaLea 👨‍🍳 \nSchreibe /meal_plan_today, um alle veganen Hauptgerichte für heute zu erhalten.\nSchreibe /meal_plan_tomorrow, um alle veganen Hauptgerichte für morgen zu erhalten.\nMit /activate_subscription kannst du den täglichen Plan aktivieren und mit /deactivate_subscription kannst du dich wieder abmelden.")
    await log_info(update, 'get_help_message')

async def send_daily_message(context: ContextTypes.DEFAULT_TYPE):
    today = date.today()
    if today == 6 or today in holidays.Germany():
        logging.info(f'Daily message wasn\'t sent to {len(get_all_subscribers())} subscribers. It\'s Sunday or a holiday.')
    for user in get_all_subscribers():
        await context.bot.send_message(chat_id=user, text=get_vegan_meals_for_date(date.today()))
    logging.info(f'Daily message sent at {len(get_all_subscribers())} subscirbers.')



if __name__ == '__main__':
    application = ApplicationBuilder().token(bot_token).build()
    create_subsciber_table()
    
    start_handler = CommandHandler('start', start)
    meal_plan_handler_today = CommandHandler('meal_plan_today', get_meal_plan_today)
    meal_plan_handler_tomorrow = CommandHandler('meal_plan_tomorrow', get_meal_plan_tomorrow)
    activate_subscription_handler = CommandHandler('activate_subscription', daily_subscription_activate)
    deactivate_subscription_handler = CommandHandler('deactivate_subscription', daily_subscription_deactivate)
    help_handler = CommandHandler('help', get_help_message)


    application.add_handler(start_handler)
    application.add_handler(meal_plan_handler_today)
    application.add_handler(meal_plan_handler_tomorrow)
    application.add_handler(activate_subscription_handler)
    application.add_handler(deactivate_subscription_handler)
    application.add_handler(help_handler)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_daily_message, "cron", hour=8, minute=0, args=[application])
    scheduler.start()

    application.run_polling()
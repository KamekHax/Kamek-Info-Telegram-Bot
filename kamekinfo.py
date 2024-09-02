from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import logging
import sys
import os
import requests
import json

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot token (replace with your actual bot token before using)
BOT_TOKEN = "[Your-Token-Here]"

# API keys for IP geolocation and weather (replace with your actual API keys)
GEO_API_KEY = "[Your-Geo-API-Key-Here]"
WEATHER_API_KEY = "[Your-Weather-API-Key-Here]"

# Define a list of developer IDs (replace with your actual developer IDs)
DEVELOPERS = [000000000]  # Example: 6326042865

# Function to check if the user is a developer
def is_developer(user_id):
    return user_id in DEVELOPERS

# Define command handlers
async def start(update: Update, context: CallbackContext) -> None:
    try:
        await update.message.reply_text('Hello! I am your bot. How can I assist you today?')
    except Exception as e:
        logger.error(f"Error in start command: {e}")

async def help_command(update: Update, context: CallbackContext) -> None:
    try:
        help_text = (
            "start - Start the bot\n"
            "help - Get a list of commands\n"
            "info - Get bot information\n"
            "checkdev - Check if you are a developer\n"
            "shutdown - Shut down the bot (for developers only)\n"
            "restart - Restart the bot (for developers only)\n"
            "weather - Get the current weather (requires an API key)\n"
            "ipcheck - Check your IP, WiFi connection, and location\n"
            "version - Get the bot version\n"
            "userinfo - Get information about your user profile\n"
            "copyright - Get copyright information\n"
            "set_language - Set the bot language\n"
            "share - Share the bot with others"
        )
        await update.message.reply_text(help_text)
    except Exception as e:
        logger.error(f"Error in help command: {e}")

async def info(update: Update, context: CallbackContext) -> None:
    try:
        await update.message.reply_text("Kamek AI - Created by **HomelanderOG on Twitter**")
    except Exception as e:
        logger.error(f"Error in info command: {e}")

async def checkdev(update: Update, context: CallbackContext) -> None:
    try:
        user_id = update.message.from_user.id
        if is_developer(user_id):
            await update.message.reply_text("You are a registered developer.")
        else:
            await update.message.reply_text("You are not a registered developer.")
    except Exception as e:
        logger.error(f"Error in checkdev command: {e}")

async def shutdown(update: Update, context: CallbackContext) -> None:
    try:
        user_id = update.message.from_user.id
        if is_developer(user_id):
            await update.message.reply_text("Shutting down the bot...")
            os.kill(os.getpid(), 9)
        else:
            await update.message.reply_text("You are not authorized to use this command.")
    except Exception as e:
        logger.error(f"Error in shutdown command: {e}")

async def restart(update: Update, context: CallbackContext) -> None:
    try:
        user_id = update.message.from_user.id
        if is_developer(user_id):
            await update.message.reply_text("Restarting the bot...")
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            await update.message.reply_text("You are not authorized to use this command.")
    except Exception as e:
        logger.error(f"Error in restart command: {e}")

async def weather(update: Update, context: CallbackContext) -> None:
    try:
        ip_info = requests.get(f"http://ipinfo.io/json?token={GEO_API_KEY}").json()
        city = ip_info.get("city")
        region = ip_info.get("region")
        country = ip_info.get("country")
        if city and region and country:
            weather_info = requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={city},{region},{country}&appid={WEATHER_API_KEY}&units=metric"
            ).json()
            weather_desc = weather_info["weather"][0]["description"]
            temp = weather_info["main"]["temp"]
            await update.message.reply_text(f"Weather in {city}, {region}, {country}: {weather_desc}, {temp}°C")
        else:
            await update.message.reply_text("Weather: Unable to fetch location data.")
    except Exception as e:
        logger.error(f"Error in weather command: {e}")
        await update.message.reply_text("Weather: Unable to fetch weather data.")

async def ipcheck(update: Update, context: CallbackContext) -> None:
    try:
        ip_info = requests.get(f"http://ipinfo.io/json?token={GEO_API_KEY}").json()
        ip = ip_info.get("ip", "Unknown")
        city = ip_info.get("city", "Unknown")
        region = ip_info.get("region", "Unknown")
        country = ip_info.get("country", "Unknown")
        wifi_info = f"IP: {ip}\nLocation: {city}, {region}, {country}"
        await update.message.reply_text(wifi_info)
    except Exception as e:
        logger.error(f"Error in ipcheck command: {e}")
        await update.message.reply_text("IP Check: Unable to fetch IP and location data.")

async def version(update: Update, context: CallbackContext) -> None:
    try:
        await update.message.reply_text("Kamek AI - Version 1.5r")
    except Exception as e:
        logger.error(f"Error in version command: {e}")

async def userinfo(update: Update, context: CallbackContext) -> None:
    try:
        user = update.message.from_user
        user_info = (
            f"User ID: {user.id}\n"
            f"Username: {user.username}\n"
            f"First Name: {user.first_name}\n"
            f"Last Name: {user.last_name}\n"
        )
        await update.message.reply_text(user_info)
    except Exception as e:
        logger.error(f"Error in userinfo command: {e}")

async def copyright_command(update: Update, context: CallbackContext) -> None:
    try:
        await update.message.reply_text(
            "© Monday September 2nd 2024 - Owned by **HomelanderOG on Twitter**"
        )
    except Exception as e:
        logger.error(f"Error in copyright command: {e}")

async def set_language(update: Update, context: CallbackContext) -> None:
    try:
        # Implement language setting logic here
        await update.message.reply_text("Language setting command executed.")
    except Exception as e:
        logger.error(f"Error in set_language command: {e}")

async def share(update: Update, context: CallbackContext) -> None:
    try:
        share_text = (
            "Check out this amazing bot! "
            "You can start interacting with it using the following link: "
            f"https://t.me/{context.bot.username}"
        )
        await update.message.reply_text(share_text)
    except Exception as e:
        logger.error(f"Error in share command: {e}")

async def unknown_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Sorry, I didn't recognize that command.")

# Main function to run the bot
def main():
    if any("telegram_bot.py" in proc for proc in os.popen("ps aux")):
        logger.warning("Another instance of the bot is running. Exiting.")
        return

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("checkdev", checkdev))
    application.add_handler(CommandHandler("shutdown", shutdown))
    application.add_handler(CommandHandler("restart", restart))
    application.add_handler(CommandHandler("weather", weather))
    application.add_handler(CommandHandler("ipcheck", ipcheck))
    application.add_handler(CommandHandler("version", version))
    application.add_handler(CommandHandler("userinfo", userinfo))
    application.add_handler(CommandHandler("copyright", copyright_command))
    application.add_handler(CommandHandler("set_language", set_language))
    application.add_handler(CommandHandler("share", share))
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()

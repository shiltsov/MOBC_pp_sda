from aiogram import Bot
from main.config_reader import config

bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")

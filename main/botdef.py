from aiogram import Bot, Dispatcher
from main.config_reader import config

bot = Bot(token=config.bot_token.get_secret_value(),  parse_mode="HTML")    
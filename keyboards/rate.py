from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

rates = ["1", "2", "3", "4", "5"]


def make_rating_kb() -> ReplyKeyboardMarkup:
    """
    Создаёт голосование
    """
    kb = ReplyKeyboardBuilder()
    for rate in rates:
        kb.button(text=rate)
    kb.adjust(len(rates))
    return kb.as_markup(resize_keyboard=True)

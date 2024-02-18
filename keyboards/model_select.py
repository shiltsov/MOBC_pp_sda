from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def make_model_kb() -> ReplyKeyboardMarkup:
    """
    Создаёт меню выбора модели
    """
    kb = ReplyKeyboardBuilder()
    kb.button(text="BOW")
    kb.button(text="TFIDF")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

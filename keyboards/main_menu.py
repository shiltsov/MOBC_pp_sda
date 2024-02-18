from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def make_main_menu() -> ReplyKeyboardMarkup:
    """
    Создаёт главное меню приложения (кнопки)
    """
    kb = ReplyKeyboardBuilder()
    kb.button(text="Определить авторство")
    kb.button(text="Голосовать")
    kb.button(text="О писателях")
    kb.button(text="О проекте")
    kb.adjust(1, 2, 1)
    return kb.as_markup(resize_keyboard=True)

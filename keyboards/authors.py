from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from handlers.utils import label2name


def make_authors_kb() -> ReplyKeyboardMarkup:
    """
    Создаёт главное меню приложения (кнопки)
    """
    names = list(label2name.values())

    kb = ReplyKeyboardBuilder()
    for name in names:
        kb.button(text=name)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

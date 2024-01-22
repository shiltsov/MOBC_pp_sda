from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.main_menu import make_main_menu
from aiogram.types import Message, ReplyKeyboardRemove

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(f"""
Приветствую {message.from_user.full_name}!                         
<b>Добро пожаловать в бот определения авторства текста</b>.
Вы в главном меню. Выберите, что хотите сделать
""", reply_markup=make_main_menu())
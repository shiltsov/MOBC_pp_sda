import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile

from keyboards.authors import make_authors_kb
from keyboards.main_menu import make_main_menu
from handlers.utils import label2name, writers

names = list(label2name.values())


class ChooseAuthor(StatesGroup):
    choosing_author = State()


router = Router()


@router.message(StateFilter(None), F.text.in_("О писателях"))
async def cmd_choose_author(message: Message, state: FSMContext):
    await message.answer(text="Выберите писателя:", reply_markup=make_authors_kb())
    await state.set_state(ChooseAuthor.choosing_author)


@router.message(ChooseAuthor.choosing_author, F.text.in_(names))
async def show_author_info(message: Message, state: FSMContext):
    logging.info(f"show_author_info: {message.from_user.full_name}")

    image_from_pc = FSInputFile(f"images/{writers[message.text][0]}")
    await message.answer_photo(image_from_pc)
    await message.answer(
        text=str(writers[message.text][1])
        + "\n\n<b>Для продолжения нажмите нужную кнопку</b>",
        reply_markup=make_main_menu(),
    )
    await state.clear()


# если сделан неверный выбор - остаемся на месте
@router.message(ChooseAuthor.choosing_author)
async def show_author_error(message: Message, state: FSMContext):
    # заносим в стейт какую модель выбрал
    await message.answer(text="Неверный выбор автора", reply_markup=make_authors_kb())
    await state.set_state(ChooseAuthor.choosing_author)

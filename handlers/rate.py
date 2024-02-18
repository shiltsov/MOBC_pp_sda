import logging
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from keyboards.rate import make_rating_kb
from keyboards.main_menu import make_main_menu


class Rate(StatesGroup):
    choosing_rating = State()


router = Router()
votes = [5]


# показать кнопки голосования
@router.message(StateFilter(None), F.text.in_("Голосовать"))
async def cmd_rate(message: Message, state: FSMContext):
    await message.answer(text="Оцените работу бота:", reply_markup=make_rating_kb())
    await state.set_state(Rate.choosing_rating)


@router.message(Rate.choosing_rating, F.text)
async def show_rating_info(message: Message, state: FSMContext):
    logging.info(f"show_rating_info: {message.from_user.full_name}")

    if message.text in ["1", "2", "3", "4", "5"]:
        vote = int(message.text)
        votes.append(vote)
        rank = sum(votes) / len(votes)
        await message.answer(
            f"""
Ваша оценка: {vote}
Всего голосований: {len(votes)}
Средняя оценка: {rank:.2f}

<b>Для продолжения нажмите нужную кнопку</b>
    """,
            reply_markup=make_main_menu(),
        )
    else:
        rank = sum(votes) / len(votes)
        await message.answer(
            f"""
Ваш голос не засчитан
Всего голосований: {len(votes)}
Средняя оценка: {rank:.2f}

<b>Для продолжения нажмите нужную кнопку</b>
    """,
            reply_markup=make_main_menu(),
        )
    await state.clear()

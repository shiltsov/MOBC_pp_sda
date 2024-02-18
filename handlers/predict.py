import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.model_select import make_model_kb
from keyboards.main_menu import make_main_menu
from aiogram.utils.formatting import Bold, as_list, as_marked_section
from aiogram.types import ContentType
from handlers.utils import infer_one
from main.botdef import bot

names = ["BOW", "TFIDF"]


class ChooseMethod(StatesGroup):
    choosing_method = State()
    waiting_data = State()


router = Router()


# начало работы КА - выбор модели
@router.message(StateFilter(None), F.text.in_("Определить авторство"))
async def cmd_choose_method(message: Message, state: FSMContext):
    await message.answer(text="Выберите модель:", reply_markup=make_model_kb())
    await state.set_state(ChooseMethod.choosing_method)


# второй шаг КА - модель выбрана, ждём текст или файл
@router.message(ChooseMethod.choosing_method, F.text.in_(names))
async def cmd_choose_method_stated(message: Message, state: FSMContext):
    # заносим в стейт какую модель выбрал
    await state.update_data(choosen_model=0 if message.text == "BOW" else 1)
    await message.answer(
        text="Отправьте текст или приложите текстовый файл:",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(ChooseMethod.waiting_data)


# если сделан неверный выбор - остаемся на месте
@router.message(
    ChooseMethod.choosing_method,
)
async def cmd_choose_method_error(message: Message, state: FSMContext):
    # заносим в стейт какую модель выбрал
    await state.update_data(choosen_model=0 if message.text == "BOW" else 1)
    await message.answer(text="Неверный выбор модели", reply_markup=make_model_kb())
    await state.set_state(ChooseMethod.choosing_method)


# третий (финальный) шаг КА - получили текст, запредиктили и выдаем главное меню. Обнуляем состояние
@router.message(ChooseMethod.waiting_data, F.text)
async def show_predict(message: Message, state: FSMContext):

    logging.info(f"show_predict: {message.from_user.full_name}")

    user_data = await state.get_data()
    res = infer_one(message.text, model=user_data.get("choosen_model", 0))

    strArr = ["Я не считаю что это:"]
    for author, score in res[1:]:
        strArr.append(author + " (" + f"{score:.4f}" + ")")

    model_name = "BOW" if user_data.get("choosen_model", 0) == 0 else "TFIDF"

    content = as_list(
        as_marked_section(
            Bold(f"{model_name}: я считаю что это:"),
            res[0][0] + " (" + f"{res[0][1]:0.4f}" + ")",
            marker="✅ ",
        ),
        as_marked_section(
            *strArr,
            marker="❌ ",
        ),
        sep="\n\n",
    )
    await state.clear()
    await message.reply(**content.as_kwargs(), reply_markup=make_main_menu())


# если отправили не текст а текстовый файл (проверок не делаем)
@router.message(
    ChooseMethod.waiting_data,
)
async def show_predict_file(
    message: Message, state: FSMContext, content_types=ContentType.DOCUMENT
):

    # считываем присланный файл
    logging.info(f"show_predict_file: file received. {message.from_user.full_name}")

    # download user document
    buffer = await bot.download(message.document)
    string = buffer.read().decode("utf-8")

    user_data = await state.get_data()
    res = infer_one(string, model=user_data.get("choosen_model", 0))

    strArr = ["Я не считаю что это:"]
    for author, score in res[1:]:
        strArr.append(author + " (" + f"{score:.4f}" + ")")

    model_name = "BOW" if user_data.get("choosen_model", 0) == 0 else "TFIDF"

    content = as_list(
        as_marked_section(
            Bold(f"{model_name}: я считаю что это:"),
            res[0][0] + " (" + f"{res[0][1]:0.4f}" + ")",
            marker="✅ ",
        ),
        as_marked_section(
            *strArr,
            marker="❌ ",
        ),
        sep="\n\n",
    )
    await state.clear()
    await message.reply(**content.as_kwargs(), reply_markup=make_main_menu())

import logging
from aiogram import F, Router
from aiogram.filters import Command
from keyboards.main_menu import make_main_menu
from aiogram.types import Message

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    logging.info(f"cmd_start: {message.from_user.full_name}")

    await message.answer(
        f"Приветствую {message.from_user.full_name}!\n<b>Добро пожаловать в бот определения авторства текста</b>.Вы в главном меню. Выберите, что хотите сделать",
        reply_markup=make_main_menu(),
    )


@router.message(F.text.in_("О проекте"))
async def cmd_info(message: Message):
    logging.info(f"cmd_info: {message.from_user.full_name}")

    await message.answer(
        """
<b>Телеграм-бот определения авторства текстов.</b>

Автор: Дмитрий Шильцов (ВШЭ МОВС [a23])

<b>Что умеет бот:</b>

- <b>Определить авторство</b> (из 10 заранее заданных русских классиков) по заданному фрагменту текста
или текстовому файлу. Этот модуль реализован через FSM - есть промежуточный узел выбора модели.
Анализ производится не по словам а по частям речи и пунктуации, то есть части речи с учетом словаформы и знаки препинания
кодируются как "слова", далее полученное кодируется на выбор либо BOW либо TFIDF и скармливается соответствующей линейной модели.
После выбора модели можно либо скормить текст либо прикрепить текстовый файл (utf-8) и получить предикт.

- <b>Голосовать</b> - тут все стандартно. голосуем по 5 бальной шкале и видим статистику по голосованиям. Реализовал без премудростей,
можно конечно вести базу данных по голосам чтобы избежать повторное голосование и тп - но это за рамками учебной задачи.

- <b>О писателях</b> - краткая информация о писателях с фото - просто хотел научиться делать сообщения с файлами и меню со всякими кнопочками

<b>Резюме:</b> в целом все основные возможности библиотеки aiogram мною освоены (прием и передача файлов, задание поведения бота с помощью FSM,
интеграция ML модели с телеграм-ботом) + постарался все по-феншую разложить по модулям.

""",
        reply_markup=make_main_menu(),
    )


@router.message(F.text)
async def unknown_command(message: Message):
    logging.info(f"cmd_unknown: {message.from_user.full_name}")
    await message.answer(
        "Вы отправили незнакомую мне команду", reply_markup=make_main_menu()
    )

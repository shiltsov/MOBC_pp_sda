import pytest

from handlers.common import cmd_start, cmd_info, unknown_command

from aiogram_tests import MockedBot
from aiogram_tests.handler import MessageHandler
from aiogram_tests.types.dataset import MESSAGE
from aiogram.filters import Command


@pytest.mark.asyncio
async def test_cmd_start():
    requester = MockedBot(MessageHandler(cmd_start, Command(commands=["start"])))
    calls = await requester.query(message=MESSAGE.as_object(text="/start"))
    answer_message = calls.send_message.fetchone().text
    assert (
        answer_message
        == "Приветствую FirstName LastName!\n<b>Добро пожаловать в бот определения авторства текста</b>.Вы в главном меню. Выберите, что хотите сделать"
    )


@pytest.mark.asyncio
async def test_cmd_info():
    requester = MockedBot(MessageHandler(cmd_info))
    calls = await requester.query(message=MESSAGE.as_object(text="О проекте"))
    answer_message = calls.send_message.fetchone().text
    assert (
        answer_message
        == """
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

"""
    )


@pytest.mark.asyncio
async def test_unknown_command():
    requester = MockedBot(MessageHandler(unknown_command))
    calls = await requester.query(message=MESSAGE.as_object(text="/figpimi"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Вы отправили незнакомую мне команду"

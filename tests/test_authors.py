import pytest

from handlers.authors import cmd_choose_author, show_author_info, show_author_error
from handlers.authors import ChooseAuthor

from aiogram_tests import MockedBot
from aiogram_tests.handler import MessageHandler
from aiogram_tests.types.dataset import MESSAGE


@pytest.mark.asyncio
async def test_cmd_choose_author():
    requester = MockedBot(MessageHandler(cmd_choose_author, state=None))
    calls = await requester.query(message=MESSAGE.as_object(text="О писателях"))
    answer_message = calls.send_message.fetchone()
    assert answer_message.text == "Выберите писателя:"
    assert "keyboard" in answer_message.reply_markup


@pytest.mark.asyncio
async def test_show_author_info():
    requester = MockedBot(
        MessageHandler(show_author_info, state=ChooseAuthor.choosing_author)
    )
    calls = await requester.query(message=MESSAGE.as_object(text="И.Тургенев"))
    answer_message = calls.send_message.fetchone().text
    assert "Ива́н Серге́евич Турге́нев" in answer_message


@pytest.mark.asyncio
async def test_show_author_error():
    requester = MockedBot(
        MessageHandler(show_author_error, state=ChooseAuthor.choosing_author)
    )
    calls = await requester.query(message=MESSAGE.as_object(text="Карабамба"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Неверный выбор автора"

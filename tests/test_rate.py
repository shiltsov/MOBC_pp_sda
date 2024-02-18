import pytest

from handlers.rate import cmd_rate, show_rating_info, Rate


from aiogram_tests import MockedBot
from aiogram_tests.handler import MessageHandler
from aiogram_tests.types.dataset import MESSAGE


@pytest.mark.asyncio
async def test_cmd_rate():
    requester = MockedBot(MessageHandler(cmd_rate, state=None))
    calls = await requester.query(message=MESSAGE.as_object(text="Голосовать"))
    answer_message = calls.send_message.fetchone()
    assert answer_message.text == "Оцените работу бота:"
    assert "keyboard" in answer_message.reply_markup


@pytest.mark.asyncio
async def test_show_rating_info():
    requester = MockedBot(MessageHandler(show_rating_info, state=Rate.choosing_rating))
    calls = await requester.query(message=MESSAGE.as_object(text="5"))
    answer_message = calls.send_message.fetchone().text
    assert "Ваша оценка: 5" in answer_message
    assert "<b>Для продолжения нажмите нужную кнопку</b>" in answer_message
    calls = await requester.query(message=MESSAGE.as_object(text="10"))
    answer_message = calls.send_message.fetchone().text
    assert "Ваш голос не засчитан" in answer_message
    assert "<b>Для продолжения нажмите нужную кнопку</b>" in answer_message

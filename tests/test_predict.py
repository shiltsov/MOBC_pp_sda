import pytest
from unittest.mock import create_autospec, patch

from io import BytesIO

from handlers.predict import (
    cmd_choose_method,
    cmd_choose_method_stated,
    cmd_choose_method_error,
    show_predict,
    show_predict_file,
)
from handlers.predict import ChooseMethod

from aiogram_tests import MockedBot
from aiogram_tests.handler import MessageHandler
from aiogram_tests.types.dataset import MESSAGE, MESSAGE_WITH_DOCUMENT

from main.botdef import bot


# пропачим для того чтобы проверить работу с файлами
mock_download = create_autospec(
    bot.download,
    return_value=BytesIO("карабамба".encode('utf-8'))
)


@pytest.mark.asyncio
async def test_cmd_choose_method():
    requester = MockedBot(MessageHandler(cmd_choose_method, state=None))
    calls = await requester.query(
        message=MESSAGE.as_object(text="Определить авторство")
    )
    answer_message = calls.send_message.fetchone()
    assert answer_message.text == "Выберите модель:"
    assert "keyboard" in answer_message.reply_markup


@pytest.mark.asyncio
async def test_cmd_choose_method_stated():
    requester = MockedBot(
        MessageHandler(cmd_choose_method_stated, state=ChooseMethod.choosing_method)
    )
    calls = await requester.query(message=MESSAGE.as_object(text="BOW"))
    answer_message = calls.send_message.fetchone().text
    assert "Отправьте текст или приложите текстовый файл:" in answer_message

    calls = await requester.query(message=MESSAGE.as_object(text="TFIDF"))
    answer_message = calls.send_message.fetchone().text
    assert "Отправьте текст или приложите текстовый файл:" in answer_message


@pytest.mark.asyncio
async def test_cmd_choose_method_error():
    requester = MockedBot(
        MessageHandler(cmd_choose_method_error, state=ChooseMethod.choosing_method)
    )
    calls = await requester.query(message=MESSAGE.as_object(text="Boosting"))
    answer_message = calls.send_message.fetchone()
    assert "Неверный выбор модели" in answer_message.text
    assert "keyboard" in answer_message.reply_markup


@pytest.mark.asyncio
async def test_show_predict():
    requester = MockedBot(MessageHandler(show_predict, state=ChooseMethod.waiting_data))
    calls = await requester.query(message=MESSAGE.as_object(text="Карабамба"))
    answer_message = calls.send_message.fetchone().text
    assert "А.Чехов" in answer_message


@patch.object(bot, "download", mock_download, create=True)
@pytest.mark.asyncio
async def test_show_predict_file():
    requester = MockedBot(
        MessageHandler(show_predict_file, state=ChooseMethod.waiting_data)
    )
    calls = await requester.query(message=MESSAGE_WITH_DOCUMENT.as_object())
    answer_message = calls.send_message.fetchone().text
    assert "А.Чехов" in answer_message

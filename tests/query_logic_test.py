# import openai
import pytest
from unittest.mock import patch, MagicMock
# from pytest_mock import MockerFixture
# from conftest import MockedCompletion
from src.query_logic import Summarizer
from dotenv import load_dotenv
import os

from openai import OpenAI
from openai._exceptions import AuthenticationError, InternalServerError
# from openai import OpenAI


@pytest.fixture
def summarizer():
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    return Summarizer(config=api_key)


def test_gpt_query(summarizer):
    test_query = "Hello, this is a test"
    response = summarizer.gpt_query(test_query)
    assert response is not False


def test_gpt_query_auth_error(summarizer):
    test_query = "Hello, this is a test"
    # TODO: try mocking using this approach
    #  https://tobiaslang.medium.com/mocking-the-openai-api-in-python-a-step-by-step-guide-4630efcb809d
    # mocker.patch('openai.ChatCompletion.create', side_effect=AuthenticationError)
    # mocker.patch('openai.OpenAI', side_effect=AuthenticationError)
    summarizer.config = 'wrong_api_key'
    assert summarizer.gpt_query(test_query) is False
    assert "OpenAI could not validate your API key" in summarizer.warning


def test_gpt_query_error_retry(mocker, summarizer):
    mock_call = mocker.patch('openai.ChatCompletion.create', side_effect=Exception)
    # with patch('openai.ChatCompletion.create',
    #            side_effect=Exception) as mock_create:

    response = summarizer.gpt_query("Hello, this is a test")
    mock_open = str(mocker.patch('builtins.open'))
    result = summarizer.paragraph_summarize_query(transcript=test_transcript, gpt_prompt=mock_open)
    assert isinstance(result, str)

    assert mock_call.call_count == 6  # max_retries + 1
    assert response is False
    assert "problem with connecting to OpenAI API" in summarizer.warning


test_transcript = "This is a test" * 1000  # long enough to require chunking


def test_paragraph_summarize_query(mocker, summarizer):
    # with patch('openai.ChatCompletion.create') as mock_create, \
    #         patch('builtins.open', MagicMock(return_value=MagicMock(
    #             __enter__=lambda x: MagicMock(read=MagicMock(return_value="dummy prompt"))))):
    #     mock_create.return_value = MagicMock(choices=[MagicMock(message=MagicMock(content="Test summary"))])
    mock_open = str(mocker.patch('builtins.open'))
    result = summarizer.paragraph_summarize_query(transcript=test_transcript, gpt_prompt=mock_open)
    assert isinstance(result, str)


def test_paragraph_summarize_query_with_warning(summarizer):
    with patch('openai.ChatCompletion.create') as mock_create, \
            patch('builtins.open', MagicMock(return_value=MagicMock(
                __enter__=lambda x: MagicMock(read=MagicMock(return_value="dummy prompt"))))):
        mock_create.return_value = MagicMock(choices=[MagicMock(message=MagicMock(content="Test summary"))])
        summarizer.warning = "Test warning"
        result = summarizer.paragraph_summarize_query(test_transcript)
        assert result is False  # should stop due to warning





import pytest
from src.query_logic import Summarizer
from dotenv import load_dotenv
import os
# from conftest import show_working_directory
# from unittest.mock import patch, MagicMock
# from pytest_mock import MockerFixture


@pytest.fixture
def summarizer():
    """Sets up Summarizer instance with OpenAI API key."""
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    return Summarizer(config=api_key)


def test_gpt_query(summarizer):
    test_query = "Hello, this is a test"
    response = summarizer.gpt_query(test_query)
    assert response is not False


def test_paragraph_summarize_query(summarizer):

    with open('test_transcript', 'r') as text:
        test_transcript = text.read()

    cwd = os.getcwd()
    gpt_prompt_path = os.path.abspath(f"{cwd}/../src/gpt_prompt")
    print(gpt_prompt_path)

    result = summarizer.paragraph_summarize_query(test_transcript, gpt_prompt_path)
    assert isinstance(result, str)


def test_paragraph_summarize_query_with_warning(summarizer):

    bad_request_transcript = "This is a test" * 1000  # this will cause 400 error

    cwd = os.getcwd()
    gpt_prompt_path = os.path.abspath(f"{cwd}/../src/gpt_prompt")

    result = summarizer.paragraph_summarize_query(bad_request_transcript, gpt_prompt_path)
    assert result is False
    assert summarizer.warning is not False


def test_gpt_query_auth_error(summarizer):
    test_query = "Hello, this is a test"
    # TODO: try mocking using this approach
    #  https://tobiaslang.medium.com/mocking-the-openai-api-in-python-a-step-by-step-guide-4630efcb809d
    # mocker.patch('openai.ChatCompletion.create', side_effect=AuthenticationError)
    # mocker.patch('openai.OpenAI', side_effect=AuthenticationError)
    summarizer.config = 'wrong_api_key'
    assert summarizer.gpt_query(test_query) is False
    assert "OpenAI could not validate your API key" in summarizer.warning


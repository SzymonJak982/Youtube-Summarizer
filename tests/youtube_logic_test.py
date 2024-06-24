import pytest
from unittest.mock import patch, MagicMock
from src.youtube_logic import YoutubeApi

# Defining a fixture for a VALID YoutubeApi instance
@pytest.fixture
def valid_youtube_api():
    return YoutubeApi("https://www.youtube.com/watch?v=dQw4w9WgXcQ")


# Defining a fixture for an INVALID YoutubeApi instance
@pytest.fixture
def invalid_youtube_api():
    return YoutubeApi("invalid_url_string")


def test_get_youtube_title():
    # External API test
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    assert YoutubeApi.get_youtube_title(url) is not None


def test_url_to_id(valid_youtube_api, invalid_youtube_api):
    assert valid_youtube_api.url_to_id() is True
    assert valid_youtube_api.video_id == "dQw4w9WgXcQ"

    assert invalid_youtube_api.url_to_id() is False
    assert invalid_youtube_api.warning == "Couldn't parse given url"


def test_video_id_validation(valid_youtube_api):
    valid_youtube_api.video_id = "dQw4w9WgXcQ"
    assert valid_youtube_api.video_id_validation() is True


def test_failed_validation(invalid_youtube_api):
    invalid_youtube_api.video_id = "dQw4w9WgXc,"
    assert invalid_youtube_api.video_id_validation() is False
    assert invalid_youtube_api.warning == 'Something went wrong when validating your URL'


def test_fetch_transcript(mocker, valid_youtube_api):
    """Simple integration & unit test"""
    # External API test
    assert valid_youtube_api.fetch_transcript() is not False

    # # Unit test
    mocker.patch.object(YoutubeApi, 'url_to_id', return_value=True)
    mocker.patch.object(YoutubeApi, 'video_id_validation', return_value=True)
    mocker.patch('youtube_transcript_api.YouTubeTranscriptApi.get_transcript', return_value=[{"text": "Hello"}, {"text": "World"}])

    transcript = valid_youtube_api.fetch_transcript()
    assert transcript == "Hello World"


def test_failed_transcript_fetch(mocker, invalid_youtube_api):
    # Simulating a failure in fetching the transcript
    mocker.patch.object(YoutubeApi, 'url_to_id', return_value=True)
    mocker.patch.object(YoutubeApi, 'video_id_validation', return_value=True)
    mocker.patch('youtube_transcript_api.YouTubeTranscriptApi.get_transcript',
                 return_value=[{"text": "Hello"}, {"text": "World"}])

    mocker.patch('youtube_transcript_api.YouTubeTranscriptApi.get_transcript', side_effect=Exception)
    assert invalid_youtube_api.fetch_transcript() is False
    assert invalid_youtube_api.warning == "Sorry, I couldn't fetch transcript for this video 😔"


def test_download_audio(mocker, valid_youtube_api):
    # External API test
    video_url = valid_youtube_api.video_url

    assert valid_youtube_api.download_audio(video_url) is not False

    # Unit test
    mock_yt = mocker.patch('pytube.YouTube')

    mock_stream = MagicMock()
    mock_streams = MagicMock()

    mock_streams.filter.return_value.first.return_value = mock_stream
    mock_yt.return_value.streams = mock_streams

    valid_youtube_api.download_audio(video_url, "audio.mp4")


    # Verifying that the download method was called with the correct filename
    mock_stream.download.assert_called_once_with(filename="audio.mp4")






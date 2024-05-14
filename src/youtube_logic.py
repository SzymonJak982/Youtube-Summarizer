from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import re
import time

def get_youtube_title(url):
    youtube = YouTube(url)
    return youtube.title


def fetch_transcript(video_url):
    def url_to_id(url):
        try:
            return url.split('v=')[1][:11]
        except Exception as e:
            warning = "Couldn't parse given url"
            return None, warning

    video_id = url_to_id(url=video_url)

    if isinstance(video_id, tuple):
        # TODO Optimise these 2 error messages
        warning = "Something went wrong upon validating your URL (1)"
        return None, warning

    pattern = r'[a-zA-Z0-9_-]{11}'
    match = re.match(pattern, video_id)
    if not match:
        warning = "Something went wrong upon validating your URL (2)"
        return None, warning

    max_retries = 3
    counter = 0

    while True:
        try:
            raw_transcript = YouTubeTranscriptApi.get_transcript(video_id)
            text_transcript = [i["text"] for i in raw_transcript]
            transcript = " ".join(text_transcript)
            return transcript, None
        except:
            # TODO: handle state info and log to streamlit
            print("Error fetching transcript. Retrying...")
            counter += 1
            if counter <= max_retries:
                time.sleep(2)
            else:
                warning = "Sorry, I couldn't fetch transcript for this video 😔"
                return None, warning



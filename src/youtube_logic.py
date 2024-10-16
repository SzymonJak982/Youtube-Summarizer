import pytube
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import re
import time


class YoutubeApi:
    def __init__(self, video_url):
        self.video_url = video_url
        self.video_id = None
        self.warning = None

    @staticmethod
    def get_youtube_title(url):
        try:
            youtube = YouTube(url)
            return youtube.title
        except:
            print("Unable to connect to Youtube API")
            return None

    def url_to_id(self):
        # TODO: This is shit implementation. Rewrite so it can be used from outside
        try:
            # parsing for url-s with session identifier
            pattern = r'\?si'
            url = self.video_url

            if re.search(pattern, url):
                video_id = self.video_url.split('https://youtu.be/')[1][:11]
            else:
                video_id = self.video_url.split('v=')[1][:11]
            self.video_id = video_id
            return video_id

        except Exception as e:
            self.warning = "Couldn't parse given url"
            return False

    def video_id_validation(self):
        """Extra validation: checking for any non-specific chars in vid_id"""
        pattern = r'[a-zA-Z0-9_-]{11}'
        if not re.match(pattern, self.video_id):
            self.warning = 'Something went wrong when validating your URL'
            return False

        return True

    def fetch_transcript(self):

        if not self.url_to_id():
            return False

        if self.video_id_validation():

            max_retries = 3
            counter = 0

            while True:
                try:
                    raw_transcript = YouTubeTranscriptApi.get_transcript(self.video_id)
                    text_transcript = [i["text"] for i in raw_transcript]
                    transcript = " ".join(text_transcript)
                    return transcript
                except:
                    # TODO: handle state info and log to streamlit
                    print("Error fetching transcript. Retrying...")
                    counter += 1
                    if counter <= max_retries:
                        time.sleep(2)
                    else:
                        self.warning = "Sorry, I couldn't fetch transcript for this video 😔"
                        return False
        else:
            return False

    @staticmethod
    def download_audio(video_url, output_path="../tmp/audio_stream.mp4"):
        try:
            start_time = time.time()

            yt = pytube.YouTube(video_url)
            audio_stream = yt.streams.filter(only_audio=True).first()
            audio_stream.download(filename=output_path)

            end_time = time.time()
            process_duration = end_time - start_time
            # print(f"Download took {process_duration} seconds")
            return True

        except:
            print("Unable to connect to Youtube API")
            return False








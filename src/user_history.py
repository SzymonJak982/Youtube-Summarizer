import time
import requests
import logging

from youtube_logic import YoutubeApi
# from database import crud_operations
from config import Config

logging.basicConfig(level=logging.INFO)


class History:
    def __init__(self):
        self.config = Config.API_URL
        self.summary_data = None


    def update_if_exists(self, video_id):
        url = f"{self.config}/check/{video_id}"
        response = requests.get(url)
        if response == 200:
            summary2update = response.text




    def local_history(self, answer, video_name, video_url):

        local_time = time.localtime()
        formatted_time = time.strftime("%d-%m-%Y %H:%M:%S", local_time)

        # only temporary

        url = "http://127.0.0.1:8000/summaries/"

        video_id = YoutubeApi(video_url)
        video_id_parsed = video_id.url_to_id()


        # 'method used': key to distinguish between whisper generated/og transcript generated answer- to be implemented
        self.summary_data = {
            "video_title": f"{video_name}",
            "timestamp": f"{formatted_time}",
            "video_url": f"{video_url}",
            "video_id": f"{video_id_parsed}",
            "summary": f"{answer}",
            "method_used": "unfilled"
        }

        response = requests.post(url, json=self.summary_data)

        # TODO Add response handler for different HTTP codes
        if response.status_code == 200:
            logging.info("Summary added successfully!")

        else:
            logging.warning(f"Failed to add summary: {response.status_code}")
            print(response.json())

    @staticmethod
    def serialize_history():
        # TODO: add this address to public config files- when hosted on Azure change code accordingly
        url = "http://127.0.0.1:8000/summaries/"
        # TODO: Check this serialization approach- maybe related with 'None' bug? Model_dump instead?
        response = requests.get(url)
        return response.text#json.dumps(response.text, ensure_ascii=False)


##  old functions for accessing session- related data
# def history():
#     return st.session_state["history"]
#
#
# def session_history(answer, video_name, video_url):
#
#     local_time = time.localtime()
#     formatted_time = time.strftime("%d-%m-%Y %H:%M:%S", local_time)
#     entry = (video_name, formatted_time, answer, video_url)
#
#     if "history" not in st.session_state:
#         st.session_state["history"] = []
#
#     entry_exists = any(vid_name == entry[0] for vid_name, format_time, ans, url in st.session_state['history'])
#     if not entry_exists:
#         st.session_state["history"].append(entry)
#     #     st.session_state["history_change"] = True
#     # else:
#     #     st.session_state["history_change"] = False







import time
import requests
import json

from youtube_logic import YoutubeApi
from config import Config
from logger import log


class History:
    def __init__(self):
        self.config = Config.API_URL
        self.summary_data = None


    def check_if_exists(self, video_id):
        url = f"{self.config}/check/{video_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            log.info("No summary found for given video_id. New will be created.")
            return None



    def local_history(self, answer, video_name, video_url):
        url = self.config

        local_time = time.localtime()
        formatted_time = time.strftime("%d-%m-%Y %H:%M:%S", local_time)

        v = YoutubeApi(video_url)
        video_id_parsed = v.url_to_id()


        # 'method used': key to distinguish between whisper generated/og transcript generated answer- to be implemented
        self.summary_data = {
            "video_title": f"{video_name}",
            "timestamp": f"{formatted_time}",
            "video_url": f"{video_url}",
            "video_id": f"{video_id_parsed}",
            "summary": f"{answer}",
            "method_used": "unfilled"
        }

        # Here goes the update
        summary2pdate = self.check_if_exists(video_id_parsed)
        if summary2pdate:
            update_id = json.loads(summary2pdate)["id"]
            update_url = f"{url}/{update_id}"
            response = requests.put(update_url, json= self.summary_data)
            operator_string = "Summary updated succesfully!"

        else:
            response = requests.post(url, json=self.summary_data)
            operator_string = "Summary added succesfully!"


        # TODO Add response handler for different HTTP codes
        if response.status_code == 200:
            log.info(operator_string)

        else:
            log.warning(f"Failed to add summary: {response.status_code}")
            print(response.json())

    def serialize_history(self):
        url = self.config
        response = requests.get(url)
        return response.text


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







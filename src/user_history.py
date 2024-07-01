# import json
# import streamlit as st
import time
import requests

import logging

logging.basicConfig(level=logging.INFO)


class History:
    def __init__(self):
        pass

    @staticmethod
    def session_history(answer, video_name, video_url):

        local_time = time.localtime()
        formatted_time = time.strftime("%d-%m-%Y %H:%M:%S", local_time)

        # only temporary
        url = "http://127.0.0.1:8000/summaries/"

        # 'method used': key to distinguish between whisper generated/og transcript generated answer
        data = {
            "video_title": f"{video_name}",
            "timestamp": f"{formatted_time}",
            "video_url": f"{video_url}",
            "summary": f"{answer}",
            "method_used": "unfilled"
        }

        response = requests.post(url, json=data)

        if response.status_code == 200:
            logging.info("Summary added successfully!")

        else:
            logging.warning(f"Failed to add summary: {response.status_code}")
            print(response.json())

    @staticmethod
    def serialize_history():

        url = "http://127.0.0.1:8000/summaries/"

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







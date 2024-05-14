import streamlit as st
import time

def history():
    return st.session_state["history"]


def session_history(answer, video_name, video_url):

    local_time = time.localtime()
    formatted_time = time.strftime("%d-%m-%Y %H:%M:%S", local_time)
    entry = (video_name, formatted_time, answer, video_url)

    if "history" not in st.session_state:
        st.session_state["history"] = []

    entry_exists = any(vid_name == entry[0] for vid_name, format_time, ans, url in st.session_state['history'])
    if not entry_exists:
        st.session_state["history"].append(entry)
        st.session_state["history_change"] = True
    else:
        st.session_state["history_change"] = False





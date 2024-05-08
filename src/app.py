import re

import streamlit as st
import time
import textwrap
import query_logic
import youtube_logic

# from dotenv import load_dotenv
import os
import textwrap


st.title('Youtube Summarizer')

st.write("""This is an experimental project of YouTube summarizer, creating notes from youtube videos.""" )

disclaimer = st.info("Note: In the current version, summarization is unavailable for videos with disabled subtitles.")
# TODO: for the v2 - figure out a way to get a transcript using whisper if transcript is unavailable

# TODO: Prompt the user with disappearing info to open a sidebar- nice to have?
with st.sidebar.form(key='my_form'):
    logo = st.image("../logo.png", caption="Friendly Summarizer, always with a helping hand!",
                    )
    youtube_url = st.text_area(
        label="Please provide YouTube video URL- example: https://www.youtube.com/watch?v=U9mJuUkhUzk ",
        max_chars=100
    )
    # query = st.sidebar.text_area(
    #     label="Summarize specific parts of the video:",
    #     max_chars=100,
    #     key="query"
    # )
    openai_api_key = st.text_input(
        label="OpenAI API Key",
        key="api_key",
        type="password",
        placeholder="Example: sk-XXX"

        )
    # TODO: Optimise this dummy function
    def all_submitted():
        st.session_state.message = "All submitted"


    submit_button = st.form_submit_button(
        label='Submit',
        on_click=all_submitted(),
        use_container_width=True,
        type="primary",
        )


if youtube_url and openai_api_key and submit_button:
    # TODO: Prompt the user to give API key if he forgot
    # success_message_placeholder = st.empty()
    # with success_message_placeholder.container():
    st.write(" ")
    st.write(" ")

    with st.spinner("Loading...📝"):

        yt_api_answer, warning = query_logic.fetch_transcript(youtube_url)

        if yt_api_answer:
            transcript = yt_api_answer
            # TODO: when waiting, log status of the process from backend
            video_title = youtube_logic.get_youtube_title(youtube_url)
            st.header(video_title)
            video_embed = st.video(youtube_url)
            summarization, warning = query_logic.ai_summarization(transcript=transcript, openai_api_key=openai_api_key)

            if summarization:
                final_answer = summarization
                # st.subheader("Summary from submitted video:")

                # saving a state of teh answer using time key-TODO: move downwards after dev
                local_time = time.localtime()
                formatted_time = time.strftime("%d-%m-%Y %H:%M:%S", local_time)

                st.session_state[formatted_time] = final_answer
                # st.info(st.session_state)
                # TODO: Add history of the streamlit session, embed in on the extendable bar below
                # TODO: Find out how to access the keys datetime and their values and save to history
                session_state_dict = st.session_state.to_dict()
                pattern = r'\d{1,2}\/\d{1,2}\/\d{2,4}'
                # TODO: (history) START HERE
                # match = re.match(list(session_state_dict.keys()), pattern)
                # st.info(match)

                st.markdown(summarization)
                st.success("Done!")
                st.balloons()
                # success_message_placeholder.success("Done!")

            elif summarization is None:
                final_answer = warning
                st.info(warning)

        elif yt_api_answer is None:
            transcript = warning
            st.info(warning)

else:
    st.stop()





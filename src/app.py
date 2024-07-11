import sqlalchemy.exc
import streamlit as st
from youtube_logic import YoutubeApi
from query_logic import Summarizer
from user_history import History
import ast
import logging

logging.basicConfig(level=logging.INFO)

st.title('Youtube Summarizer')
st.write("""This is an experimental project of YouTube summarizer, creating notes from youtube videos.""")

disclaimer = st.info("Note: In this version, summarization is available almost exclusively for english-language videos")


def history_display():
    """Displays history read from sqlite session as expanders. Limit:20"""
    # history_as_list = user_history.history()
    try:
        history = History()
        history_as_list = history.serialize_history()
        # vid_name, format_time, ans, url
        for record in reversed(ast.literal_eval(history_as_list)):
            # title
            with st.expander(record["video_title"]):
                st.write(record["timestamp"])
                st.video(record["video_url"])
                st.markdown(record["summary"])

    except Exception as e:
        logging.info(e)
        # Handling empty database for new user
        return None


@st.cache_data
def summarization_wrapper(output):
    """Small util wrapper"""
    return output


tab1, tab2 = st.tabs(["Summarizer", "Your summaries"])


with tab2:
    st.info("Note: In the current version your summaries are stored locally as .db file in this project.")
    history_display()

with tab1:
    with st.sidebar.form(key='my_form'):
        logo = st.image("../logo.png", caption="Friendly Summarizer, always with a helping hand!",
                        )
        youtube_url = st.text_area(
            label="Please provide YouTube video URL:",
            max_chars=100
        )

        openai_api_key = st.text_input(
            label="OpenAI API Key",
            key="api_key",
            type="password",
            placeholder="Example: sk-XXX"

            )
        #TODO: Optimise this dummy function
        def all_submitted():
            st.session_state.message = "All submitted"


        submit_button = st.form_submit_button(
            label='Submit',
            on_click=all_submitted(),
            use_container_width=True,
            type="primary",
            )

        quiz_generation = False

        st.write(" ")
        on = st.toggle("Test your knowledge!")
        if on:
            quiz_generation = True

    if youtube_url and openai_api_key and submit_button:

        st.write(" ")
        st.write(" ")

        with st.spinner("Loading...📝"):

            youtube = YoutubeApi(youtube_url)
            transcript = youtube.fetch_transcript()

            if transcript:
                video_title = youtube.get_youtube_title(youtube_url)
                st.header(video_title)
                st.video(youtube_url)

                summarizer = Summarizer(openai_api_key)
                summ = summarizer.paragraph_summarize_query(transcript)
                summarization = summarization_wrapper(summ)
                print(summarization)

                if quiz_generation:
                    qna = summarizer.quiz_generator(summarization)

                history = History()
                history.session_history(summarization, video_title, youtube_url)

                def quiz_display(question_and_answer):
                    for entry in question_and_answer:
                        with st.expander(entry):
                            pass


                if summarization:
                    st.markdown(summarization)
                    if quiz_generation:
                        st.markdown(qna)
                    st.success("Done!")
                    st.balloons()
                else:
                    st.info(summarizer.warning)
            else:
                st.info(youtube.warning)

    else:
        st.stop()

# with tab2:
#     # Streamlit does not offer conditional rendering
#
#     history_display()


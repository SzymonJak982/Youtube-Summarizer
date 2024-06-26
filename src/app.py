import streamlit as st
from youtube_logic import YoutubeApi
from query_logic import Summarizer
import user_history


st.title('Youtube Summarizer')
st.write("""This is an experimental project of YouTube summarizer, creating notes from youtube videos.""")

disclaimer = st.info("Note: In the current version, summarization is unavailable for videos with disabled subtitles.")
# TODO: for the v2 - figure out a way to get a transcript using whisper if transcript is unavailable

tab1, tab2 = st.tabs(["Summarizer", "Your summaries"])

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
                summarization = summarizer.paragraph_summarize_query(transcript, 'gpt_prompt')
                # TODO: Here put logic call to endpoint.
                user_history.session_history(summarization, video_title, youtube_url)

                if summarization:
                    st.markdown(summarization)
                    st.success("Done!")
                    st.balloons()
                else:
                    st.info(summarizer.warning)
            else:
                st.info(youtube.warning)

    else:
        st.stop()

with tab2:
    st.info("Note: In the current version your summaries are present only in the current browser session and will be lost after refresh.")

    ######## Info for dev
    # st.info(st.session_state["history"])
    # st.info(st.session_state["history_change"])
    # # limit = 20
    ########
    history_as_list = user_history.history()
    # vid_name, format_time, ans, url
    for vid_name, time, answer, url in reversed(history_as_list):
        # title
        with st.expander(vid_name):
            # timestamp
            st.write(time)
            # vid_embed
            st.video(url)
            # summary
            st.markdown(answer)


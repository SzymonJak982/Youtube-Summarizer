import streamlit as st
import time
import query_logic
import youtube_logic
import user_history


st.title('Youtube Summarizer')
st.write("""This is an experimental project of YouTube summarizer, creating notes from youtube videos.""" )

disclaimer = st.info("Note: In the current version, summarization is unavailable for videos with disabled subtitles.")
# TODO: for the v2 - figure out a way to get a transcript using whisper if transcript is unavailable

tab1, tab2 = st.tabs(["Summarizer", "Your summaries"])

with tab1:
    with st.sidebar.form(key='my_form'):
        logo = st.image("../logo.png", caption="Friendly Summarizer, always with a helping hand!",
                        )
        youtube_url = st.text_area(
            label="Please provide YouTube video URL- example: https://www.youtube.com/watch?v=U9mJuUkhUzk ",
            max_chars=100
        )

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

        st.write(" ")
        st.write(" ")

        with st.spinner("Loading...📝"):

            yt_api_answer, warning = youtube_logic.fetch_transcript(youtube_url)

            if yt_api_answer:
                transcript = yt_api_answer
                # TODO: when waiting, log status of the process from backend
                video_title = youtube_logic.get_youtube_title(youtube_url)
                st.header(video_title)
                video_embed = st.video(youtube_url)
                # TODO implement class
                summarization, warning = query_logic.ai_summarization(transcript, openai_api_key)

                if summarization:
                    final_answer = summarization
                    st.markdown(summarization)
                    st.success("Done!")
                    st.balloons()

                    user_history.session_history(final_answer, video_title, youtube_url)

                elif summarization is None:
                    final_answer = warning
                    st.info(warning)

            elif yt_api_answer is None:
                transcript = warning
                st.info(warning)

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


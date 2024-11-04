import streamlit as st
from youtube_logic import YoutubeApi
from query_logic import Summarizer
from user_history import History
from app_utils import StreamlitUtils, Quiz
from logger import log


@st.cache_data
def summarization_wrapper(output):
    return output

@st.cache_data
def transcript_generation_wrapper(output):
    return output


# st.title('Youtube Summarizer')

st.write("""This is an experimental project of YouTube summarizer, creating notes from youtube videos.""")

disclaimer = st.info("Note: In this version, summarization is available almost exclusively for english-language videos")

# @st.cache_data
# def summarization_wrapper(output):
#     # TODO: Figure out what to do with it or delete it.
#     """Small util wrapper for caching summary- does not work"""
#     return output



tab1, tab2, tab3 = st.tabs(["Summarizer", "Your summaries", "Your quiz"])

# Tabs in the reversed order because Streamlit reruns this script on every change
# For correct history generation and dynamic quiz interaction

utils = StreamlitUtils()
utils.st_sessionstate_init()

log.info('Active quiz' if st.session_state.quiz_qna else 'Inactive quiz')



with tab3:
    if st.session_state.quiz_qna:
        Quiz.render_quiz()

with tab1:
    if st.session_state.quiz_qna:
        #TODO: Data is not saved in the function itself. Figure out how to access this data.
        cached_transcript = transcript_generation_wrapper(st.session_state.video_url)

        # cache_t
        s = summarization_wrapper(cached_transcript)
        st.markdown(s)

with tab2:
    st.info("⟳ Refresh the page to see the most recent summary")
    # utils = StreamlitUtils()
    utils.history_display()


with tab1:
    with st.sidebar.form(key='my_form'):
        logo = st.image("../logo.png", caption="Friendly Summarizer, always with a helping hand!",
                        )
        st.subheader("Summarize! 📝")

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

        # Here, transform this into session state
        quiz_generation = False

        utils.spacer(1)
        st.subheader("Quiz me! 🤔")

        options = ["Open-ended exploratory questions", "Quiz-type questions", "Both, bring it on!"]
        option_select = st.selectbox("Select type of questions", options, index=None, placeholder="None (default)")

        if option_select:
            quiz_generation = True

        submit_button = st.form_submit_button(
            label='Submit',
            on_click=all_submitted(),
            use_container_width=True,
            type="primary",
        )

    if youtube_url and openai_api_key and submit_button:

        utils.spacer(2)

        with st.spinner("Loading...📝"):
            # TODO: Optional: This process can be optimised in the by running in a single classes (clearer code)

            youtube = YoutubeApi(youtube_url)
            transcript = youtube.fetch_transcript()

            if transcript:
                # caching transcript for session in streamlit
                cache_t = transcript_generation_wrapper(transcript)

                st.session_state.video_url = youtube_url
                video_title = youtube.get_youtube_title(youtube_url)
                st.header(video_title)
                st.video(youtube_url)

                summarizer = Summarizer(openai_api_key)
                s = summarizer.paragraph_summarize_query(transcript)

                # caching a summary for session in streamlit
                summarization = summarization_wrapper(s)
                # summarization = summarization_wrapper(s)
                print(summarization)

                # Saving a summary to history
                history = History()
                history.local_history(summarization, video_title, youtube_url)

                if summarization:
                    # Generating quiz based on summary
                    q = Quiz()
                    quiz = q.question_creator(options, option_select, summarizer, summarization)
                    (qna, quiz_qna) = quiz

                    if quiz_qna:
                        # saving QUIZ as JSON to tmp/ path
                        utils.save_quiz_questions(quiz_qna)

                    st.markdown(summarization)
                    st.success("Done!")

                    if quiz_generation:

                        # If exploratory questions were chosen, they are displayed at the bottom of the summary
                        utils.spacer(1)

                        if qna:
                            utils.quiz_display(qna)
                        else:
                            st.info("For quiz, head on to 'Your quiz' tab")

                    # st.balloons()

                else:
                    st.info(summarizer.warning)
            else:
                st.info(youtube.warning)

    else:
        st.stop()


# Tab is rerun to generate new quiz after choosing "QUIT" option.
with tab3:
    if st.session_state.quiz_qna:
        # pass
        # # actual code to be run here
        Quiz.render_quiz()




import streamlit as st
from youtube_logic import YoutubeApi
from query_logic import Summarizer
from user_history import History
from app_utils import StreamlitUtils, Quiz

# import ast
import logging

logging.basicConfig(level=logging.INFO)

st.title('Youtube Summarizer')

st.write("""This is an experimental project of YouTube summarizer, creating notes from youtube videos.""")

disclaimer = st.info("Note: In this version, summarization is available almost exclusively for english-language videos")

@st.cache_data
def summarization_wrapper(output):
    """Small util wrapper"""
    return output


tab1, tab2, tab3 = st.tabs(["Summarizer", "Your summaries", "Your quiz"])


with tab2:
    st.info("Note: In the current version your summaries are stored locally as .db file in this project.")
    utils = StreamlitUtils()
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

        quiz_generation = False

        utils.spacer(1)
        st.subheader("Quiz me! 🤔")

        on = st.toggle("Test your knowledge!")#, on_change=utils.quiz_mode_init())
        if on:
            quiz_generation = True

        option = st.selectbox("Select type of questions",
                     ("Open-ended exploratory questions", "Quiz-type questions", "Both, bring it on!"),
                     index=None)




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
                video_title = youtube.get_youtube_title(youtube_url)
                st.header(video_title)
                st.video(youtube_url)

                summarizer = Summarizer(openai_api_key)
                summ = summarizer.paragraph_summarize_query(transcript)
                summarization = summarization_wrapper(summ)
                print(summarization)

                # Saving a summary to history
                history = History()
                history.local_history(summarization, video_title, youtube_url)

                if summarization:

                    if option == 'Open-ended exploratory questions' or option is None:
                        qna = summarizer.quiz_generator(summarization)
                        quiz_qna = None

                    elif option == 'Quiz-type questions':
                        qna = None
                        quiz_qna = summarizer.quiz_generator(summarization, is_scq_quiz=True)

                    elif option == "Both, bring it on!":
                        qna = summarizer.quiz_generator(summarization)
                        quiz_qna = summarizer.quiz_generator(summarization, is_scq_quiz=True)


                    if quiz_qna is not None:
                        utils.save_quiz_questions(quiz_qna)

                    st.markdown(summarization)
                    st.success("Done!")

                    if quiz_generation:

                        # If exploratory questions were chosen, they are displayed at the bottom of the summary
                        utils.spacer(1)
                        utils.quiz_display(qna) if qna is not None else st.write("For quiz, head on to 'Your quiz' tab")

                        # TODO: If 'both' or quiz type was chosen, inform the user that he can find his quiz in another tab
                    # st.balloons()

                else:
                    st.info(summarizer.warning)
            else:
                st.info(youtube.warning)

    else:
        st.stop()


with tab3:
    if quiz_qna:
        # pass
        # # actual code to be run here
        Quiz.render_quiz()


# with tab2:
#     # Streamlit does not offer conditional rendering
#
#     history_display()


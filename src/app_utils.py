import streamlit as st
from user_history import History
from logger import log
import json
import os
from config import Config
from style_customization import UICustomization





class StreamlitUtils:
    """Class to handle different Streamlit functionalities outside of main app.py file"""
    def __init__(self):
        self.tmp_config = Config.TMP_PATH

    @staticmethod
    def st_sessionstate_init():
        """Initialize st.session state variables"""
        # # for many variables:
        # default_values = {"quiz_qna": False}
        # for key, value in default_values.items():
        #     st.session_state.setdefault(key, value)
        if "quiz_qna" not in st.session_state:
            st.session_state.quiz_qna = False
        if "video_url"not in st.session_state:
            st.session_state.video_url = False

    @staticmethod
    def spacer(space_width: int):
        """Small util for creating spaces- not supported in streamlit natively"""
        for _ in range(space_width):
            st.write(" ")

    @staticmethod
    def history_display():
        """Displays history read from sqlite session as expanders. Limit:20"""
        # history_as_list = user_history.history()
        try:
            history = History()
            history_as_list = json.loads(history.serialize_history())
            # TODO: segregate dictionaries in a list based on timestamp for displaying updated at the top
            # vid_name, format_time, ans, url
            for record in reversed(history_as_list):
                with st.expander(record["video_title"]):
                    st.write(record["timestamp"])
                    # st.write(record["video_id"])
                    st.video(record["video_url"])
                    st.markdown(record["summary"])

        except Exception as e:
            log.info(e)
            return None

    @staticmethod
    def quiz_display(question_and_answer):

        response = json.loads(question_and_answer)

        StreamlitUtils.spacer(2)

        st.subheader("Now, let's test your knowledge! Expand to see the answer.")

        for record_id, record in response.items():
            with st.expander(record['question']):
                st.write(record['answer'])

    def save_quiz_questions(self, generated_quiz):

        directory = self.tmp_config
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(f"{directory}/test_quiz.json", "w") as json_file:
            json_file.write(generated_quiz)


class Quiz:
    """Class for creating interactive quiz in streamlit for the user
    Works on json generated and saved in tmp/ by query logic. """

    # TODO: Add structure validation to GPT quiz-json response
    # TODO: handle scenario when GPT is unavaialble and no transcript was generated
    # TODO: Handle additional potential retry logic if needed
    def __init__(self):
        self.tmp_config = Config.TMP_PATH

    @staticmethod
    def question_creator(options, option_select, qna_query, summarization):
        """
        :param options: ["Open-ended exploratory questions", "Quiz-type questions", "Both, bring it on!"]
        :param qna_query: Qerying the LLM for quiz about summarized text
        """
        qna = None
        quiz_qna = None

        # if "quiz_qna" not in st.session_state:
        #     # False by default
        #     st.session_state.quiz_qna = False

        if option_select == options[0] or option_select is True:
            qna = qna_query.quiz_generator(summarization)
            # quiz_qna = None
        elif option_select == options[1]:
            # qna = None
            quiz_qna = qna_query.quiz_generator(summarization, is_scq_quiz=True)
            # if "quiz_qna" not in st.session_state:
                # TODO: Disable that after quiz is finished
            st.session_state.quiz_qna = quiz_qna

        elif option_select == options[2]:
            qna = qna_query.quiz_generator(summarization)
            quiz_qna = qna_query.quiz_generator(summarization, is_scq_quiz=True)

        return qna, quiz_qna


    def open_json(self):
        """Placeholder for a return. """
        # TODO: Change JSON schema and change quiz algo to handle int as keys with values as lists
        with open(f"{self.tmp_config}/test_quiz.json", "r", encoding='utf8') as f:
            quiz_data = json.load(f)
        return quiz_data["1"]

    @staticmethod
    def render_quiz():
        """All of the logic for rendering interactive quiz
        Original streamlit-quiz idea by banderpt: https://github.com/benderpt/streamlit_quizz_template/blob/main/main.py"""
        # style customization
        UICustomization.change_button_style()

        # initializing session state variables
        default_values = {'current_index': 0, 'current_question': 0, 'score': 0, 'selected_option': None,
                          'answer_submitted': False}
        for key, value in default_values.items():
            st.session_state.setdefault(key, value)

        # Loading saved quiz
        q = Quiz()

        quiz_data = q.open_json()
        if "quiz_data" not in st.session_state:
            st.session_state.quiz_data = quiz_data

        data = st.session_state.quiz_data

        def restart_quiz():
            st.session_state.current_index = 0
            st.session_state.score = 0
            st.session_state.selected_option = None
            st.session_state.answer_submitted = False

        def submit_answer():
            if st.session_state.selected_option:
                st.session_state.answer_submitted = True

                # Check if the selected option is correct
                if st.session_state.selected_option == st.session_state.quiz_data[st.session_state.current_index]['answer']:
                    st.session_state.score += 1

            else:
                # If no option selected, show a message and do not mark as submitted
                st.warning("Please select an option before submitting.")

        def next_question():
            st.session_state.current_index += 1
            st.session_state.selected_option = None
            st.session_state.answer_submitted = False

        def close_quiz():
            st.session_state.quiz_qna = False

        st.title("Quiz")

        # Progress bar
        progress_bar_value = (st.session_state.current_index + 1) / len(st.session_state.quiz_data)
        st.metric(label="Score", value=f"{st.session_state.score} / {len(st.session_state.quiz_data)}")
        st.progress(progress_bar_value)

        # Display the question and answer options
        question_item = st.session_state.quiz_data[st.session_state.current_index]
        st.subheader(f"Question {st.session_state.current_index + 1}")
        st.subheader(question_item["question"])
        # st.write(question_item['information'])

        st.markdown(""" ___""")

        options = question_item['options']
        correct_answer = question_item['answer']

        # Checking if correct
        if st.session_state.answer_submitted:
            for i, option in enumerate(options):
                label = option
                if option == correct_answer:
                    st.success(f"{label} (Correct!)")
                elif option == st.session_state.selected_option:
                    st.error(f"{label} (Incorrect)")
                else:
                    st.write(label)

        # Listing the options
        else:
            for i, option in enumerate(options):
                if st.button(option, key=i, use_container_width=True):
                    st.session_state.selected_option = option

        st.markdown(""" ___""")

        # Submission button and response logic
        if st.session_state.answer_submitted:
            if st.session_state.current_index < len(st.session_state.quiz_data) - 1:
                st.button('Next', on_click=next_question)
            else:
                st.write(f"Quiz completed! Your score is: {st.session_state.score} / {len(data)}")
                if st.button('Restart', on_click=restart_quiz):
                    pass
        else:
            if st.session_state.current_index < len(st.session_state.quiz_data):
                st.button('Submit', on_click=submit_answer)
                st.button('Quit', on_click= close_quiz)





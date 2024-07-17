import streamlit as st
from user_history import History
import ast
import logging
import json
import os


class StreamlitUtils:
    """Class to handle different Streamlit functionalities outside of main app.py file"""
    def __init__(self):
        pass

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

    @staticmethod
    def quiz_display(question_and_answer):

        response = json.loads(question_and_answer)

        StreamlitUtils.spacer(2)

        st.subheader("Now, let's test your knowledge! Expand to see the answer.")

        for record_id, record in response.items():
            with st.expander(record['question']):
                st.write(record['answer'])

        # TODO: introduced bug with None here ?


    @staticmethod
    def quiz_mode_init():
        # if 'quiz_init' not in st.session_state:
        #     st.session_state.quiz_init = False

        # callback to update 'init' based on 'check'
        # def flip():
        #     if st.session_state["check"]:
        #         st.session_state["init"] = True
        #     else:
        #         st.session_state["init"] = False
        #
        # if "init" not in st.session_state:
        #     st.session_state["init"] = True
        #
        # st.toggle(
        #     "Flip the switch, bitch", value=st.session_state["init"], key="check", on_change=flip
        # )
        #
        # st.write(st.session_state["test"])
        pass

    @staticmethod
    def save_quiz_questions(generated_quiz):

        directory = "tmp/json"
        if not os.path.exists(directory):
            os.makedirs(directory)

        # data = json.loads(generated_quiz)

        with open(f"{directory}/test_quiz.json", "w") as json_file:
            # json.dump(data, json_file, indent=4)
            json_file.write(generated_quiz)





class Quiz:
    """Class for creating interactive quiz in streamlit for the user
    Works on json generated and saved in tmp/ by query logic. """

    # TODO: Add structure validation to GPT quiz-json response
    # TODO: handle scenario when GPT is unavaialble and no transcript was generated
    # TODO: Handle additional potential retry logic if needed
    def __init__(self):
        pass

    @staticmethod
    def open_json():
        """Placeholder for a return. """
        # TODO: Change JSON schema and change quiz algo to handle int as keys with values as lists
        with open("tmp/json/test_quiz.json", "r", encoding='utf8') as f:
            quiz_data = json.load(f)
        return quiz_data["1"]



    @staticmethod
    def render_quiz():
        """All of the logic for rendering quiz
        Original streamlit-quiz idea by banderpt: https://github.com/benderpt/streamlit_quizz_template/blob/main/main.py"""

        # initialising session state variables
        default_values = {'current_index': 0, 'current_question': 0, 'score': 0, 'selected_option': None,
                          'answer_submitted': False}
        for key, value in default_values.items():
            st.session_state.setdefault(key, value)

        # Loading saved quiz
        quiz_data = Quiz.open_json()

        # questions = []
        # correct = []
        # explanations = []
        # options = []
        #
        # for entry_id, entry in quiz_data.items():
        #     questions.append(entry["scq"])
        #     correct.append(entry['correct'])
        #     explanations.append(entry['explanation'])
        #     options.append(entry['options'])

        def restart_quiz():
            st.session_state.current_index = 0
            st.session_state.score = 0
            st.session_state.selected_option = None
            st.session_state.answer_submitted = False

        def submit_answer():

            # Check if an option has been selected- change from default None state
            if st.session_state.selected_option is not None:
                # Mark the answer as submitted
                st.session_state.answer_submitted = True

                # correct_answers = []
                # for entry_id, entry in quiz_data.items():
                #     correct_answers.append(entry['correct'])

                # Check if the selected option is correct
                if st.session_state.selected_option == quiz_data[st.session_state.current_index]['answer']:
                    st.session_state.score += 1

            else:
                # If no option selected, show a message and do not mark as submitted
                st.warning("Please select an option before submitting.")

        def next_question():
            st.session_state.current_index += 1
            st.session_state.selected_option = None
            st.session_state.answer_submitted = False

        st.title("Streamlit Quiz App")

        # Progress bar
        progress_bar_value = (st.session_state.current_index + 1) / len(quiz_data)
        st.metric(label="Score", value=f"{st.session_state.score} / {len(quiz_data)}")
        st.progress(progress_bar_value)

        # Display the question and answer options
        question_item = quiz_data[st.session_state.current_index]
        st.subheader(f"Question {st.session_state.current_index + 1}")
        st.subheader(question_item["question"])
        # st.write(question_item['information'])

        st.markdown(""" ___""")

        options = question_item['options']
        correct_answer = question_item['answer']

        if st.session_state.answer_submitted:
            for i, option in enumerate(options):
                label = option
                if option == correct_answer:
                    st.success(f"{label} (Correct!)")
                elif option == st.session_state.selected_option:
                    st.error(f"{label} (Incorrect)")
                else:
                    st.write(label)
        else:
            for i, option in enumerate(options):
                if st.button(option, key=i, use_container_width=True):
                    st.session_state.selected_option = option

        st.markdown(""" ___""")

        # Submission button and response logic
        if st.session_state.answer_submitted:
            if st.session_state.current_index < len(quiz_data) - 1:
                st.button('Next', on_click=next_question)
            else:
                st.write(f"Quiz completed! Your score is: {st.session_state.score} / {len(quiz_data) * 10}")
                if st.button('Restart', on_click=restart_quiz):
                    pass
        else:
            if st.session_state.current_index < len(quiz_data):
                st.button('Submit', on_click=submit_answer)


        # # Answer selection
        # answer_options = []
        # answer_option_ids = []
        #
        # for ans_option, ans_opt_id in options[0].items():
        #     answer_options.append(ans_option)
        #     answer_option_ids.append(ans_opt_id)

        # option_item = options[st.session_state.current_index]
        # correct_answer = correct[st.session_state.current_index]
        # explanation_item = explanations[st.session_state.current_index]
        # # TODO- finish this algo, checking if answer chosen by user through radio is == correct. Check through dict.
        #
        # user_choice = st.radio(question_item, list(option_item.values()), index=None, on_change=submit_answer())
        # if user_choice is not None:
        #     st.session_state.selected_option = user_choice
        #
        # if st.session_state.answer_submitted:
        #     selected_key = [key for key, value in option_item.items() if value == user_choice]
        #     if selected_key == correct_answer:
        #         st.success(f"Correct answer!{explanation_item}")
        #
        #     elif selected_key != correct_answer and selected_key is not None:
        #         st.error(f"Incorrect 😔{explanation_item}")
        #
        #     else:
        #         st.write(explanation_item)
        #

        # if user_choice


        # if st.session_state.answer_submitted:
        #     for i, option in enumerate(answer_options):
        #         label = option
        #         if option == correct_answer:
        #             st.success(f"{label} (Correct answer)")
        #         elif option == st.session_state.selected_option:
        #             st.error(f"{label} (Incorrect answer)")
        #         else:
        #             st.write(label)
        # else:
        #     for i, option in enumerate(options):
        #         if st.button(option, key=i, use_container_width=True):
        #             st.session_state.selected_option = option
        #
        # st.markdown(""" ___""")
        #
        # # Submission button and response logic
        # if st.session_state.answer_submitted:
        #     if st.session_state.current_index < len(quiz_data) - 1:
        #         st.button('Next', on_click=next_question)
        #     else:
        #         st.write(f"Quiz completed! Your score is: {st.session_state.score} / {len(quiz_data)}")
        #         if st.button('Restart', on_click=restart_quiz):
        #             pass
        # else:
        #     if st.session_state.current_index < len(quiz_data):
        #         st.button('Submit', on_click=submit_answer)





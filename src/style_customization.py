import streamlit as st


class UICustomization:
    # class for custom CSS injections to streamlit
    # TODO: Check if this works
    def __init__(self):
        pass

    @staticmethod
    def change_button_style():
        # button styling, unsafe allow... for executing HTML as markdown
        st.markdown("""
        <style>
        div.stButton > button:first-child {
            display: block;
            margin: 0 auto;
        </style>
        """, unsafe_allow_html=True)


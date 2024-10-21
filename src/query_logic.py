from openai import OpenAI
import os
import time
import textwrap
from openai._exceptions import AuthenticationError, InternalServerError
from typing import Optional, Union
from logger import log
from utilities import get_path



class Summarizer:
    # TODO: Optional: Manage downstream processing and warnings with this class
    def __init__(self, config):
        self.config = config
        self.warning = None

    def gpt_query(self, request, temperature, json_response=False) -> Optional[Union[str, bool]]:
        """GPT-query method for creating summaries and creating quizes
        :param json_response: specifing response as a JSON file for quiz_generator method
        :param temperature: abstraction factor for GPT
        :param request: prompt for summary or quiz generation (prompt templates in /tmp/) """
        #TODO: Add output-type declaration and menage empty/non empty responses (isinstance+len) tather than str+ bool

        os.environ['OPENAI_API_KEY'] = self.config
        client = OpenAI()
        counter = 0
        max_retries = 3

        while True:
            try:
                if json_response:
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo-0125",
                        temperature=temperature,
                        response_format={"type": "json_object"},
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant"},
                            {"role": "user", "content": request}
                        ],
                        stop="END_SUMMARY"
                    )
                    return response.choices[0].message.content

                else:
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo-0125",
                        temperature=temperature,
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant"},
                            {"role": "user", "content": request}
                        ],
                        stop="END_SUMMARY"
                    )
                    return response.choices[0].message.content

            except AuthenticationError as e:
                self.warning = f"OpenAI could not validate your API key: {e.message}"
                return False

            except (InternalServerError, Exception) as e:
                log.warning(e)
                counter += 1
                if counter <= max_retries:
                    time.sleep(1)
                    # self.warning = e
                else:
                    self.warning = f"Sorry, there was a problem with connecting to OpenAI API:{e}"
                    return False

    @staticmethod
    def chunker(text, chunk_length) -> Optional[list]:
        return textwrap.wrap(text, chunk_length)

    def paragraph_summarize_query(self, transcript) -> \
            Optional[Union[str, bool]]:
        chunks = Summarizer.chunker(text=transcript, chunk_length=8000)

        # gpt_prompt_path = "prompts_and_schemas/gpt_prompt"
        gpt_prompt_path = get_path("gpt_prompt")

        with open(gpt_prompt_path, 'r') as p:
            gpt_prompt_template = p.read()

        result = []
        count = 0

        for chunk in chunks:
            count = count + 1
            current_paragraph = chunk
            prompt = gpt_prompt_template.format_map({'paragraph': current_paragraph})
            summary = self.gpt_query(request=prompt, temperature=0)

            if self.warning:
                return False

            #TODO: Optional: Handle state logging to streamlit like progress bar
            print('\n\n\n', count, 'of', len(chunks), summary)
            result.append(summary)

        return ' '.join(result)

    def quiz_generator(self, request, is_scq_quiz=False):
        """ Open AI query for quiz generation

        :param request: summary generated for the video
        :param is_scq_quiz: argument from streamlit, specifying if quiz should be a single choice test.
        By default, set to False if not specified otherwise"""

        # TODO: Provide additional instructions to avoid stupid questions (prompt-related, needs some testing)
        # TODO: better path management!

        quiz_prompt_path = get_path("quiz_prompt") if is_scq_quiz is False else get_path("scq_quiz_prompt")
        quiz_json_schema_path = get_path("quiz_schema.json") if is_scq_quiz is False else get_path("choice_quiz_schema.json")

        with open(quiz_prompt_path, 'r') as p:
            quiz_prompt_template = p.read()

        with open(quiz_json_schema_path, 'r') as s:
            quiz_response_schema = s.read()

        prompt = quiz_prompt_template.format_map({'number_of_questions': 5, 'json_schema': quiz_response_schema,
                                                  'text': request})

        return self.gpt_query(prompt, json_response=True, temperature=0.5)









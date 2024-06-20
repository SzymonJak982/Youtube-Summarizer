from openai import OpenAI
import os
import time
import textwrap


class Summarizer:
    # TODO: Menage downstream processing and warnings with this class
    def __init__(self, config):
        self.config = config
        self.warning = None

    def gpt_query(self, request):

        os.environ['OPENAI_API_KEY'] = self.config
        client = OpenAI()
        counter = 0
        max_retries = 5

        while True:
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo-0125",
                    temperature=0,
                    # response_format={"type": "json_object"},
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant"},
                        {"role": "user", "content": request}
                    ],
                    stop="END_SUMMARY"
                )
                return response.choices[0].message.content

            except Exception:
                counter += 1
                if counter <= max_retries:
                    time.sleep(1)
                else:
                    self.warning = "Sorry, there was a problem with connecting to OpenAI API"
                    return False

    @staticmethod
    def chunker(text, chunk_length):
        return textwrap.wrap(text, chunk_length)

    def paragraph_summarize_query(self, transcript):
        chunks = Summarizer.chunker(text=transcript, chunk_length=8000)

        with open('gpt_prompt', 'r') as prompt:
            gpt_prompt_template = prompt.read()

        result = []
        count = 0

        for chunk in chunks:
            count = count + 1
            current_paragraph = chunk
            prompt = gpt_prompt_template.format_map({'paragraph': current_paragraph})
            summary = self.gpt_query(prompt)

            if self.warning:
                return False

            #TODO: Handle state logging to streamlit
            print('\n\n\n', count, 'of', len(chunks), summary)
            result.append(summary)

        return ' '.join(result)





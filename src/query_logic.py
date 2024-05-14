import re
from openai import OpenAI
import os
import time
import textwrap

#TODO Add a class for Query
def ai_summarization(transcript, openai_api_key):
    # TODO! Optimise in context keyword check- nonsense reduction
    models = {'gpt_3': "gpt-3.5-turbo-0125", "gpt_4": "gpt-4-0125-preview"}

    with open('gpt_prompt', 'r') as prompt:
        gpt_prompt = prompt.read()

    os.environ['OPENAI_API_KEY'] = openai_api_key

    def gpt_query(request, model):
        """'
        :param model- gpt_3' or 'gpt_4'
        :param request- any query
         """
        client = OpenAI()
        # os.environ.get('OPENAI_API_KEY')
        model = models[str(model)]
        # start_time = time.time()

        counter = 0
        max_retries = 5

        while True:
            try:
                response = client.chat.completions.create(
                    model=model,
                    temperature=0,
                    # response_format={"type": "json_object"},
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant"},
                        {"role": "user", "content": request}
                    ],
                    stop="END_SUMMARY"
                )
                return response.choices[0].message.content

            except Exception as e:
                counter += 1
                if counter <= max_retries:
                    time.sleep(1)
                else:
                    warning = "Sorry, there was a problem with connecting to OpenAI API"
                    return None, warning

    def naive_chunker(text, chunk_length):
        return textwrap.wrap(text, chunk_length)

    # chunks_as_list = naive_chunker(transcript, 8000)

    def naive_paragraph_summarizer(gpt_model, query):
        """Possibly more params needed."""
        chunks = naive_chunker(text=transcript, chunk_length=8000)
        result = list()
        count = 0
        for chunk in chunks:
            count = count + 1
            current_paragraph = chunk
            prompt = query.format_map({'paragraph': current_paragraph})
            summary = gpt_query(prompt, model=gpt_model)

            if isinstance(summary, tuple):
                warning = None, "Couldn't connect to openAI."
                return warning

            #TODO: Handle state logging to streamlit
            print('\n\n\n', count, 'of', len(chunks), summary)
            result.append(summary)

        return ' '.join(result), None # if result[0] is not tuple else result[0]

    return naive_paragraph_summarizer(gpt_model='gpt_3', query=gpt_prompt)



# gpt_query(request = query, model= 'gpt_3')




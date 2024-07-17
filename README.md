# Youtube-Summarizer App

<img src="https://github.com/SzymonJak982/Youtube-Summarizer/blob/main/logo.png?raw=true" alt="Project Logo" width="200" height="200" title="Project Logo">


The YouTube Summarizer App is a simple Python app providing detailed, college-like notes for YouTube videos. It's ideal for students, researchers, or anyone looking to extract concise, informative summaries from educational videos. The app runs locally using FastAPI for backend and Streamlit for user interface. It is also equipped with Docker support for easy deployment.

## Features

- **Video Summarization**: Converts YouTube transcript into detailed text notes using GPT model.
- **Saving summaries**: Utilizes SQLAlchemy for efficient data storage. 
- **Streamlit Interface**: User-friendly web interface for easy operation.
- **Docker Integration**: Supports Docker for straightforward setup.

## Latest updates
*17.07.2024:*
- **Quiz mode**- added option of exploratory question/answer generation
### Current development:
   - Enhancing transcript generation functionality using Whisper 
   - Quiz-mode- creating interactive quiz experience for the user, using questions generated from summary

## Prerequisites

Before you begin, ensure you have the following:
- Python 3.8 or higher
- Docker (optional, for Docker setup)
- An API key from OpenAI (the app uses GPT-3.5 model)

## Setup Instructions

### Without Docker

1. **Clone the Repository**
   
```bash
git clone https://github.com/SzymonJak982/Youtube-Summarizer.git
cd Youtube-Summarizer
```
2. **Create a virtual environment in Python and activate it**:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
   
  ```bash
  pip install -r requirements.txt
  ```
4. **Get your OpenAI API key**
To get the necessary API key, follow these steps:

    1. Go to the [OpenAI platform website](https://platform.openai.com/docs/overview)
    2. If you don't have an account, click "Sign up" and create one.
    3. Once logged in, navigate to the API key management page.
    4. Click "Create new secret key" and note down the generated API key (you would not see the key again).

5. **Run the App**
   
  ```bash
  streamlit run app.py
 ```
6. **In another terminal window, activate history endpoint with uvicorn (for summary history)**

 ```bash
  uvicorn src.endpoints.endpoints:app --reload
 ```  

### Using Docker

1. **Clone the Repository**

```bash
git clone https://github.com/SzymonJak982/Youtube-Summarizer.git
cd Youtube-Summarizer
```

3. **Build and start the service**
   
```bash
docker-compose up --build
```

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests, or open an issue to suggest features or report bugs.
Here are some of the possible contribution ideas:
- Adopt local LLM for more independency from OpenAI, e.g. using [Mixtral model](https://huggingface.co/cognitivecomputations/dolphin-2.6-mixtral-8x7b)
- Develop transcript fetching from other platforms with API calls as well as webscraping if needed
- Develop asynchronious approach to summary generation to speed up the process for long transcripts 

## Licence

This project is under Apache-2.0 License. If you wish to use it in your own project you should credit the orginal owner.  

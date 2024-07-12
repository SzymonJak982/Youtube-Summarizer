# Youtube-Summarizer App

<img src="https://github.com/SzymonJak982/Youtube-Summarizer/blob/main/logo.png?raw=true" alt="Project Logo" width="200" height="200" title="Project Logo">


The YouTube Summarizer App is a simple Python app providing detailed, college-like notes for YouTube videos. It's ideal for students, researchers, or anyone looking to extract concise, informative summaries from educational videos. The app runs locally using FastAPI for backend and Streamlit for user interface. It is also equipped with Docker support for easy deployment.

## Features

- **Video Summarization**: Converts YouTube transcript into detailed text notes using GPT model.
- **Saving summaries**: Utilizes SQLAlchemy for efficient data storage. 
- **Streamlit Interface**: User-friendly web interface for easy operation.
- **Docker Integration**: Supports Docker for straightforward setup.

## Latest updates
*01.07.2024:*
- *Summary history: Summarizer can now also store created summaries in local sqlite session*
- *Currently working on setting up a Whisper model locally to enhance transcript generation*
### Current development:
   - enhancing transcript generation functionality using Whisper 
   - generation time optimisation using async logic for API calls and Tenacity 

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

3. **Install dependencies**
   
  ```bash
  pip install -r requirements.txt
  ```

3. **Run the App**
   
  ```bash
  streamlit run app.py
 ```
4. **In another terminal window, activate history endpoint with uvicorn**

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

## Licence

Apache-2.0 License

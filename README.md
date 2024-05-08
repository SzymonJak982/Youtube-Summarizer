# Youtube-Summarizer App

The YouTube Summarizer App provides detailed, college-like notes for YouTube videos. It's ideal for students, researchers, or anyone looking to extract concise, informative summaries from educational videos. The app runs locally using Streamlit and is equipped with Docker support for easy deployment.

## Features

- **Video Summarization**: Converts YouTube transcript into detailed text notes using GPT model.
- **Streamlit Interface**: User-friendly web interface for easy operation.
- **Docker Integration**: Supports Docker for straightforward setup and scalability.

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

2. **Install dependencies**
  ```bash
  pip install -r requirements.txt
  ```

3. **Run the App**
  ```bash
  streamlit run app.py
 ```

### Using Docker

1. **Clone the Repository**
   ```bash
   git clone https://github.com/SzymonJak982/Youtube-Summarizer.git 
   cd Youtube-Summarizer
   ```

2. **Build and start the service**
   ```bash
   docker-compose up --build
   ```

# Youtube-Summarizer App

<img src="https://github.com/SzymonJak982/Youtube-Summarizer/blob/main/logo.png?raw=true" alt="Project Logo" width="200" height="200" title="Project Logo">


The YouTube Summarizer App provides detailed, college-like notes for YouTube videos. It's ideal for students, researchers, or anyone looking to extract concise, informative summaries from educational videos. The app runs locally using Streamlit and is equipped with Docker support for easy deployment.

## Features

- **Video Summarization**: Converts YouTube transcript into detailed text notes using GPT model.
- **Streamlit Interface**: User-friendly web interface for easy operation.
- **Docker Integration**: Supports Docker for straightforward setup and scalability.

## Latest updates
*14.05:*
- *Summary history: Summarizer can now also store created summaries in the current browser session*
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

MIT License

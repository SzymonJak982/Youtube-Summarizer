import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)

# TODO: Ensure it works correctly when run with Docker
STATIC_FILE_DIR = os.path.join(PROJECT_DIR, "src/prompts_and_schemas")

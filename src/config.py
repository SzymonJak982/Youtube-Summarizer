import os


class Config():
    API_URL = os.getenv('API_URL', 'http://localhost:8000/summaries')


class Production(Config):
    # For future Azure App Service Deployment
    pass
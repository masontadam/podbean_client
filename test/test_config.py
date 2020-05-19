from dotenv import load_dotenv
import os

app_dir = os.path.abspath(os.path.dirname(__file__))
env_path = os.path.join(app_dir, '..', '.env')
load_dotenv(dotenv_path=env_path)

class TestConfig():
    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET') 
    REDIRECT_URI = os.environ.get('REDIRECT_URI')
    SCOPES = [i for i in os.environ.get('SCOPES').split(' ')]
    EMAIL = os.environ.get('EMAIL')
    PASSWORD = os.environ.get('PASSWORD')

    CALLBACK_URI = ''
    ACCESS_TOKEN = ''
    STATE = ''

    AUDIO_KEY = ''
    IMAGE_KEY = ''
    EID = ''

    AUTH_BASE_URL = 'https://api.podbean.com/v1/dialog/oauth'
    TOKEN_URL = 'https://api.podbean.com/v1/oauth/token'
    PODCAST_URL = 'https://api.podbean.com/v1/podcasts'
    EPISODES_URL = 'https://api.podbean.com/v1/episodes'
    AUTH_UPLOAD_BASE_URL = 'https://api.podbean.com/v1/files/uploadAuthorize'

from podbean_client import PodBeanClient
from test_config import TestConfig as test
import test_utils as utils
import requests
import pytest
import flask
import os

def test_unititialized_object():
    client = PodBeanClient()

    assert client.client_id == None
    assert client.client_secret == None
    assert client.scopes == None
    assert client.redirect_uri == None

def test_static_variables():
    client = PodBeanClient()

    assert client.auth_base_url == test.AUTH_BASE_URL
    assert client.token_url == test.TOKEN_URL
    assert client.podcast_url == test.PODCAST_URL
    assert client.episodes_url == test.EPISODES_URL 
    assert client.auth_upload_base_url == test.AUTH_UPLOAD_BASE_URL

def test_initialized_object():
    client = PodBeanClient(client_id=test.CLIENT_ID, 
        client_secret=test.CLIENT_SECRET, 
        scopes=test.SCOPES, 
        redirect_uri=test.REDIRECT_URI)

    assert client.client_id == test.CLIENT_ID
    assert client.client_secret == test.CLIENT_SECRET
    assert client.scopes == test.SCOPES
    assert client.redirect_uri == test.REDIRECT_URI

def test_flask_init_app():
    app = flask.Flask(__name__)

    app.config['CLIENT_ID'] = test.CLIENT_ID
    app.config['CLIENT_SECRET'] = test.CLIENT_SECRET
    app.config['SCOPES'] = test.SCOPES
    app.config['REDIRECT_URI'] = test.REDIRECT_URI

    client = PodBeanClient()
    client.init_app(app)

    assert client.client_id == test.CLIENT_ID
    assert client.client_secret == test.CLIENT_SECRET
    assert client.scopes == test.SCOPES
    assert client.redirect_uri == test.REDIRECT_URI

    with pytest.raises(ValueError):
        app.config['CLIENT_ID'] = None
        assert client.init_app(app)

    with pytest.raises(ValueError):
        app.config['CLIENT_SECRET'] = None
        assert client.init_app(app)

    with pytest.raises(ValueError):
        app.config['SCOPES'] = None
        assert client.init_app(app)

    with pytest.raises(ValueError):
        app.config['REDIRECT_URI'] = None
        assert client.init_app(app)


def test_get_authorization_url():
    client = PodBeanClient(client_id=test.CLIENT_ID, 
        client_secret=test.CLIENT_SECRET, 
        scopes=test.SCOPES, 
        redirect_uri=test.REDIRECT_URI)
    auth_url, state = client.get_authorization_url()

    correct_url = (
    f'https://api.podbean.com/v1/dialog/oauth?response_type=code&'
    f'client_id={test.CLIENT_ID}&'
    f'redirect_uri=https%3A%2F%2F127.0.0.1%3A5000%2Fpodbeancallback&'
    f'scope=podcast_read+podcast_update+episode_publish+episode_read&'
    f'state={state}'
    )

    assert auth_url == correct_url

def test_get_auth_token():
    client = PodBeanClient(client_id=test.CLIENT_ID, 
        client_secret=test.CLIENT_SECRET, 
        scopes=test.SCOPES, 
        redirect_uri=test.REDIRECT_URI)
    auth_url, test.STATE = client.get_authorization_url()

    # perform podbean account login actions
    utils.podbean_login(test, client, auth_url)

    response = client.get_auth_token(test.CALLBACK_URI, test.STATE)

    correct_keys = ['access_token', 'expires_in', 'token_type', 'scope',
    'refresh_token', 'expires_at']

    assert list(response.keys()) == correct_keys

    test.ACCESS_TOKEN = response['access_token']

def test_upload_file():
    client = PodBeanClient(client_id=test.CLIENT_ID, 
        client_secret=test.CLIENT_SECRET, 
        scopes=test.SCOPES, 
        redirect_uri=test.REDIRECT_URI)

    # Test audio/mpeg
    with open('test.mp3', 'wb') as f:
        # 10mb file
        f.seek(10485760-1)
        f.write(b'\0')
        f.close()
    with open('test.mp3', 'rb') as f:
        mp3_response = client.upload_file(test.ACCESS_TOKEN, f, 'test.mp3', 
            10485760-1, 'audio/mpeg')
        f.close()

    # Test image/jpeg
    with open('test.jpg', 'wb') as f:
        # 10mb file
        f.seek(1048576-1)
        f.write(b'\0')
        f.close()
    with open('test.jpg', 'rb') as f:
        jpg_response = client.upload_file(test.ACCESS_TOKEN, f, 'test.jpg', 
            10485760-1, 'image/jpeg')
        f.close()
            
    # Test image/png
    with open('test.png', 'wb') as f:
        # 10mb file
        f.seek(1048576-1)
        f.write(b'\0')
        f.close()
    with open('test.png', 'rb') as f:
        png_response = client.upload_file(test.ACCESS_TOKEN, f, 'test.png', 
            10485760-1, 'image/png')
        f.close()

    assert mp3_response[0].status_code == requests.codes.ok
    assert jpg_response[0].status_code == requests.codes.ok
    assert png_response[0].status_code == requests.codes.ok

    test.AUDIO_KEY = mp3_response[1]
    test.IMAGE_KEY = jpg_response[1]

def test_get_all_episodes():
    client = PodBeanClient(client_id=test.CLIENT_ID, 
        client_secret=test.CLIENT_SECRET, 
        scopes=test.SCOPES, 
        redirect_uri=test.REDIRECT_URI)

    episodes = client.get_all_episodes(test.ACCESS_TOKEN)

    assert episodes != []

    test.EID = episodes[-1]['id']

def test_get_podcast_info():
    client = PodBeanClient(client_id=test.CLIENT_ID, 
        client_secret=test.CLIENT_SECRET, 
        scopes=test.SCOPES, 
        redirect_uri=test.REDIRECT_URI)

    response = client.get_podcast_info(test.ACCESS_TOKEN)

    assert response.status_code == requests.codes.ok

def test_publish_episode():
    client = PodBeanClient(client_id=test.CLIENT_ID, 
        client_secret=test.CLIENT_SECRET, 
        scopes=test.SCOPES, 
        redirect_uri=test.REDIRECT_URI)

    test_title = "Test Title"
    test_desc = "Test Description"

    response = client.publish_episode(test.ACCESS_TOKEN, test_title, test_desc,
        test.AUDIO_KEY, test.IMAGE_KEY)

    assert response.status_code == requests.codes.ok

def test_update_episode():
    client = PodBeanClient(client_id=test.CLIENT_ID, 
        client_secret=test.CLIENT_SECRET, 
        scopes=test.SCOPES, 
        redirect_uri=test.REDIRECT_URI)

    test_title = "Test Title"
    test_desc = "Test Description"

    response = client.update_episode(test.EID, test.ACCESS_TOKEN, test_title,
        test_desc, test.AUDIO_KEY, test.IMAGE_KEY)
    print(response.content)

    assert response.status_code == requests.codes.ok

def test_cleaup():
    # Cleanup FS
    os.remove('test.mp3')
    os.remove('test.jpg')
    os.remove('test.png')
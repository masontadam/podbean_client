from podbean_client import PodBeanClient
from config import TestConfig as test
import utils
import requests
import pytest
import flask

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

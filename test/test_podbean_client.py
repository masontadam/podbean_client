from podbean_client import PodBeanClient
import flask
import pytest

CLIENT_ID = '123456789'
CLIENT_SECRET = '987654321'
SCOPES = ['podcast_read', 'podcast_update', 'episode_publish', 'episode_read']
REDIRECT_URI = 'https://127.0.0.1:5000/callback'

def test_unititialized_object():
    client = PodBeanClient()

    assert client.client_id == None
    assert client.client_secret == None
    assert client.scopes == None
    assert client.redirect_uri == None

def test_static_variables():
    client = PodBeanClient()

    assert client.auth_base_url == 'https://api.podbean.com/v1/dialog/oauth'
    assert client.token_url == 'https://api.podbean.com/v1/oauth/token'
    assert client.podcast_url == 'https://api.podbean.com/v1/podcasts'
    assert client.episodes_url == 'https://api.podbean.com/v1/episodes'
    assert client.auth_upload_base_url == 'https://api.podbean.com/v1/files/uploadAuthorize'

def test_initialized_object():
    client = PodBeanClient(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, 
        scopes=SCOPES, redirect_uri=REDIRECT_URI)

    assert client.client_id == CLIENT_ID
    assert client.client_secret == CLIENT_SECRET
    assert client.scopes == SCOPES
    assert client.redirect_uri == REDIRECT_URI

def test_flask_init_app():
    app = flask.Flask(__name__)

    app.config['CLIENT_ID'] = CLIENT_ID
    app.config['CLIENT_SECRET'] = CLIENT_SECRET
    app.config['SCOPES'] = SCOPES
    app.config['REDIRECT_URI'] = REDIRECT_URI

    client = PodBeanClient()
    client.init_app(app)

    assert client.client_id == CLIENT_ID
    assert client.client_secret == CLIENT_SECRET
    assert client.scopes == SCOPES
    assert client.redirect_uri == REDIRECT_URI

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
    client = PodBeanClient(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, 
        scopes=SCOPES, redirect_uri=REDIRECT_URI)

    url = 'https://api.podbean.com/v1/dialog/oauth?response_type=code&' \
    'client_id=123456789&redirect_uri=https%3A%2F%2F127.0.0.1%3A5000%2F' \
    'callback&scope=podcast_read+podcast_update+episode_publish+episode_read&' \
    'state={}'

    auth_url, state = client.get_authorization_url()

    assert url.format(state) == auth_url

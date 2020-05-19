from requests_oauthlib import OAuth2Session
import requests

class PodBeanClient(object):
    # PodBean API Enpoints
    auth_base_url = 'https://api.podbean.com/v1/dialog/oauth'
    token_url = 'https://api.podbean.com/v1/oauth/token'
    podcast_url = 'https://api.podbean.com/v1/podcasts'
    episodes_url = 'https://api.podbean.com/v1/episodes'
    auth_upload_base_url = 'https://api.podbean.com/v1/files/uploadAuthorize'

    def __init__(self, client_id=None, client_secret=None, scopes=None, redirect_uri=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.scopes = scopes
        self.redirect_uri = redirect_uri

    def init_app(self, app):
        self.client_id = app.config['CLIENT_ID']
        self.client_secret = app.config['CLIENT_SECRET']
        self.redirect_uri = app.config['REDIRECT_URI']
        self.scopes = app.config['SCOPES']

        if self.client_id is None or self.client_secret is None \
            or self.redirect_uri is None or self.scopes is None:
            
            raise ValueError('Must set all of the following app.config values: '
                'CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, and SCOPES. '
                'These values can be found in your PodBean Developer console.')

    def get_authorization_url(self):
        session = OAuth2Session(self.client_id, redirect_uri=self.redirect_uri,
            scope=self.scopes)
        return session.authorization_url(self.auth_base_url)

    def get_auth_token(self, auth_response, state):
        session = OAuth2Session(self.client_id, redirect_uri=self.redirect_uri,
            state=state)
        return session.fetch_token(self.token_url, 
            client_secret=self.client_secret, 
            authorization_response=auth_response)

    def _authorize_upload(self, token, file_name, file_size, content_type):
        params = {
            'access_token' : token,
            'filename' : file_name,
            'filesize' : file_size,
            'content_type' : content_type
        }
        return requests.get(self.auth_upload_base_url, params=params)

    def upload_file(self, token, file, file_name, file_size, content_type):

        response = self._authorize_upload(token, file_name, file_size,
            content_type)

        if response.status_code == requests.codes.ok:
            response_json = response.json()
            presigned_url = response_json['presigned_url']
            expire_at = response_json['expire_at']
            file_key = response_json['file_key']

            headers = {
                'Content-Type': str(content_type),
                'Content-Length': str(file_size)
            }

            return requests.put(presigned_url, data=file, headers=headers), file_key

        else:
            return response

    def get_all_episodes(self, token):
        episode_list = []

        params = {
            'offset' : '0',
            'access_token' : token,
            'limit' : '20'
        }

        has_more = True
        while has_more:
            episodes = requests.get(self.episodes_url, params=params)
            episode_list = episode_list + episodes.json()['episodes']
            params['offset'] = str(int(params['offset']) + int(params['limit']))
            has_more = episodes.json()['has_more']

        return episode_list

    def get_podcast_info(self, token):
        params = {
            'access_token' : token
        }
        return requests.get(self.podcast_url, params=params)

    def publish_episode(self, token, title, desc, media_key, logo_key):
        params = {
            'access_token' : token,
            'title' : title,
            'content' : desc,
            'status' : 'publish',
            'type' : 'public',
            'media_key' : media_key,
            'logo_key' : logo_key
        }
        return requests.post(self.episodes_url, data=params)

    def update_episode(self, eid, token, title, desc, media_key, logo_key):
        params = {
            'access_token' : token,
            'title' : title,
            'content' : desc,
            'status' : 'publish',
            'type' : 'public',
            'media_key' : media_key,
            'logo_key' : logo_key
        }

        return requests.post(self.episodes_url + '/{}'.format(eid), data=params)

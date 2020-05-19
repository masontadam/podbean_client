from podbean_client import PodBeanClient
import requests

def podbean_login(test, client, auth_url):
    s = requests.Session()
    kdowskie = 'kdsowie31j4k1jlf913'

	# Login Page
    response = s.get(auth_url)
    params = {
        kdowskie : s.cookies.get_dict().get(kdowskie),
        'LoginForm[username]' : f'{test.EMAIL}',
        'LoginForm[password]' : f'{test.PASSWORD}',
        'yt0' : ''
    }
    r = s.post(response.url, headers=s.headers, data=params)

    # Authorize Application Page
    start = r.text.find('var data = [{"id":"') + 19
    end = start + 12
    params = {
        'podcast' : r.text[start:end],
        kdowskie : s.cookies.get_dict().get(kdowskie),
        'action' : 'authorize',
        'scopes' : test.SCOPES
    }
    r = s.post(r.url, headers=s.headers, data=params, allow_redirects=False)

    # Set Access Code
    test.CALLBACK_URI = r.headers['Location']

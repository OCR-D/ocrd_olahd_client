from requests_toolbelt.multipart.encoder import MultipartEncoder
from requests import post

class OlaHdClient():

    def __init__(self, endpoint, username, password):
        self.endpoint = endpoint
        self.username = username
        self.password = password
        self.token = None

    def is_logged_in(self):
        return self.token is not None

    def login(self):
        m = MultipartEncoder(fields={
            'password': self.password,
            'username': self.username,
        })
        r = post('%s/login' % self.endpoint, data=m, headers={
            'Accept': 'application/json',
            'Content-Type': m.content_type,
        })
        if r.status_code != 200:
            r.raise_for_status()
        self.token = r.json()['accessToken']

    def post(self, bag_fpath, prev_pid=None):
        if not self.is_logged_in():
            raise Exception("Not logged in")
        fields = {'file': ('file.zip', open(bag_fpath, 'rb'), 'application/vnd.ocrd+zip')}
        if prev_pid:
            fields['prev'] = prev_pid
        m = MultipartEncoder(fields)
        r = post('%s/bag' % self.endpoint, data=m, headers={
            'Authorization': 'Bearer %s' % self.token,
            # 'Accept': 'application/json',
            'Content-Type': m.content_type,
        })
        if r.status_code >= 400:
            r.raise_for_status()
        return r.json()['pid']

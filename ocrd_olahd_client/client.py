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
        r = post('%s/login' % self.endpoint, files={
            'password': ('password', self.password),
            'username': ('username', self.username),
        })
        if r.status_code != 200:
            r.raise_for_status()
        self.token = r.text

    def post_bag(self, bag_fpath, prev_pid=None):
        if not self.is_logged_in():
            raise Exception("Not logged in")
        files = {'file': ('file', bag_fpath)}
        if prev_pid:
            files['prev'] = ('prev', prev_pid)
        return post('%s/bag' % self.endpoint, files)

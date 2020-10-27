import urllib.request, json

class CoreomicsAPI(object):
    _instance = None
    def __new__(cls):
        if cls._instance is None:
#             print('Creating the object')
            cls._instance = super(CoreomicsAPI, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance
    @staticmethod
    def initialize(URL, auth_token):
        instance = CoreomicsAPI()
        instance.URL = URL
        instance.token = auth_token
    def request(self, relative_url, method='GET', data=None):
        url = '{}/server{}'.format(self.URL, relative_url)
        if data:
            params = json.dumps(data).encode('utf8')
            req = urllib.request.Request(url, data=params, method=method)
        else:
            req = urllib.request.Request(url, method=method)
        req.add_header('Authorization', 'Token {}'.format(self.token))
        req.add_header('Content-Type', 'application/json')
        response = urllib.request.urlopen(req)
        return json.loads(response.read())

class SubmissionManager(object):
    @staticmethod
    def get_submissions(querystring=''):
        return CoreomicsAPI().request('/api/submissions/{}'.format(querystring)).get('results')

class Submission(object):
    def __init__(self, submission_data):
        self.data = submission_data
    @property
    def id(self):
        return self.data['id']
    @property
    def project_id(self):
        return self.data['internal_id']
    def update_status(self, status, email=False):
        return CoreomicsAPI().request('/api/submissions/{}/update_status/'.format(self.id), 'POST', {'status':status, 'email': email})
  
  

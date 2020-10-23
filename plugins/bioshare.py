from coreomics.requests import CoreomicsAPI

class SubmissionShare(object):
    def __init__(self, submission_id):
        self.id = submission_id
        self.data = self.get_share()
        self.permissions = None
    @property
    def url(self):
        return self.data.get('url',None) if self.data else None
    def exists(self):
        return self.data is not None
    def get_share(self):
        try:
            return CoreomicsAPI().request('/api/bioshare/submission_shares/{}/'.format(self.id))
        except:
            return None
    def create_share(self):
        if not self.data:
            self.data = CoreomicsAPI().request('/api/bioshare/submission_shares/', 'POST', {'submission': self.id})
    def share(self):
        self.permissions = CoreomicsAPI().request('/api/bioshare/submission_shares/{}/share/'.format(self.id), 'POST', {'submission': self.id})
        return self.permissions
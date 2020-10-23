from coreomics.requests import CoreomicsAPI

class SubmissionShare(object):
    def __init__(self, submission_id):
        self.id = submission_id
        self.share = self.get_share()
    @property
    def url(self):
        return self.share.get('url',None) if self.share else None
    def exists(self):
        return self.share is not None
    def get_share(self):
        try:
            return CoreomicsAPI().request('/api/bioshare/submission_shares/{}/'.format(self.id))
        except:
            return None
    def create_share(self):
        if not self.share:
            self.share = CoreomicsAPI().request('/api/bioshare/submission_shares/', 'POST', {'submission': self.id})

from coreomics.requests import CoreomicsAPI
from os.path import expanduser
import subprocess
# import re

class SubmissionShare(object):
    def __init__(self, submission_id):
        self.id = submission_id
        self.data = self.get_share()
        self.permissions = None
    @property
    def url(self):
        return self.data.get('url',None) if self.data else None
    @property
    def bioshare_id(self):
        return self.data.get('bioshare_id', None) if self.data else None
    @property
    def server(self):
#         return re.match(r'https?:\/\/(.*)\/bioshare\/.*', self.url).groups()[0]
        return self.url.split('//')[1].split('/')[0]
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
    def send_rsync_command(self, source, dest_dir='/', ssh_key='~/.ssh/id_rsa'):
        return ['rsync', '-e', 'ssh -i {}'.format(expanduser(ssh_key)), '-vrtL', '--no-p', '--no-g', '--chmod=ugo=rwX', source, 'bioshare@{}:/{}{}'.format(self.server, self.bioshare_id, dest_dir)]
#         return ['rsync', '-e', 'ssh -i {}'.format(expanduser(ssh_key)), '-vrtL', '--no-p', '--no-g', '--chmod=ugo=rwX', source, '{}{}'.format('bioshare@bioshare.bioinformatics.ucdavis.edu:/m4ym4kux7b7ngi9', dest_dir)]
#         rsync -vrt --no-p --no-g --chmod=ugo=rwX /path/to/my/files bioshare@server.domain.net:/{}/
    def receive_rsync_command(self, dest, source_dir="/", ssh_key='~/.ssh/id_rsa'):
#         rsync -vrt bioshare@server.domain.net:/uqgva457544351l/test/ /to/my/local/directory
        return ['rsync', '-e', 'ssh -i {}'.format(expanduser(ssh_key)), '-vrt', 'bioshare@{}:/{}{}'.format(self.server, self.bioshare_id, source_dir), dest]
#         return ['rsync', '-e', 'ssh -i {}'.format(expanduser(ssh_key)), '-vrt', 'bioshare@bioshare.bioinformatics.ucdavis.edu:/m4ym4kux7b7ngi9{}'.format(source_dir), dest]
    def send_rsync(self, source, dest_dir='/', ssh_key='~/.ssh/id_rsa'):
        return self.rsync(self.send_rsync_command(source, dest_dir, ssh_key))
    def receive_rsync(self, dest, source_dir="/", ssh_key='~/.ssh/id_rsa'):
        return self.rsync(self.receive_rsync_command(dest, source_dir, ssh_key))
    def rsync(self, command):
        print(' '.join(command))
        return subprocess.Popen(command).pid
#         return subprocess.Popen(command, stdout=subprocess.STDOUT, stderr=subprocess.STDOUT)
        
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
    def send_rsync_command(self, source, dest_dir='/', ssh_key='~/.ssh/id_rsa', verbose=False):
        return ['rsync', '-e', 'ssh -i {}'.format(expanduser(ssh_key)), '-rtL'+('v' if verbose else ''), '--no-p', '--no-g', '--chmod=ugo=rwX', source, 'bioshare@{}:/{}{}'.format(self.server, self.bioshare_id, dest_dir)]
    def receive_rsync_command(self, dest, source_dir="/", ssh_key='~/.ssh/id_rsa', verbose=False):
        return ['rsync', '-e', 'ssh -i {}'.format(expanduser(ssh_key)), '-rt'+('v' if verbose else ''), 'bioshare@{}:/{}{}'.format(self.server, self.bioshare_id, source_dir), dest]
    def send_rsync(self, source, dest_dir='/', ssh_key='~/.ssh/id_rsa', logfile=None, verbose=False):
        return self.rsync(self.send_rsync_command(source, dest_dir, ssh_key, verbose=verbose), logfile=logfile)
    def receive_rsync(self, dest, source_dir="/", ssh_key='~/.ssh/id_rsa', logfile=None, verbose=False):
        return self.rsync(self.receive_rsync_command(dest, source_dir, ssh_key, verbose=verbose), logfile=logfile)
    def rsync(self, command, logfile=None):
        print(' '.join(command))
        if logfile:
            with open(logfile,"ab") as out:
                return subprocess.Popen(command, stdout=out, stderr=out).pid
        else:
            return subprocess.Popen(command).pid
        
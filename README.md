# coreomics_api
Python3 libary for making interaction with coreomics API easy

```Python3
from coreomics.requests import CoreomicsAPI, SubmissionManager, Submission

#Initialize the API
CoreomicsAPI.initialize('https://institution.coreomics.com/', 'YOURAPIKEY')  # Create API Key on site under Profile->API Access
#Get submissions
submissions = SubmissionManager.get_submissions('?page=1&page_size=10&search=Pacbio')
#Set some statuses
for submission in submissions: #do something with submissions
    submission = Submission(submission)
    response = submission.update_status(status='Samples Received', email=True)
    print("id: {}, project_id: {}".format(submission.id, submission.project_id), response)
```

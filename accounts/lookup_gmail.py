from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from googleapiclient import errors


from datetime import datetime
from dateutil import tz

from requests import exceptions as requests_errors

from google.auth.exceptions import RefreshError
from .social_auth_credentials import Credentials
from social_django.utils import load_strategy

from .models import JobApplication
import base64

def convertTime(base):

    # METHOD 2: Auto-detect zones:
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    # utc = datetime.utcnow()
    #utc = datetime.strptime('2011-01-21 02:37:21', '%Y-%m-%d %H:%M:%S')
    base = base[:base.index('+0000') - 1]
    utc = datetime.strptime(base, '%a, %d %b %Y %H:%M:%S')
    #Mon, 1 Oct 2018 22:35:03 +0000 (UTC)

    # Tell the datetime object that it's in UTC time zone since
    # datetime objects are 'naive' by default
    utc = utc.replace(tzinfo=from_zone)

    # Convert time zone
    central = utc.astimezone(to_zone)
    return central.strftime('%Y-%m-%d')
    #return central.strftime('%a, %d %b %Y %H:%M:%S %z')

def GetMessage(service, user_id, msg_id, user):
  """Get a Message with given ID.
  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.
  Returns:
    A Message.
  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
    jobTitle = ''
    company = ''
    date = ''
    '''for part in message['payload']['parts']:
        if(part['mimeType'] == 'text/html'):
            print()
            print(base64.urlsafe_b64decode(part['body']['data'].encode('ASCII')))
            print()
            print()'''
    for header in message['payload']['headers']:
        if header['name'] == 'Subject':
            #print('Message subject: %s' % header['value'])
            subject = str(header['value'])
            jobTitle = subject[subject.index('for ') + 4 : subject.index(' at ')]
            company = subject[subject.index('at ') + 3:]
            source = 'LinkedIn'
        elif header['name'] == 'Date':
            date = header['value']
            date = convertTime(str(date))
    if user.is_authenticated:
      inserted_before = JobApplication.objects.all().filter(msgId=msg_id)
      if not inserted_before:
        japp = JobApplication(jobTitle=jobTitle, company=company, applyDate=date, msgId=msg_id, source = source, user = user)
        japp.save()


    ja = JobApplication(jobTitle, company, date)
    return ja
  except errors.HttpError as error:
    print('An error occurred: %s' % error)



def ListMessagesMatchingQuery(service, user_id, query=''):
  """List all Messages of the user's mailbox matching the query.
  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    query: String used to filter messages returned.
    Eg.- 'from:user@some_domain.com' for Messages from a particular sender.
  Returns:
    List of Messages that match the criteria of the query. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate ID to get the details of a Message.
  """
  try:
    response = service.users().messages().list(userId=user_id,
                                               q=query, includeSpamTrash=True).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(userId=user_id, q=query,
                                         pageToken=page_token, includeSpamTrash=True).execute()
      messages.extend(response['messages'])

    return messages
  except errors.HttpError as error:
    print('An error occurred: %s' % error)

def fetchJobApplications(user):
    #initiates Gmail API
    usa = user.social_auth.get(provider='google-oauth2')
    GMAIL = build('gmail', 'v1', credentials=Credentials(usa))

    messages = ListMessagesMatchingQuery(GMAIL, 'me', 'from:jobs-listings@linkedin.com AND subject:You applied for')# AND after:2018/01/01')
    #print('there is ' + str(len(messages)) + ' messages sent from jobs-listings@linkedin.com')

    jobList = []
    for message in messages:
        ja = GetMessage(GMAIL, 'me', message['id'], user)
        jobList.append(ja)

    print(jobList)

from django.core.management.base import BaseCommand, CommandError
from django.views.generic import ListView, DetailView
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('email',type=str)
    def handle(self, *args, **options):
        email = options['email']
        print(email)
        main()
        file_name = 'C:/Users/Lane/Documents/Lift my Python/mysite/wbuilder/templates/wbuilder/workout.html'
        my_email = 'pythonlifter@gmail.com'
        my_passw = 'Tennessee14'
        recipients = email
        subject = 'Your Workout'

        message = MIMEMultipart()
        message['From'] = my_email
        message['To'] = recipients
        message['Subject'] = subject

        with open(file_name, 'r') as f:
            body = f.read().replace('{% extends "personal/header.html" %}{% block content %}', '')
            body = body.replace('{% include "wbuilder/includes/checkboxes.html" %}<table class=\"col-sm-8\">',
                                '<table>')
            body = body.replace('<form><tr><td><input type="submit" value="Send Email to Myself" name="Submit" style="color:black"><td></tr></form>',
                                '')
            body = body.replace('{% endblock %}', '')

        message.attach(MIMEText(body, 'html'))

        srv = smtplib.SMTP('smtp.gmail.com:587')
        srv.ehlo()
        srv.starttls()
        srv.login(my_email, my_passw)
        text = message.as_string()
        srv.sendmail(my_email, recipients, text)
        srv.quit()

import httplib2
import os
import oauth2client
from oauth2client import client, tools, file
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googleapiclient import errors, discovery
# import mimetypes
# from email.mime.image import MIMEImage
# from email.mime.audio import MIMEAudio
# from email.mime.base import MIMEBase

import requests

def send_email_mail_gun(subject, html_content, email):
    # Mailgun API key and domain
    API_KEY = ''
    MAILGUN_DOMAIN = 'sandbox0591d3180e704bd385cf8c394f0116f3.mailgun.org'
    
    # Mailgun API endpoint
    MAILGUN_URL = f'https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages'

    # Email details
    sender = str(email)
    recipient = 'shorttail375@gmail.com'
    # Request data
    data = {
        'from': sender,
        'to': recipient,
        'subject': subject,
        'text': "TechGuru",
        'html': html_content,
    }

    # Send the email
    response = requests.post(MAILGUN_URL, auth=('api', API_KEY), data=data)

    if response.status_code == 200:
        print('Email sent successfully!')
    else:
        print('Failed to send email. Status code:', response.status_code)
        print('Response:', response.text)
    return response


# Define the necessary scopes
SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = 'credentials.json'
APPLICATION_NAME = 'Gmail API Python Send Email'

def create_message_html(sender, to, subject, msgHtml, msgPlain):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg.attach(MIMEText(msgPlain, 'plain'))
    msg.attach(MIMEText(msgHtml, 'html'))
    return {'raw': base64.urlsafe_b64encode(msg.as_bytes()).decode()}

def send_message_gmail(sender, to, subject, msgHtml, msgPlain, attachmentFile=None):
    try:
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        print (credential_dir)
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                    'gmail-python-email-send.json')
        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            credentials = tools.run_flow(flow, store)
            print('Storing credentials to ' + credential_path)
        
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)
        if attachmentFile:
            # message1 = createMessageWithAttachment(sender, to, subject, msgHtml, msgPlain, attachmentFile)
            pass
        else: 
            message1 = create_message_html(sender, to, subject, msgHtml, msgPlain)
        # print (message1)
        result = send_message_internal(service, "me", message1)
        return result
    except Exception as e:
        print ("Something went wrong.")
        print (e.args[0])

def send_message_internal(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
        return "Error"
    return "OK"

# Example usage:
def main():
    to = "tech.guru.k.p@gmail.com"
    sender = "tech.guru.k.p@gmail.com"
    subject = "Good job"
    msgHtml = "Hi<br/>Html Email"
    msgPlain = "Hi\nPatrick"
    res = send_message_gmail(sender, to, subject, msgHtml, msgPlain)
    print (res)

if __name__ == '__main__':
    main()
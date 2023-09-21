import requests

def send_email(subject, html_content, email):
    # Mailgun API key and domain
    API_KEY = '1fd41c5f7052ce262455b4f702a96ef1-f0e50a42-d575de17'
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

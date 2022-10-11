import smtplib
import ssl
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

MAIL_CONFIG_FILE = "mail_config.json"

def send_email(subject, sender_name, body, send_to):
    config = read_mail_config()
    MAIL_USER = config['MAIL_USER']
    MAIL_PW = config['MAIL_PW']
    SMTP_SERVER = config['SMTP_SERVER']
    SMTP_PORT = config['SMTP_PORT']


    send_from = f'({sender_name}) {MAIL_USER}'
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = send_from
    msg['To'] = send_to

    msg.attach(MIMEText(body, 'html'))

    try:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        smtp_server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        smtp_server.starttls(context=context)
        smtp_server.login(MAIL_USER, MAIL_PW)
        smtp_server.sendmail(send_from, send_to, msg.as_string())
        print('[INFO] email to', send_to, 'sent successfully')
    except:
        print('[ERROR] sending email to', send_to, 'failed')
    finally:
        smtp_server.close()


def read_mail_config():
    json_string = open(MAIL_CONFIG_FILE, 'r').read()
    return json.loads(json_string)

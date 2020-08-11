import os
from dotenv import load_dotenv
from netmiko import ConnectHandler
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import json
import logging

# Enable logging for debugging but then disable if not needed
# comment out line 12 to turn logging on
logging.basicConfig(level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.CRITICAL)

# load creds from environment variables
load_dotenv()
user = os.environ.get('username')
pw = os.environ.get('password')
sec = os.environ.get('secret')
euser = os.environ.get('eusername')
epw = os.environ.get('epassword')

# Connect
switch = {
    'device_type': 'cisco_ios_telnet',
    'ip': 'IP HERE',
    'username': user,
    'password': pw,
    'secret': sec,
    'port': 23
}
try:
    # using **variable unpacks a python dictionary
    c = ConnectHandler(**switch)

    # Enter enable mode, issue command, and disconnect
    c.enable()
    results = c.send_command('show run')
    c.disconnect()

    # Write output to a file
    filename = f"{switch['ip']}.txt"
    file = open(
        f"/home/fahadLinux/Documents/CodeSamples/Python/Networking/IOS/{filename}", 'w')
    file.write(results)
    file.close()

    # send success email
    s = smtplib.SMTP(host='smtp.office365.com', port=587)
    s.starttls()
    s.login(euser, epw)
    body = f"Backup script succeeded at {datetime.now()}"
    msg = MIMEMultipart()
    msg['From'] = euser
    msg['To'] = euser
    msg['Subject'] = 'Backup script succeeded'
    msg.attach(MIMEText(body, 'plain'))
    s.send_message(msg)
except Exception as e:
    s = smtplib.SMTP(host='smtp.office365.com', port=587)
    s.starttls()
    s.login(euser, epw)
    body = f"{datetime.now()} - Script failed with error: {e}"
    msg = MIMEMultipart()
    msg['From'] = euser
    msg['To'] = euser
    msg['Subject'] = 'Backup script failed'
    msg.attach(MIMEText(body, 'plain'))
    s.send_message(msg)

    # handle Teams message
    url = 'URL HERE'
    message = {
        'title': 'BACKUP FAILED',
        'text': 'The backup script did not succeed. Please research'
    }
    response_body = requests.post(url=url, data=json.dumps(message))

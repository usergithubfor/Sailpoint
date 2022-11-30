import json
import requests
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import smtplib

owner = 'freecodecamp'
repo = 'freecodecamp'
auth_user = 'github_user_name'
auth_access_token = 'github_access_token'

response = requests.get('https://api.github.com/repos/freecodecamp/freecodecamp/pulls?q=+type:pr+sort=created&order=asc&state=all&page={page}', auth=({auth_user}, {auth_access_token}))
list_pr=response.json()

with open("output.json", 'w') as f:
    json.dump(list_pr, f)

#Creating a Dataframe out of json file
df = pd.read_json(r'output.json')
df1 = df[['url', 'state', 'title', 'created_at', 'number' ]]
#csv creation
df1.to_csv(r'final.csv', index = None)


#Email Function
def send_mail():
    # Create a multipart message
    msg = MIMEMultipart()
    body_part = MIMEText('Kindly find the attached file for your reference of current pull requests', 'plain')
    msg['Subject'] = 'Pull Requests Status'
    msg['From'] = 'sender_address'
    msg['To'] = 'receiver_address'
    smtp_user = 'email_user'
    smtp_app_pass = 'mail_server_authentication_app_token'
    # Add body to email
    msg.attach(body_part)
    # open and read the CSV file in binary
    with open('final.csv','rb') as file:
    # Attach the file with filename to the email
        msg.attach(MIMEApplication(file.read(), Name='final.csv'))

    # Create SMTP object
    try:
        smtp_obj = smtplib.SMTP_SSL('smtp.gmail.com')
        smtp_obj.starttls
        # Login to the server
        smtp_obj.login(smtp_user, smtp_app_pass)
        smtp_obj.sendmail(msg['From'], msg['To'], msg.as_string())
        smtp_obj.quit()
    except:
        print("Connection Unsuccessful")
send_mail()

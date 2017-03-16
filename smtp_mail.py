#-*- coding: utf-8 -*-
#!/usr/bin/env python3

import os
import datetime
import smtplib
import base64
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import COMMASPACE, formatdate
from email.header import Header

SENDER_ADDTESS = 'sunjingyi@memect.co'
SENDER_USERNAME = 'sunjingyi@memect.co'
SENDER_PSW = raw_input('Enter your psw: ')
SENDER_SERVER = 'smtp.mxhichina.com'

image_path = './image2.png'
image_id = 'image1'

def construct_mail(send_from, send_to, subject, text, html, files=None):
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = Header(COMMASPACE.join(send_to).encode('utf8'), 'utf8').encode()
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text, 'plain'))
    msg.attach(MIMEText(html, 'html'))

    # attach img
    with open(image_path, 'rb') as f:
        msg_image = MIMEImage(f.read())
    msg_image.add_header('Content-ID', '<{}>'.format(image_id))
    msg.attach(msg_image)

    if files is not None and files:
        for f in files or []:
            with open(f['path'], "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=os.path.basename(f['name'])
                )
                part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(f['name'])
                msg.attach(part)

    return msg.as_string()

def send_mail_to(server, username, password, send_from, send_to, msg):
    print(str(datetime.datetime.now()))
    try:
        smtpserver = smtplib.SMTP_SSL(server)
        smtpserver.ehlo()
        smtpserver.login(username, password)
        smtpserver.sendmail(send_from, send_to, msg)
        print("Successfully sent email")
        smtpserver.close()
        return True
    except Exception as inst:
        print(inst.args)
        print(inst)
        print("Error: unable to send email")
    return False

def send_mail(to_address, subject, text_body='', html_body=''):
    
    server = SENDER_SERVER
    username = SENDER_USERNAME
    password = SENDER_PSW
    sender_address = SENDER_ADDTESS
    # add multiple attachment
    msg = construct_mail(sender_address, [to_address], subject, text_body, html_body)
    send_mail_to(server, username, password, sender_address, [to_address], msg)

def main():

    # load html template
    with open("./invitation.html", "r") as f:
        html_text = f.read()

    # embed image into html use cid mark
    html_text = html_text.replace("_IMAGE_SRC", "cid:{}".format(image_id))

    send_mail('714350847@qq.com', '金融知识图谱论坛报名确认', 'Hello', html_text)

if __name__ == '__main__':
    main()

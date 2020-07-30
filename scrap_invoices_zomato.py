"""
Python 2.7/3.6 compatible
GMAIL Accounts
A script to download email attachments from specific email addresses
Please edit the following details to work:
YOUR_EMAIL_ADDRESS
YOUR_EMAIL_PASSWORD
LABEL - Inbox, Trash, Archive, ...
RECEIVING_EMAIL_ADDRESS
RECEIVING_SUBJECT - '*' for all OR 'Title of Subject'
On imap search params:
Remove the parameters you don't require for a general search
"""
import datetime
import email
import getpass
import imaplib
import os
import sys
import time
import imgkit

detach_dir = '.'

imapSession = imaplib.IMAP4_SSL('imap.gmail.com')
typ, accountDetails = imapSession.login('test@gmail.com', 'sample1234')
imapSession.select()
typ, data = imapSession.search(None, '(SUBJECT "Your Zomato order from")')
print(typ, data)
print('Search...')
counter = 0
REMOTE_TIME_ZONE_OFFSET = +5.5 * 60 * 60
for msgId in data[0].split():
    typ, messageParts = imapSession.fetch(msgId, '(RFC822)')
    emailBody = messageParts[0][1]
    raw_email_string = emailBody.decode('utf-8')
    mail = email.message_from_string(raw_email_string)  #
    for part in mail.walk():
        if part.get_content_type() not in 'text/html'or datetime.datetime.fromtimestamp(
                time.mktime((email.utils.parsedate(
                    mail['Date']))) + time.timezone + REMOTE_TIME_ZONE_OFFSET).today().weekday() > 4:
            # print(part.as_string())
            continue
        # fileName = part.get_filename()
        fileName = datetime.datetime.fromtimestamp(
            time.mktime((email.utils.parsedate(mail['Date']))) + time.timezone + REMOTE_TIME_ZONE_OFFSET).strftime(
            '%d-%m-%Y')
        if bool(fileName):
            filePath = os.path.join(detach_dir, 'attachments', fileName + '.jpg')
            if not os.path.isfile(filePath):
                counter = 0
            else:
                counter += 1
                fileName += '_' + repr(counter)
            filePath = os.path.join(detach_dir, 'attachments', fileName + '.jpg')
            # print(filePath)
            imgkit.from_string(part.get_payload(decode=True).decode(), filePath)
            # import re
            #
            # url = re.search("(?P<url>https?://[^\s]+receipt[^\\\"^'\s]+)", part.get_payload(decode=True).decode()).group(
            #     "url")
            # print(url)
            # import urllib.request
            #
            # urllib.request.urlretrieve(url, filePath)

            # import pdfplumber
            # pdf = pdfplumber.open(filePath)
            # page = pdf.pages[0]
            # text = page.extract_text()
            # pdf.close()
            #
            # # if 'temporary issue' in text:
            # #     print (url)
            # #     os.remove(filePath)
            #
            # if 'reception' not in text:
            #     print (filePath)
            #     os.remove(filePath)

imapSession.close()
imapSession.logout()

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
import imaplib
import os
import time

detach_dir = '.'
# if 'attachments' not in os.listdir(detach_dir):
#     os.mkdir('attachments')

imapSession = imaplib.IMAP4_SSL('imap.gmail.com')
typ, accountDetails = imapSession.login('test@gmail.com', 'sample1234')
imapSession.select()
typ, data = imapSession.search(None, '(SUBJECT "CureFit: Confirmation for OrderId")')
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
        if part.get_content_type() not in 'application/pdf' or 'attachment' not in part.get('Content-Disposition', ''):
            # print(part.as_string())
            continue
        # fileName = part.get_filename()
        # https://www.stackoverflow.com/a/1790885/11548682
        fileName = datetime.datetime.fromtimestamp(time.mktime((email.utils.parsedate(mail['Date']))) + time.timezone - REMOTE_TIME_ZONE_OFFSET).strftime('%d-%m-%Y')
        if bool(fileName):
            filePath = os.path.join(detach_dir, 'attachments', fileName + '.pdf')
            if not os.path.isfile(filePath):
                counter = 0
            else:
                counter += 1
                fileName += '_' + repr(counter)
            filePath = os.path.join(detach_dir, 'attachments', fileName + '.pdf')
            print(fileName)
            fp = open(filePath, 'wb')
            fp.write(part.get_payload(decode=True))
            fp.close()
            print('fp closed ...')

imapSession.close()
imapSession.logout()

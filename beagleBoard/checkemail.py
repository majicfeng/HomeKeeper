#!/usr/bin/python3

from imapclient import IMAPClient
import time
import pdb
#pdb.set_trace()
import Adafruit_BBIO.GPIO as GPIO

DEBUG = True

HOSTNAME = 'imap.gmail.com'
USERNAME = 'homewestvillageh@gmail.com'
PASSWORD = 'hackathon2017'
MAILBOX = 'INBOX'

NEWMAIL_OFFSET = -1   # my unread messages never goes to zero, yours might
MAIL_CHECK_FREQ = 3 # check mail every 60 seconds

bedroom = "P9_23"
livingroom = "P9_27"
GPIO.setup(bedroom, GPIO.OUT) #bedroom
GPIO.setup(livingroom, GPIO.OUT) #livingroom
LAST_UNSEEN_ID = -1
def checklasttitle(server):
    res = server.search('UNSEEN')
    if len(res) > 0 and LAST_UNSEEN_ID!=max(res):
        #new email
        response = server.fetch([max(res)], ['ENVELOPE'])[max(res)]
        for name, data in response.items():
                #pdb.set_trace()
                if(name==b"ENVELOPE"):
                        sub = data.subject
                        if sub is None:
                            return
                        else:
                            sub = sub.decode("ascii")
                        print (sub)
                        if sub.find("on")!= -1:
                                turnonlight(sub)
                        elif sub.find("off")!= -1:
                                turnofflight(sub)
                        else:
                                pass

        #server.fetch([2], [b'ENVELOPE'])[2][b'ENVELOPE'].subject

def turnonlight(sub):
    if sub.find("living"):
        #pdb.set_trace()
        GPIO.output(livingroom, GPIO.HIGH)
    elif sub.find("bedroom"):
        GPIO.output(bedroom, GPIO.HIGH)
    else:
        GPIO.output(bedroom, GPIO.HIGH)
        GPIO.output(livingroom, GPIO.HIGH)


def turnofflight(sub):
    if sub.find("living"):
        GPIO.output(livingroom, GPIO.LOW)
    elif sub.find("bedroom"):
        GPIO.output(bedroom, GPIO.LOW)
    else:
        GPIO.output(livingroom, GPIO.LOW)
        GPIO.output(bedroom, GPIO.LOW)

server = IMAPClient(HOSTNAME, use_uid=True, ssl=True)
server.login(USERNAME, PASSWORD)
def loop():
    #server = IMAPClient(HOSTNAME, use_uid=True)
    global server
    if DEBUG:
        print('Logging in as ' + USERNAME)
        select_info = server.select_folder(MAILBOX)
        print('%d messages in INBOX' % select_info[b'EXISTS'])
    folder_status = server.folder_status(MAILBOX, 'UNSEEN')
    newmails = int(folder_status[b'UNSEEN'])
    checklasttitle(server)

    if DEBUG:
        print ("You have", newmails, "new emails!")

    #if newmails > NEWMAIL_OFFSET:
    #    GPIO.output("P9_12", GPIO.HIGH)

    #else:
    #    GPIO.output("P9_12", GPIO.LOW)

    time.sleep(MAIL_CHECK_FREQ)

if __name__ == '__main__':
    try:
        print ('Press Ctrl-C to quit.')
		print ('Press Ctrl-C to quit.')
        GPIO.output(livingroom, GPIO.LOW)
        GPIO.output(bedroom, GPIO.LOW)
        while True:
            loop()
    finally:
        GPIO.cleanup()


#!/usr/bin/python3

from evdev import InputDevice, categorize, ecodes
from select import select
import smtplib

dev = InputDevice('/dev/input/event1')

print(dev)

fromaddr = 'homewestvillageh@gmail.com'
toaddrs  = 'shen.feng04@gmail.com'
msg = 'Subject: Alert! Break in'


# Credentials (if needed)
username = 'homewestvillageh@gmail.com'
password = 'hackathon2017'

# The actual mail send
status = 0
while True:
   global status
   r,w,x = select([dev], [], [])
   for event in dev.read():
       if event.type == ecodes.EV_KEY:
           if status == 0:
               server = smtplib.SMTP('smtp.gmail.com:587')
               server.starttls()
               server.login(username,password)
               server.sendmail(fromaddr, toaddrs, msg)
               server.quit()
               status = 1

           print(categorize(event))

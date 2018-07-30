#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Push a key combination to a list of Cisco Phones
import base64
import requests
#To disable the warning "InsecureRequestWarning: Unverified HTTPS request is being made"
#in requests using urllib3,  it's needed to import the specific instance of the module
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import time
#phone 7911
# phone_url = 'http://'+authentication+'10.9.44.26/CGI/Execute'
authentication = 'orange7911:12345@'
phone_url = 'http://'+authentication+'{0}/CGI/Execute'
# Dictionary containing headers for the request
headers = {
  'SoapAction':'CUCM:DB ver=9.1',
  'Authorization': 'Basic ', 
  'Content-Type': 'text/xml; charset=utf-8'
}
# key_array.append('XML=<CiscoIPPhoneExecute><ExecuteItem URL="Key:Settings"/></CiscoIPPhoneExecute>'
# key_array.append('XML=<CiscoIPPhoneExecute><ExecuteItem URL="Key:Soft4"/></CiscoIPPhoneExecute>')

# Keys to be sent

key_array =['Applications']
key_array.append('KeyPad3')
key_array.append('KeyPad4')
key_array.append('KeyPad5')

unlock =['KeyPadStar']
unlock.append('KeyPadStar')
unlock.append('KeyPadPound')

erase = ['KeyPad2']
erase.append('Soft4')
erase.append('Soft2')

execute = 'XML=<CiscoIPPhoneExecute><ExecuteItem URL="Key:{0}"/></CiscoIPPhoneExecute>'



def push(keys):
  push = requests.post(phone_url, headers=headers, data=keys) 
  response = push.text
  print(response)
  return

with open('ip_7911.txt') as f:
    content = f.readlines()

content = [x.strip() for x in content]

for line in content:
  phone_url = phone_url.format(line)
  for x in key_array:
    key = execute.format(x)
    push(key)
    time.sleep(0.3)

  time.sleep(2)
  
  for y in unlock:
    key = execute.format(y)
    push(key)
    time.sleep(0.3)

  time.sleep(0.2)

  for z in erase:
    key = execute.format(z)
    push(key)
    time.sleep(0.3)
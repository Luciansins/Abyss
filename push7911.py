#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Push a key combination to a list of Cisco Phones
import requests
from queue import Queue
from threading import Thread
# To disable the warning "InsecureRequestWarning: Unverified HTTPS request is being made"
# in requests using urllib3,  it's needed to import the specific instance of the module
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import time

# phone 7911
# phone_url = 'http://'+authentication+'10.9.44.26/CGI/Execute'
authentication = 'orange7911:12345@'
phone_url = 'http://' + authentication + '{0}/CGI/Execute'
# Dictionary containing headers for the request
headers = {
    'SoapAction': 'CUCM:DB ver=9.1',
    'Authorization': 'Basic ',
    'Content-Type': 'text/xml; charset=utf-8'
}
# key_array.append('XML=<CiscoIPPhoneExecute><ExecuteItem URL="Key:Settings"/></CiscoIPPhoneExecute>'
# key_array.append('XML=<CiscoIPPhoneExecute><ExecuteItem URL="Key:Soft4"/></CiscoIPPhoneExecute>')

# Keys to be sent

key_array = ['Applications', 'KeyPad3', 'KeyPad4', 'KeyPad5']

unlock = ['KeyPadStar', 'KeyPadStar', 'KeyPadPound']

erase = ['KeyPad2', 'Soft4', 'Soft2']

execute = 'XML=<CiscoIPPhoneExecute><ExecuteItem URL="Key:{0}"/></CiscoIPPhoneExecute>'


class DownloadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            link = self.queue.get()
            time.sleep(1)
            print(link)
            self.queue.task_done()


def push(keys):
    r = requests.post(phone_url, headers=headers, data=keys)
    response = r.text
    print(response)
    return


with open('ip_7911.txt') as f:
    content = f.readlines()

content = [x.strip() for x in content]

ts = time()
# Create a queue to communicate with the worker threads
queue = Queue()
# Create 8 worker threads
for x in range(8):
    worker = DownloadWorker(queue)
    # Setting daemon to True will let the main thread exit even though the workers are blocking
    worker.daemon = True
    worker.start()
# Put the tasks into the queue as a tuple
for link in content:
    print('Queueing {}'.format(link))
    queue.put(link)
# Causes the main thread to wait for the queue to finish processing all the tasks
queue.join()
print('Took {}'.format(time() - ts))

#
# for line in content:
#     phone_url = phone_url.format(line)
#     for x in key_array:
#         key = execute.format(x)
#         push(key)
#         time.sleep(0.3)
#
#     time.sleep(2)
#
#     for y in unlock:
#         key = execute.format(y)
#         push(key)
#         time.sleep(0.3)
#
#     time.sleep(0.2)
#
#     for z in erase:
#         key = execute.format(z)
#         push(key)
#         time.sleep(0.3)

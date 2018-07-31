#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Push a key combination to a list of Cisco Phones
from queue import Queue
from threading import Thread
from time import time, sleep
import requests
# To disable the warning "InsecureRequestWarning: Unverified HTTPS request is being made"
# in requests using urllib3,  it's needed to import the specific instance of the module
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# <editor-fold desc="Setting">
authentication = 'orange7911:12345@'
phone_url = 'http://' + authentication + '{0}/CGI/Execute'
execute_data = 'XML=<CiscoIPPhoneExecute><ExecuteItem URL="Key:{0}"/></CiscoIPPhoneExecute>'

# Keys to be sent
key_array = ['Applications', 'KeyPad3', 'KeyPad4', 'KeyPad5']
unlock = ['KeyPadStar', 'KeyPadStar', 'KeyPadPound']
erase = ['KeyPad2', 'Soft4', 'Soft2']
# </editor-fold>

# <editor-fold desc="Configuration">
filename = 'ip_7911.txt'
num_worker_threads = 8
# </editor-fold>


class MigrationWorker(Thread):
    def __init__(self, q):
        Thread.__init__(self)
        self.q = q

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            ip = self.q.get()
            url = phone_url.format(ip)
            execute_items(url, key_array)
            sleep(2)
            execute_items(url, unlock)
            sleep(0.2)
            execute_items(url, erase)
            print(ip)
            self.q.task_done()


def execute_items(url, keys):
    for key in keys:
        payload = execute_data.format(key)
        xml_push(url, payload)
        sleep(0.3)
    return


def xml_push(url, payload):
    # Dictionary containing headers for the request
    headers = {
        'SoapAction': 'CUCM:DB ver=9.1',
        'Authorization': 'Basic ',
        'Content-Type': 'text/xml; charset=utf-8'
    }
    try:
        r = requests.post(url, headers=headers, data=payload)
        print(r.text)
    except requests.exceptions.HTTPError as eHttp:
        print("Http Error:", eHttp)
    except requests.exceptions.ConnectionError as eConnection:
        print("Error Connecting:", eConnection)
    except requests.exceptions.Timeout as eTimeout:
        print("Timeout Error:", eTimeout)
    except requests.exceptions.RequestException as eRequest:
        print("OOps: Something Else", eRequest)
    return


def get_ips(path):
    with open(path) as file:
        lines = file.readlines()
    return [line.strip() for line in lines]


def main():
    ts = time()
    ips = get_ips(filename)
    # Create a queue to communicate with the worker threads
    q = Queue()
    # Create 8 worker threads
    for x in range(num_worker_threads):
        worker = MigrationWorker(q)
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()
    # Put the tasks into the queue as a tuple
    for ip in ips:
        q.put(ip)
    # Causes the main thread to wait for the queue to finish processing all the tasks
    q.join()
    print('Took {}'.format(time() - ts))


if __name__ == "__main__":
    # execute only if run as a script
    main()

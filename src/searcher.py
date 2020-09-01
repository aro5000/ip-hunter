# This is a class defining a searching object to query various DNS servers

import requests
import json
import socket


class Searcher:
    def __init__(self, target):
        self._target = target
        self._results = []

    @property
    def results(self):
        return self._results

    def googledns(self):
        # Query Google DNS 4 times and append the answers to the results list
        for i in range(4):
            # This is only for debug purposes:
            #print('Google DNS attempt: ' + str(i))
            r = requests.get('https://dns.google.com/resolve?name=' + self._target + '&type=A')

            # Check HTTP status, and append answers to the results attribute of the searcher object
            if r.ok:
                jdat = json.loads(r.text)
                for o in jdat['Answer']:
                    if o['type'] == 1:
                        self._results.append(o['data'])

    def cloudflaredns(self):
        # Query Cloudflare DNS 4 times and append the answers to the results list
        for i in range(4):
            # This is only for debug purposes:
            #print('Cloudflare DNS attempt: ' + str(i))
            headers = {'accept': 'application/dns-json'}
            r = requests.get('https://cloudflare-dns.com/dns-query?name=' + self._target + '&type=A', headers=headers)

            # Check HTTP status, and append answers to the results attribute of the searcher object
            if r.ok:
                jdat = json.loads(r.text)
                for o in jdat['Answer']:
                    if o['type'] == 1:
                        self._results.append(o['data'])

    def localresolver(self):
        # Query the locally assigned resolver 4 times.
        for i in range(4):
            # For debugging purposes:
            #print('Local DNS attempt: ' + str(i))
            resp = socket.gethostbyname(self._target)
            self._results.append(resp)

#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: keystone_test.py
Author: zuozongming(zuozongming@cloudin.ren)
Date: 2016/03/14 10:36:40
'''
import os
import sys
import time
import pycurl
import logging
import json
import requests

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='a')


class KeystoneTest:
    
    def __init__(self):
        self.username = "perf_testuser_0001"
        self.password = "demopass"
        self.user_domain_name = "default"
        self.project_domain_name = "default"
        self.project_name = "demo"
        self.keystone_url = "http://127.0.0.1:35357/v3/"

    def make_auth_data(self):
        data = { "auth": {
                   "identity": {
                     "methods": ["password"],
                     "password": {
                       "user": {
                         "name": self.username,
                         "domain": { "id": self.user_domain_name },
                         "password": self.password
                       }
                     }
                   },
                   "scope": {
                     "project": {
                       "name": self.project_name,
                       "domain": { "id": self.project_domain_name }
                     }
                   }
                 }
               }
        return json.dumps(data)
    
    def create_token(self):
        logging.info('create token is begin')
        auth_url = self.keystone_url + "auth/tokens"
        post_data = self.make_auth_data()
        headers = {'content-type': 'application/json'}
        try:
            r = requests.post(auth_url, post_data, headers=headers)
            logging.info('token is [%s]'%r.headers["X-Subject-Token"])
            logging.info('create token is end')
            return r.headers["X-Subject-Token"]
        except:
            logging.warning('create token is failed')
            return False

    def validate_token(self):
        logging.info('validate token is begin')
        master_token = self.create_token()
        headers = {'content-type': 'application/json',
                   'X-Auth-Token': master_token,
                   'X-Subject-Token': self.create_token()}
        auth_url = self.keystone_url + "auth/tokens"
        try:
            r = requests.get(auth_url, headers=headers)
            logging.info('token is [%s]'%r.headers["X-Subject-Token"])
            logging.info('validate token is end')
            return r.headers["X-Subject-Token"]
        except:
            logging.warning('validate token is failed')
            return False

def main():
    keystone_test = KeystoneTest()
    if keystone_test.create_token() is False:
        print "False"
    elif keystone_test.validate_token() is False:
        print "False"
    else:
        print "Ture"
if __name__ == '__main__':
    main()

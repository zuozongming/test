#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: keystone_test.py
Author: zuozongming(zuozongming@cloudin.ren)
Date: 2016/03/14 10:36:40
'''
import re
import os
import sys
import time
import logging
import json
import requests

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='a')


class CheckUser:
    
    def __init__(self):
        self.ip_use_file = "./user.txt"
        self.user_dict = {}
        self.internal_customer_dict = {}
        self.external_customer_dict = {}
        self.user_ipnum_map = {}
        self.customer_json_file = "./customer.txt"


    def _get_ip_use_num(self):
        user_file = open(self.ip_use_file, "r")
        for line in user_file:
            line = line.strip("\r\n").strip()
            if line not in self.user_dict:
                self.user_dict[line] = 0
            self.user_dict[line] += 1
            num +=1

    def _get_internal_user_name(self):
        customer_file = open(self.customer_json_file, "r")
        for line in customer_file:
            line = line.strip("\r\n").strip()
            customer = json.loads(line)
            data = customer['data']
            for item in data:
                pattern = '>(.+?)</a>'
                user = re.findall(pattern, item['user__username'])
                type = item['account_type']
                if type in "内部用户".decode('utf-8'):
                    self.internal_customer_dict[user[0]] = item['name']
                else:
                    self.external_customer_dict[user[0]] = item['name']

    def check_internal_user_ip_num(self):
        self._get_internal_user_name()
        self._get_ip_use_num()
        num = 0
        for user in self.user_dict:
            if user in self.internal_customer_dict:
                print self.internal_customer_dict[user],
                print self.user_dict[user]
                num += self.user_dict[user]
            elif user in self.external_customer_dict:
                print self.external_customer_dict[user],
                print self.user_dict[user]
                num += self.user_dict[user]
            else:
                print user,
                print self.user_dict[user]
                num += self.user_dict[user]
        print num
        print 'ok'


def main():
    check_user = CheckUser()
    check_user.check_internal_user_ip_num()

if __name__ == '__main__':
    main()

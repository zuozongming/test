#!/usr/bin/env python
# -*- coding: gb18030 -*-
 
'''
File: check_token.py
Author: zuozongming(zuozongming@cloudin.ren)
Date: 2016/03/02 18:14:40
'''
import json
import logging
import urllib2
import urllib
import socket
import time
import sys
import os
import re



def check_token():
    user_file = "data/user_token.json"
    #f = open(user_file, "rb", 0)
    token_file = "data/user_token.txt"
    t = open(token_file, "w")
   #多个token 
   with open(user_file) as f:
        for line in f.readlines():
            p = json.loads(line)
            for data in p:
                if data == "access":
                    access_list = p[data]
                    for access in access_list:
                         if access == "token":
                             token_list = access_list[access]
                             for token in token_list:
                                 if token == "id":
                                     fernet_token =  token_list[token]
                                     t.write(fernet_token+"\n")
                                     #print fernet_token
    f.close()
    t.close()
    
def main():
    check_token()

if __name__ == "__main__":
    main()

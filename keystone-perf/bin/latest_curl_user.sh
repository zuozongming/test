#!/bin/sh
curl -X POST -d '{"auth": {"passwordCredentials":{"username": "perf_testuser_0001", "password": "demopass"}}}' \
     -H "Content-type: application/json" http://0.0.0.0:35357/v2.0/tokens \
     > ../data/user_token_ben.json
python check_token_user_ben.py


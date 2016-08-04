#!/bin/sh
rm data/user_token.json

#创建多个token
while read USER_NAME; do
#for i in $(seq 1); do
#    USER_NAME=perf_testuser_$(printf "%04d" $i)
    curl -X POST -d '{"auth": {"passwordCredentials":{"username": "'${USER_NAME}'", "password": "demopass"}}}' \
         -H "Content-type: application/json" http://0.0.0.0:5000/v2.0/tokens \
         >> data/user_token.json
         echo "">> data/user_token.json

    #     -H "Content-type: application/json" http://0.0.0.0:5000/v2.0/tokens | \
    #     python -mjson.tool
    #     python -mjson.tool >> data/user_token.json
    #     >> data/user_token.json
    if [ "$?" != 0 ]; then
        echo "Token validation failed"
        break
    fi
done <data/username.txt


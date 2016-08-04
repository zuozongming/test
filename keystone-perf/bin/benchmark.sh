set -e
HOST=127.0.0.1

echo "[+] Delete users..."
#/usr/bin/time -f "%e" -a sh perf-delete-users.sh
echo "[+] Delete users done"
sleep 1

echo "[+] Create users..."
#/usr/bin/time -f "%e" -a sh perf-create-users.sh
echo "[+] Create users done"
sleep 1


echo "[+] Create token..."
sh latest_curl_user.sh
ADMIN_TOKEN=`sed -n "${num}p" ../data/user_token_ben.txt`
SUBJECT_TOKEN=`sed -n "${num}p" ../data/user_token_ben.txt`
RELEASE_PATH=../release


echo "Warming up Apache..."
ab -c 100 -n 1000 -T 'application/json' http://$HOST:35357/ > /dev/null 2>&1

echo "Benchmarking token creation..."
ab -r -c 1 -n 200 -p auth.json -T 'application/json' http://$HOST:35357/v3/auth/tokens > $RELEASE_PATH/latest_create_token
if grep -q 'Non-2xx' $RELEASE_PATH/latest_create_token; then
echo 'Non-2xx return codes! Aborting.'
fi


echo "Benchmarking token validation..."
ab -r -c 1 -n 10000 -T 'application/json' -H "X-Auth-Token: $ADMIN_TOKEN" -H "X-Subject-Token: $SUBJECT_TOKEN" http://$HOST:35357/v3/auth/tokens > $RELEASE_PATH/latest_validate_token
if grep -q 'Non-2xx' $RELEASE_PATH/latest_validate_token; then
echo 'Non-2xx return codes! Aborting.'
fi

echo "Benchmarking token creation concurrently..."
ab -r -c 100 -n 2000 -p auth.json -T 'application/json' http://$HOST:35357/v3/auth/tokens > $RELEASE_PATH/latest_create_token_concurrent
if grep -q 'Non-2xx' $RELEASE_PATH/latest_create_token_concurrent; then
  echo 'WARNING: Non-2xx return codes!'
fi

echo "Benchmarking token validation concurrency..."
ab -r -c 100 -n 100000 -T 'application/json' -H "X-Auth-Token: $ADMIN_TOKEN" -H "X-Subject-Token: $SUBJECT_TOKEN" http://$HOST:35357/v3/auth/tokens > $RELEASE_PATH/latest_validate_token_concurrent
if grep -q 'Non-2xx' $RELEASE_PATH/latest_validate_token_concurrent; then
  echo 'WARNING: Non-2xx return codes!'
fi

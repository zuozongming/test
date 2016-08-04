#!/bin/sh

export OS_SERVICE_TOKEN=ADMIN
export OS_SERVICE_ENDPOINT=http://localhost:35357/v3.0
rm ../data/username.txt
for i in $(seq 100); do
    openstack user create  perf_testuser_$(printf "%04d" $i) \
                         --project demo --password demopass 2>&1 > /dev/null
    echo "perf_testuser_$(printf "%04d" $i)">> ../data/username.txt
    if [ "$?" != 0 ]; then
        echo "User creation failed"
        break
    fi
done


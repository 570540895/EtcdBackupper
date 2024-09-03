import os
import json
import time
import csv

with open('test.csv', 'w') as fp:
    writer = csv.writer(fp, dialect='unix')

    writer.writerow(['uid', 'createDate', 'startTime', 'endTime', 'cpu_num', 'mem(GB)', 'gpu_num', 'worker_num'])
    writer.writerows([['1', 2, 3, 4, 4, 4, 4, 4], ['2', 3, 4, 5, 8, 8, 8, 1]])
    fp.close()


print(int(time.time()))
key_set = {'a', 'b', 'c'}
element = 'd'
if element not in key_set:
    key_set.add(element)
print(key_set)

p = os.popen('ETCDCTL_API=3 etcdctl --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key --endpoints=https://10.105.12.159:2379,https://10.105.12.158:2379,https://10.105.12.157:2379  get --prefix /registry/scheduling.volcano.sh/podgroups/default')
s = p.read()
dic = json.load(s)
print(dic)
p.close()

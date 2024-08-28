import os
p = os.popen("ETCDCTL_API=3 etcdctl --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key --endpoints=https://10.105.12.159:2379,https://10.105.12.158:2379,https://10.105.12.157:2379  get --prefix /registry/scheduling.volcano.sh/podgroups/default")
s = p.read()
print(s)
p.close()

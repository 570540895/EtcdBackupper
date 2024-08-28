import os
import base64

# ETCD config
etcd_cacert_path = '/etc/kubernetes/pki/etcd/ca.crt'
etcd_cert_path = '/etc/kubernetes/pki/etcd/server.crt'
etcd_key_path = '/etc/kubernetes/pki/etcd/server.key'
etcd_endpoints = 'https://10.105.12.159:2379,https://10.105.12.158:2379,https://10.105.12.157:2379'
key_prefix = '/registry/scheduling.volcano.sh/podgroups/default'
init_etcd_revision = ''
etcd_revision = ''

init_cmd = 'ETCDCTL_API=3 etcdctl --cacert={} --cert={} --key={} --endpoints={} -w=json get --prefix {}'.format(
    etcd_cacert_path, etcd_cert_path, etcd_key_path, etcd_endpoints, key_prefix
)

cmd = 'ETCDCTL_API=3 etcdctl --cacert={} --cert={} --key={} --endpoints={} -w=json get --prefix {} --rev={}'.format(
    etcd_cacert_path, etcd_cert_path, etcd_key_path, etcd_endpoints, key_prefix, etcd_revision
)

# initialize
p = os.popen(init_cmd)
p.read()

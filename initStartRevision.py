import os
import json


def initialize_etcd_start_revision():
    with open("./config.json", "r") as f:
        cfg_dict = json.load(f)
        etcd_cacert_path = cfg_dict['etcd_cacert_path']
        etcd_cert_path = cfg_dict['etcd_cert_path']
        etcd_key_path = cfg_dict['etcd_key_path']
        etcd_endpoints = cfg_dict['etcd_endpoints']
        key_prefix = cfg_dict['key_prefix']
        start_revision_file = cfg_dict['start_revision_file']
        f.close()

    init_cmd = 'ETCDCTL_API=3 etcdctl --cacert={} --cert={} --key={} --endpoints={} -w=json get --prefix {}'.format(
        etcd_cacert_path, etcd_cert_path, etcd_key_path, etcd_endpoints, key_prefix
    )

    # initialize
    p = os.popen(init_cmd)
    s = p.read()
    d = json.loads(s)
    with open(start_revision_file, 'w') as f:
        f.write(str(d['header']['revision']))
        f.close()


if __name__ == '__main__':
    initialize_etcd_start_revision()

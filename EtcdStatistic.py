import os
import time
import json
import base64
import csv

csv_file = 'output/data-{}.csv'.format(str(int(time.time())))

def get_etcd_data():
    # get etcdctl config
    with open('./config.json', 'r') as f:
        cfg_dict = json.load(f)
        etcd_cacert_path = cfg_dict['etcd_cacert_path']
        etcd_cert_path = cfg_dict['etcd_cert_path']
        etcd_key_path = cfg_dict['etcd_key_path']
        etcd_endpoints = cfg_dict['etcd_endpoints']
        key_prefix = cfg_dict['key_prefix']
        start_revision_file = cfg_dict['start_revision_file']
        f.close()

    # initialize etcd_start_revision and etcd_end_revision
    with open(start_revision_file, 'r') as f:
        etcd_start_revision = int(f.read())
        f.close()
    init_cmd = 'ETCDCTL_API=3 etcdctl --cacert={} --cert={} --key={} --endpoints={} -w=json get --prefix {}'.format(
        etcd_cacert_path, etcd_cert_path, etcd_key_path, etcd_endpoints, key_prefix
    )
    res = os.popen(init_cmd)
    res_s = res.read()
    res_d = json.loads(res_s)
    etcd_end_revision = res_d['header']['revision']

    with open(csv_file, 'w') as fp:
        writer = csv.writer(fp, dialect='unix')
        writer.writerow(['uid', 'createDate', 'startTime', 'endTime', 'cpu_num', 'mem(GB)', 'gpu_num', 'worker_num'])
        key_set = set({})
        for etcd_revision in range(etcd_start_revision, etcd_end_revision+1):
            cmd = 'ETCDCTL_API=3 etcdctl --cacert={} --cert={} --key={} --endpoints={} -w=json get --prefix {} --rev={}'.format(
                etcd_cacert_path, etcd_cert_path, etcd_key_path, etcd_endpoints, key_prefix, etcd_revision
            )
            res = os.popen(cmd)
            res_s = res.read()
            res_d = json.loads(res_s)

            kvs =
            for kv in kvs:
                key =
                if key in key_set:
                    continue
                key_set.add(key)
                value =
                uid =
                createDate =
                startTime =
                endTime =
                cpu_num =
                mem =
                gpu_num =
                worker_num =
                writer.writerow([uid, createDate, startTime, endTime, cpu_num, mem, gpu_num, worker_num])
        fp.close()


if __name__ == '__main__':
    get_etcd_data()

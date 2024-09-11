import os
import time
import datetime
import json
import base64
import csv

csv_file = 'output/data-{}.csv'.format(str(int(time.time())))

start_time_offset = 0
end_time_offset = 0


def utctime2timestamp(utc_time_str):
    UTC_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
    ts = datetime.datetime.strptime(utc_time_str, UTC_FORMAT) + datetime.timedelta(hours=8)
    return int(ts.timestamp())


def get_num(str):
    i = 0
    for c in str:
        if '0' <= c <= '9':
            i = i*10+(ord(c)-ord('0'))
        else:
            break
    return i


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

    '''    
    init_cmd = 'ETCDCTL_API=3 etcdctl --cacert={} --cert={} --key={} --endpoints={} -w=json get --prefix {}'.format(
        etcd_cacert_path, etcd_cert_path, etcd_key_path, etcd_endpoints, key_prefix
    )
    res = os.popen(init_cmd)
    res_s = res.read()
    res_d = json.loads(res_s)
    etcd_end_revision = res_d['header']['revision']
    '''

    # 临时使用
    etcd_end_revision = etcd_start_revision + 300000

    with open(csv_file, 'w') as fp:
        writer = csv.writer(fp, dialect='unix')
        writer.writerow(['uid', 'createDate', 'startTime', 'endTime', 'cpu_num', 'mem(GB)', 'gpu_num', 'worker_num'])
        key_set = set({})
        etcd_revision = etcd_start_revision
        while etcd_revision <= etcd_end_revision:
            cmd = 'ETCDCTL_API=3 etcdctl --cacert={} --cert={} --key={} --endpoints={} -w=json get --prefix {} --rev={}'.format(
                etcd_cacert_path, etcd_cert_path, etcd_key_path, etcd_endpoints, key_prefix, etcd_revision
            )
            res = os.popen(cmd)
            res_s = res.read()

            # 临时使用
            if len(res_s) < 10:
                continue
            etcd_revision = etcd_revision + 1

            res_d = json.loads(res_s)

            if 'kvs' not in res_d.keys():
                continue
            kvs = res_d['kvs']
            for kv in kvs:
                key = base64.b64decode(kv['key'])
                if key in key_set:
                    continue
                key_set.add(key)
                value = base64.b64decode(kv['value'])
                value_d = json.loads(value)
                uid = value_d['metadata']['ownerReferences'][0]['uid']
                create_date = utctime2timestamp(value_d['metadata']['creationTimestamp'])
                if 'status' not in value_d.keys():
                    continue
                if 'conditions' not in value_d['status'].keys():
                    continue
                conditions = value_d['status']['conditions']
                for condition in conditions:
                    if condition['type'] == 'Scheduled':
                        start_time = utctime2timestamp(condition['lastTransitionTime'])
                        break
                cfg = value_d['metadata']['annotations']['kubectl.kubernetes.io/last-applied-configuration']
                cfg_d = json.loads(cfg)
                duration = cfg_d['spec']['tasks'][0]['template']['spec']['activeDeadlineSeconds']
                end_time = start_time + duration
                cpu_num = get_num(value_d['spec']['minResources']['requests.cpu'])
                mem = get_num(value_d['spec']['minResources']['requests.memory'])
                gpu_num = int(int(value_d['spec']['minResources']['zhejianglab.com/gpu'])/int(value_d['spec']['minResources']['pods']))
                worker_num = int(value_d['spec']['minMember'])
                writer.writerow([uid, create_date, start_time, end_time, cpu_num, mem, gpu_num, worker_num])
        fp.close()


if __name__ == '__main__':
    get_etcd_data()

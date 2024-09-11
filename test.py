import os
import json
import time
import csv
import pandas as pd
import datetime
import base64

d = {"1": "2"}
print(d.keys())

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


def test():
    with open('demo.csv', 'w') as fp:
        writer = csv.writer(fp, dialect='unix')
        res_s = '{"header":{"cluster_id":8827614406474033067,"member_id":17200601880754911600,"revision":3734578,"raft_term":44},"kvs":[{"key":"L3JlZ2lzdHJ5L3NjaGVkdWxpbmcudm9sY2Fuby5zaC9wb2Rncm91cHMvZGVmYXVsdC92Y2pvYi0wLTgzYmY5NmYwLWEwNzItNDE1ZC1hNTAyLWE2MDI3MzRiOTE3ZQ==","create_revision":3734399,"mod_revision":3734481,"version":3,"value":"eyJhcGlWZXJzaW9uIjoic2NoZWR1bGluZy52b2xjYW5vLnNoL3YxYmV0YTEiLCJraW5kIjoiUG9kR3JvdXAiLCJtZXRhZGF0YSI6eyJhbm5vdGF0aW9ucyI6eyJrdWJlY3RsLmt1YmVybmV0ZXMuaW8vbGFzdC1hcHBsaWVkLWNvbmZpZ3VyYXRpb24iOiJ7XCJhcGlWZXJzaW9uXCI6XCJiYXRjaC52b2xjYW5vLnNoL3YxYWxwaGExXCIsXCJraW5kXCI6XCJKb2JcIixcIm1ldGFkYXRhXCI6e1wiYW5ub3RhdGlvbnNcIjp7fSxcIm5hbWVcIjpcInZjam9iLTBcIixcIm5hbWVzcGFjZVwiOlwiZGVmYXVsdFwifSxcInNwZWNcIjp7XCJtaW5BdmFpbGFibGVcIjo0LFwic2NoZWR1bGVyTmFtZVwiOlwidm9sY2Fub1wiLFwidGFza3NcIjpbe1wibmFtZVwiOlwidGFzay0wXCIsXCJwb2xpY2llc1wiOlt7XCJhY3Rpb25cIjpcIkNvbXBsZXRlSm9iXCIsXCJldmVudFwiOlwiVGFza0NvbXBsZXRlZFwifV0sXCJyZXBsaWNhc1wiOjQsXCJ0ZW1wbGF0ZVwiOntcIm1ldGFkYXRhXCI6e1wibmFtZVwiOlwicG9kLTBcIn0sXCJzcGVjXCI6e1wiYWN0aXZlRGVhZGxpbmVTZWNvbmRzXCI6MzYxLFwiY29udGFpbmVyc1wiOlt7XCJjb21tYW5kXCI6W1wiL2Jpbi9zaFwiLFwiLWNcIixcInNsZWVwIDEwMDAwMFwiXSxcImltYWdlXCI6XCJidXN5Ym94XCIsXCJuYW1lXCI6XCJjdHItMFwiLFwicmVzb3VyY2VzXCI6e1wibGltaXRzXCI6e1wiY3B1XCI6XCI2NG1cIixcIm1lbW9yeVwiOlwiODk2TWlcIixcInpoZWppYW5nbGFiLmNvbS9ncHVcIjo4fSxcInJlcXVlc3RzXCI6e1wiY3B1XCI6XCI2NG1cIixcIm1lbW9yeVwiOlwiODk2TWlcIixcInpoZWppYW5nbGFiLmNvbS9ncHVcIjo4fX19XSxcInJlc3RhcnRQb2xpY3lcIjpcIk5ldmVyXCJ9fX1dLFwidHRsU2Vjb25kc0FmdGVyRmluaXNoZWRcIjowfX1cbiJ9LCJjcmVhdGlvblRpbWVzdGFtcCI6IjIwMjQtMDktMTFUMDk6Mjg6MzVaIiwiZ2VuZXJhdGlvbiI6MywibWFuYWdlZEZpZWxkcyI6W3siYXBpVmVyc2lvbiI6InNjaGVkdWxpbmcudm9sY2Fuby5zaC92MWJldGExIiwiZmllbGRzVHlwZSI6IkZpZWxkc1YxIiwiZmllbGRzVjEiOnsiZjptZXRhZGF0YSI6eyJmOmFubm90YXRpb25zIjp7Ii4iOnt9LCJmOmt1YmVjdGwua3ViZXJuZXRlcy5pby9sYXN0LWFwcGxpZWQtY29uZmlndXJhdGlvbiI6e319LCJmOm93bmVyUmVmZXJlbmNlcyI6eyIuIjp7fSwiazp7XCJ1aWRcIjpcIjgzYmY5NmYwLWEwNzItNDE1ZC1hNTAyLWE2MDI3MzRiOTE3ZVwifSI6e319fSwiZjpzcGVjIjp7Ii4iOnt9LCJmOm1pbk1lbWJlciI6e30sImY6bWluUmVzb3VyY2VzIjp7Ii4iOnt9LCJmOmNvdW50L3BvZHMiOnt9LCJmOmNwdSI6e30sImY6bGltaXRzLmNwdSI6e30sImY6bGltaXRzLm1lbW9yeSI6e30sImY6bWVtb3J5Ijp7fSwiZjpwb2RzIjp7fSwiZjpyZXF1ZXN0cy5jcHUiOnt9LCJmOnJlcXVlc3RzLm1lbW9yeSI6e30sImY6cmVxdWVzdHMuemhlamlhbmdsYWIuY29tL2dwdSI6e30sImY6emhlamlhbmdsYWIuY29tL2dwdSI6e319LCJmOm1pblRhc2tNZW1iZXIiOnsiLiI6e30sImY6dGFzay0wIjp7fX0sImY6cXVldWUiOnt9fSwiZjpzdGF0dXMiOnt9fSwibWFuYWdlciI6InZjLWNvbnRyb2xsZXItbWFuYWdlciIsIm9wZXJhdGlvbiI6IlVwZGF0ZSIsInRpbWUiOiIyMDI0LTA5LTExVDA5OjI4OjM1WiJ9LHsiYXBpVmVyc2lvbiI6InNjaGVkdWxpbmcudm9sY2Fuby5zaC92MWJldGExIiwiZmllbGRzVHlwZSI6IkZpZWxkc1YxIiwiZmllbGRzVjEiOnsiZjpzdGF0dXMiOnsiZjpjb25kaXRpb25zIjp7fSwiZjpwaGFzZSI6e319fSwibWFuYWdlciI6InZjLXNjaGVkdWxlciIsIm9wZXJhdGlvbiI6IlVwZGF0ZSIsInRpbWUiOiIyMDI0LTA5LTExVDA5OjI4OjM3WiJ9XSwibmFtZSI6InZjam9iLTAtODNiZjk2ZjAtYTA3Mi00MTVkLWE1MDItYTYwMjczNGI5MTdlIiwibmFtZXNwYWNlIjoiZGVmYXVsdCIsIm93bmVyUmVmZXJlbmNlcyI6W3siYXBpVmVyc2lvbiI6ImJhdGNoLnZvbGNhbm8uc2gvdjFhbHBoYTEiLCJibG9ja093bmVyRGVsZXRpb24iOnRydWUsImNvbnRyb2xsZXIiOnRydWUsImtpbmQiOiJKb2IiLCJuYW1lIjoidmNqb2ItMCIsInVpZCI6IjgzYmY5NmYwLWEwNzItNDE1ZC1hNTAyLWE2MDI3MzRiOTE3ZSJ9XSwidWlkIjoiNThmNTgwYjMtMjY3Zi00ZDNiLWE4ZTEtYmJmOWZiMjEwYmMyIn0sInNwZWMiOnsibWluTWVtYmVyIjo0LCJtaW5SZXNvdXJjZXMiOnsiY291bnQvcG9kcyI6IjQiLCJjcHUiOiIyNTZtIiwibGltaXRzLmNwdSI6IjI1Nm0iLCJsaW1pdHMubWVtb3J5IjoiMzU4NE1pIiwibWVtb3J5IjoiMzU4NE1pIiwicG9kcyI6IjQiLCJyZXF1ZXN0cy5jcHUiOiIyNTZtIiwicmVxdWVzdHMubWVtb3J5IjoiMzU4NE1pIiwicmVxdWVzdHMuemhlamlhbmdsYWIuY29tL2dwdSI6IjMyIiwiemhlamlhbmdsYWIuY29tL2dwdSI6IjMyIn0sIm1pblRhc2tNZW1iZXIiOnsidGFzay0wIjo0fSwicXVldWUiOiJkZWZhdWx0In0sInN0YXR1cyI6eyJjb25kaXRpb25zIjpbeyJsYXN0VHJhbnNpdGlvblRpbWUiOiIyMDI0LTA5LTExVDA5OjI4OjM2WiIsIm1lc3NhZ2UiOiI0LzAgdGFza3MgaW4gZ2FuZyB1bnNjaGVkdWxhYmxlOiBwb2QgZ3JvdXAgaXMgbm90IHJlYWR5LCA0IG1pbkF2YWlsYWJsZSIsInJlYXNvbiI6Ik5vdEVub3VnaFJlc291cmNlcyIsInN0YXR1cyI6IlRydWUiLCJ0cmFuc2l0aW9uSUQiOiIwYjg3MWJhNi0yNDdjLTQyZmEtOWZhNy0yNjgwZWZiMzk2YTkiLCJ0eXBlIjoiVW5zY2hlZHVsYWJsZSJ9LHsibGFzdFRyYW5zaXRpb25UaW1lIjoiMjAyNC0wOS0xMVQwOToyODozN1oiLCJyZWFzb24iOiJ0YXNrcyBpbiBnYW5nIGFyZSByZWFkeSB0byBiZSBzY2hlZHVsZWQiLCJzdGF0dXMiOiJUcnVlIiwidHJhbnNpdGlvbklEIjoiNmU3MTMxMzYtZDhhOC00NzFjLTkzOGQtZTM2MTllMzlkNjZjIiwidHlwZSI6IlNjaGVkdWxlZCJ9XSwicGhhc2UiOiJSdW5uaW5nIn19Cg=="}],"count":1}'
        res_d = json.loads(res_s)
        kvs = res_d['kvs']
        key_set = set({})
        for kv in kvs:
            key = base64.b64decode(kv['key'])
            if key in key_set:
                continue
            key_set.add(key)
            value = base64.b64decode(kv['value'])
            value_d = json.loads(value)
            uid = value_d['metadata']['ownerReferences'][0]['uid']
            create_date = utctime2timestamp(value_d['metadata']['creationTimestamp'])
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


if __name__ =='__main__':
    test()
print(1)







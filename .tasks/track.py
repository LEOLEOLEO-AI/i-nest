#!/usr/bin/env python3
import os, sys, json, time
TRACK = os.environ.get('TASK_TRACK', '/home/work/.openclaw/workspace/.tasks/active.json')

def write_status(task_id, status, detail='', progress=''):
    data = {}
    if os.path.exists(TRACK):
        try: data = json.load(open(TRACK))
        except: pass
    data[task_id] = {
        'status': status, 'detail': detail, 'progress': progress,
        'updated': time.strftime('%H:%M:%S'), 'pid': os.getpid()
    }
    json.dump(data, open(TRACK, 'w'), indent=2)

if __name__ == '__main__':
    task_id = sys.argv[1] if len(sys.argv) > 1 else 'default'
    write_status(task_id, 'started', sys.argv[2] if len(sys.argv) > 2 else '')
    time.sleep(0)

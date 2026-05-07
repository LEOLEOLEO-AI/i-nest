import os, json, subprocess, time

track = '/home/work/.openclaw/workspace/.tasks/active.json'
log = '/home/work/.openclaw/workspace/.tasks/status_log.txt'
sim = '/home/work/.openclaw/workspace/sdi_sim'
now = time.strftime('%Y-%m-%d %H:%M:%S')

print('===== CLAW TASK STATUS %s =====' % now)
print('')

if os.path.exists(track):
    try:
        d = json.load(open(track))
        s_key = 'status'; a_key = 'updated'; det_key = 'detail'
        for tid, info in d.items():
            pid = info.get('pid', '?')
            alive = os.path.exists('/proc/%s' % pid) if pid != '?' else False
            dot = '[ON]' if alive else '[OFF]'
            print('  %s %s: %s @ %s | %s' % (dot, tid, info.get(s_key,'?'), info.get(a_key,'?'), info.get(det_key,'')))
    except Exception as e:
        print('  (read failed: %s)' % e)
else:
    print('  no active tasks')

print('')
print('[processes]')
r = subprocess.run(['ps', 'aux'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
lines = r.stdout.decode().split('\n')
procs = [l for l in lines if 'python' in l.lower() and 'grep' not in l and 'http.server' not in l and 'websockify' not in l and 'networkd' not in l and 'waagent' not in l and 'unattended' not in l and 'WALinuxAgent' not in l]
if procs:
    for p in procs[:5]:
        print(' ' + p[:120])
else:
    print('  none running')

print('')
print('[result files]')
files = []
if os.path.exists(sim):
    files = sorted([f for f in os.listdir(sim) if f.endswith('.json')], key=lambda x: os.path.getmtime(os.path.join(sim, x)), reverse=True)
    for f in files[:5]:
        fp = os.path.join(sim, f)
        size = os.path.getsize(fp)
        mtime = time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(fp)))
        print('  %s: %sB @ %s' % (f, size, mtime))

print('')
print('[sessions]')
r2 = subprocess.run(['openclaw', 'sessions', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
for line in r2.stdout.decode().split('\n'):
    if 'running' in line.lower():
        print(' ' + line[:100])

with open(log, 'w') as f:
    f.write(now + '\n')
    f.write('python_procs: %d\n' % len(procs))
    for ff in files:
        f.write(ff + '\n')
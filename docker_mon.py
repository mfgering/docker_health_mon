#!/usr/bin/python

# All SSH libraries for Python are junk (2011-10-13).
# Too low-level (libssh2), too buggy (paramiko), too complicated
# (both), too poor in features (no use of the agent, for instance)

# Here is the right solution today:

import re
import subprocess
import sys

HOST="alphocker.dawson"
CONTAINER="mfgtransovpnproxy"
# Ports are handled in ~/.ssh/config since we use OpenSSH
#COMMAND = f"docker container inspect {CONTAINER}"
#docker ps --filter "name=mfgtransovpnproxy" --format "{{.ID}}: {{.Status}}"
COMMAND = 'docker ps --all --filter "name=mfgtransovpnproxy" --format "{{.Names}}\t{{.ID}}\t{{.Status}}"'

ssh = subprocess.Popen(["ssh", HOST, COMMAND],
                       shell=False, 
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
result = ssh.stdout.readlines()
if result == []:
    error = ssh.stderr.readlines()
    print(f"ERROR: {error}")
else:
    health_pattern = r"[^\(]+\((.*?)\)"
    for line in result:
        (names, id, status) = line.decode("utf-8").split("\t")
        m = re.search(health_pattern, status)
        if m:
            health = m.group(1)
        else:
            pass # no health!
        print(line.decode("utf-8"))
    output = [x.decode("utf-8") for x in result]
    print(output)
    

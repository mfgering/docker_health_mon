#!/usr/bin/python3
import re
import subprocess
import sys
import smtplib
import settings

def send_notice(name, state):
        conn = smtplib.SMTP(settings.SMTP_SERVER)
        conn.set_debuglevel(False)
        conn.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        try:
                body = f"The docker container named '{name}' is in state '{state}' and not healthy."
                message = f"Subject: {name} container is not healthy\n\n{body}"
                conn.sendmail(settings.EMAIL_FROM, settings.RECIPIENTS, message)
        except Exception as exc:
                print(exc)
        finally:
                conn.quit()

def restart_container(container):
    COMMAND = f'docker container restart {container}'
    ssh = subprocess.Popen(["ssh", settings.HOST, COMMAND],
                            shell=False, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()

state = None
health = None
TEMPLATE = '{{.Names}}\t{{.ID}}\t{{.Status}}'
COMMAND = f'docker ps --all --filter "name={settings.CONTAINER}" --format "{TEMPLATE}"'

ssh = subprocess.Popen(["ssh", settings.HOST, COMMAND],
                                           shell=False, 
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
result = ssh.stdout.readlines()
if result == []:
        #error = ssh.stderr.readlines()
        send_notice(settings.CONTAINER, 'not found')
        #print(f"ERROR: {error}")
else:
        health_pattern = r"[^\(]+\((.*?)\)"
        state_pattern = r"^(.*?)\s+"
        for line in result:
                (names, id, status) = line.decode("utf-8").split("\t")
                if names == settings.CONTAINER:
                        m = re.search(state_pattern, status)
                        if m:
                                state = m.group(1).lower()
                                if state == 'up':
                                        m = re.search(health_pattern, status)
                                        if m:
                                                health = m.group(1).lower()
                                        else:
                                                pass # no health!
                        break
                print(line.decode("utf-8"))
        if health != 'healthy':
                send_notice(settings.CONTAINER, state)
                restart_container(settings.CONTAINER)

        #output = [x.decode("utf-8") for x in result]
        #print(output)
        

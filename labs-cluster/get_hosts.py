#!/usr/bin/env python3
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json
import socket
import subprocess
import paramiko
import sys
import os


SSH_USERNAME = "iiitd"
SSH_PASSWORD = "student"

key = open(os.path.expanduser('~/.ssh/id_rsa.pub')).read()

def main():
    ips = find_ips()
    with open("hosts_lame", "w") as f:
        f.write("[servers]\n")
        
        for i,ip in enumerate(ips):
            f.write("server%i ansible_host=%s\n" % (i,ip))
        
        f.write("\n[servers:vars]\n")
        
        f.write("ansible_user=iiitd\nansible_pass=student\nansible_sudo_pass=student\nansible_python_interpreter=/usr/bin/python3")

    


def find_ips():
    ips = []
    for last in range(11,250):
        ip = "192.168.32."+str(last)
        print(ip, end=" : ")
        if port_22_is_open(ip):
            ips.append(ip)
    return ips

def port_22_is_open(ip):
    # SSH DETAILS
    SSH_ADDRESS = ip

    client = paramiko.SSHClient()
    client.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(SSH_ADDRESS, username=SSH_USERNAME, password=SSH_PASSWORD, timeout=1)
        client.exec_command('mkdir -p ~/.ssh/')
        client.exec_command('echo "%s" > ~/.ssh/authorized_keys' % key)
        client.exec_command('chmod 644 ~/.ssh/authorized_keys')
        client.exec_command('chmod 700 ~/.ssh/')
        client.close()
        print("success")
        return True
    except Exception as e:
        print("error: {0}".format(e))
        return False


if __name__ == '__main__':
    main()

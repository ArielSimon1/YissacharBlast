#!/bin/env python3
# -*- coding: latin-1 -*-
from io import StringIO
import paramiko 
from time import sleep
import glob, os
from scp import SCPClient

def file_command(filepath):
    os.chdir(filepath)
    print("Welcome to Yissachar-lab Blast-script.")
    sleep(2)
    print("your input files:")
    for file in glob.glob("*.seq"):
        print(file)
    sleep(1)

class SshClient:
    #"A wrapper of paramiko.SSHClient"
    TIMEOUT = 4

    def __init__(self, host, port, username, password, key=None, passphrase=None):
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if key is not None:
            key = paramiko.RSAKey.from_private_key(StringIO(key), password=passphrase)
        self.client.connect(host, port, username=username, password=password, pkey=key, timeout=self.TIMEOUT)
        os.chdir('D:/Blastn_input')
        for file in glob.glob("*.seq"):
            with SCPClient(self.client.get_transport()) as scp:
                scp.put(file, 'Yissachar-Blast/input_files/'+file)  # Copy my_file.txt to the server


    def close(self):
        if self.client is not None:
            self.client.close()
            self.client = None

    def execute(self, command, sudo=False):
        feed_password = False
        if sudo and self.username != "root":
            file_command("D:/Blastn_input")
            command = 'bash BlastScript.sh'
            print("Working on it...")
            sleep(2)
            print("Level 1/3: create multiple sequences input file...")
            sleep(2)
            print("Level 2/3: blasting :) ... approximately 2 minutes per sequence")
            feed_password = self.password is not None and len(self.password) > 0
        stdin, stdout, stderr = self.client.exec_command(command)
        if feed_password:
            stdin.write(self.password + "\n")
            stdin.flush()
        return {'out': stdout.readlines(), 
                'err': stderr.readlines(),
                'retval': stdout.channel.recv_exit_status()}

    def execute2(self, command, sudo=False):
        feed_password = False
        if sudo and self.username != "root":
            command = 'rm /home/stu/nissan/Yissachar-Blast/input_files/*'
        stdin, stdout, stderr = self.client.exec_command(command)
        if feed_password:
            stdin.write(self.password + "\n")
            stdin.flush()
        return {'out': stdout.readlines(), 'err': stderr.readlines(), 'retval': stdout.channel.recv_exit_status()}

if __name__ == "__main__":
    client = SshClient(host='132.70.61.34', port=22, username='nissan', password='nissan2018')
    try:
        ret = client.execute('dmesg', sudo=True)
        print("".join(ret["out"]))
        ret2 = client.execute2('dmesg', sudo=True)
        print('Done. have a good day!')
        sleep(200)
    finally:
      client.close()
#!/usr/bin/env python
#coding:utf8
#++++++++++++description++++++++++++#
"""
@author:ying
@contact:249462971@qq.com
@site:
@software: PyCharm
@time: 2019/5/14 上午7:52
"""
#+++++++++++++++++++++++++++++++++++#

import paramiko
class SshCmd(object):
    def __init__(self,ip,username,passwd,port,cmd):
        self.ip=ip
        self.username=username
        self.passwd=passwd
        self.port=port
        self.cmd=cmd

    def sshCmd(self):
        # print self.host
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.host,port=self.port,username=self.username,password=self.passwd)
        stdin, stdout, stderr = ssh.exec_command(self.cmd)
        stdout=stdout.readlines()
        ssh.close()
        # print '------>',stdout
        return stdout
    def sshCmds(self):
        # print self.host
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.host,port=self.port,username=self.username,password=self.passwd)
        stdin, stdout, stderr = ssh.exec_command(self.cmd)
        stdout=stdout.read()
        ssh.close()
        # print '------>',stdout
        return stdout

# ip='192.168.101.70'
# username='root'
# passwd='jgmes2018'
# port=22
# cmd='ls'
# # ssh = paramiko.SSHClient()
# # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# # ssh.connect(hostname=host,port=port,username=username,password=passwd)
# # stdin, stdout, stderr = ssh.exec_command(cmd)
# # print ('stdout---->', stdout.readlines())
# # ssh.close()
# ssh1 = SshCmd(host=ip, username=username, passwd=passwd, port=port, cmd=cmd)
# # str=str(ssh1.sshCmd()).replace('\\n','').replace('\\l','').replace('\S','').replace('\\','').strip().replace('Kernel r on an m','')
# str = ssh1.sshCmd()
# print str
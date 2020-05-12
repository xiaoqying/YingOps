#!/usr/bin/env python
#coding:utf8
#++++++++++++description++++++++++++#
"""
@author:ying
@contact:249462971@qq.com
@site: 
@software: PyCharm
@time: 2019/5/14 上午7:52
@该文件没什么用，仅供参考
"""
#+++++++++++++++++++++++++++++++++++#

import yaml,nmap,os,time,json,paramiko,hmac
os.environ['DJANGO_SETTINGS_MODULE'] = 'YingOps.settings'
import django
django.setup()
from assets import models
from pysnmp.entity.rfc3413.oneliner import cmdgen
PROJECT_ROOT = os.path.realpath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import sys
# print PROJECT_ROOT
"""加载配置文件"""
s_conf=yaml.load(open('{0}/conf/scanhosts.yaml'.format(PROJECT_ROOT) ))

'''服务器参数'''
net = s_conf['hostinfo']['nets'][0]
nets = s_conf['hostinfo']['nets'][0]+'.0/24'
ssh_pass = s_conf['hostinfo']['ssh_pass']
ssh_user = s_conf['hostinfo']['ssh_user']
syscmd_list = s_conf['hostinfo']['syscmd_list']
ports = s_conf['hostinfo']['ports']
black_list = s_conf['hostinfo']['black_list']
email_list = s_conf['hostinfo']['email_list']
ssh_key_file = s_conf['hostinfo']['ssh_key_file']

'''交换机参数'''
cpu_oids =s_conf['netinfo']['cpu_oids']
mem_oids =s_conf['netinfo']['mem_oids']
temp_oids =s_conf['netinfo']['temp_oids']
modle_oids =s_conf['netinfo']['modle_oids']
sysname_oid =s_conf['netinfo']['sysname_oid']
community = s_conf['netinfo']['community']


# s_conf['hostinfo']['nets'][0] = net = 'nihao'

# print net,s_conf['hostinfo']['nets'][0]



"""开始扫描"""
class ScanHostMethod(object):
    """初始化数据"""
    def __init__(self,nets):
        self.nets=nets

    """扫描出所有的ip"""
    def allHost(self):
        nm=nmap.PortScanner()
        nm.scan(self.nets,arguments='-n sP PE')
        all_host=nm.all_hosts()
        with open('all_host.txt','w') as f:
            f.write(json.dumps(all_host))
        # print('-'*20,all_host)
        return all_host

    """对扫描出来的所有IP进行分类"""
    def hostItems(self):
        unknow_list=[]
        linux_dic={}
        windows_dic={}
        nm = nmap.PortScanner()
        nm.scan(self.nets, arguments='-n sP PE')
        all_host = nm.all_hosts()
        for host in all_host:
            try:
                if nm[host]['tcp'][22]['state'] == 'open':
                    ports=nm[host]['tcp'].keys()
                    print('{0} is linux system...There are some ports opening --> {1}'.format(host,ports))
                    linux_dic[host]=ports
                else:
                    try:
                        if nm[host]['tcp'][3389]['state'] == 'open':
                            ports = nm[host]['tcp'].keys()
                            print('%s is windows system..... There are some ports opening --> %s' %(host,ports))
                            windows_dic[host] = ports
                        else:
                            unknow_list.append(host)
                    except KeyError:
                        unknow_list.append(host)
                        continue
            except KeyError:
                try:
                    if nm[host]['tcp'][3389]['state'] == 'open':
                        ports = nm[host]['tcp'].keys()
                        print('%s is windows system.....!!!!!!! There are some ports opening --> %s' %(host,ports))
                        windows_dic[host]=ports
                    else:
                        unknow_list.append(host)
                except KeyError:
                    unknow_list.append(host)
                    # print('--------> %s KeyError' %host)


        with open('conf/txtfile/all_host.txt','w') as f:
            f.write(json.dumps(all_host))
        with open('conf/txtfile/linux_host.txt','w') as f:
            f.write(json.dumps(linux_dic))
        with open('conf/txtfile/windows_host.txt','w') as f:
            f.write(json.dumps(windows_dic))
        with open('conf/txtfile/unknow_host.txt','w') as f:
            f.write(json.dumps(unknow_list))

        return all_host,linux_dic,windows_dic,unknow_list


class SwitchMethod(object):
    '''初始化参数'''
    def __init__(self,unknow_li,cpu_oids,mem_oids,temp_oids,modle_oids,sysname_oid,community):
        self.sw_li=unknow_li
        self.cpu_oids=cpu_oids
        self.mem_oids=mem_oids
        self.temp_oids=temp_oids
        self.modle_oids=modle_oids
        self.sysname_oid=sysname_oid
        self.community=community
    '''交换机总执行方法'''
    def swMethod(self,sw_ip,oids):
        try:
            cg = cmdgen.CommandGenerator()
            errorIndication,errorStatus,errorIndex,varBinds = cg.getCmd(
                cmdgen.CommunityData('server',self.community,1),
                cmdgen.UdpTransportTarget((sw_ip,161)),
                oids
            )
            result = str(varBinds[0][1]) if varBinds[0][1] else ""
        except Exception as e:
            result = None
            print(sw_ip + ' is not switch or snmp not enable!')
        except IndexError:
            result = None
            print(sw_ip + ' is not switch or snmp not enable!')
        return result
    '''获取cpu使用率'''
    def cpuInfo(self,swip):
        for oid in self.cpu_oids:
            cpu_usage=self.swMethod(swip,oid)
            if cpu_usage:
                print('--------cpu_usage',cpu_usage)
                return cpu_usage
            else:
                print('------++++++++++++--',cpu_usage)
    '''获取mem使用率'''
    def memInfo(self,swip):
        for oid in self.mem_oids:
            mem_usage=self.swMethod(swip,oid)
            if mem_usage:
                return mem_usage
    '''获取交换机名称'''
    def sysnameInfo(self,swip):
        for oid in self.sysname_oid:
            sysname = self.swMethod(swip,oid)
            if sysname:
                return sysname
    '''获取交换机型号'''
    def modleInfo(self,swip):
        for oid in self.modle_oids:
            modle_usage=self.swMethod(swip,oid)
            if modle_usage:
                return modle_usage
    '''获取温度'''
    def tempInfo(self,swip):
        for oid in self.temp_oids:
            temp_usage=self.swMethod(swip,oid)
            if temp_usage:
                return temp_usage
    '''run'''
    def run(self):
        dic={}
        obj = models.SwitchInfo.objects.all()
        for swip in self.sw_li:
            ip=swip
            sysname = self.sysnameInfo(swip)
            if sysname:
                cpu = self.cpuInfo(swip)

                mem = self.memInfo(swip)
                temp = self.tempInfo(swip)
                sysname = self.sysnameInfo(swip)
                modle = self.modleInfo(swip)

                dic['cpu']=cpu
                dic['ip']=ip
                dic['mem']=mem
                dic['temp']=temp
                dic['sysname']=sysname
                dic['modle']=modle
                if cpu or mem or temp or  sysname or modle:
                    print('{0} switch ---> cpu:{1},mem:{2},temp:{3},sysname:{4},modle:{5}'.format(swip,cpu,mem,temp,sysname,modle))
                # print temp,mem,sysname
                    obj.create(**dic)

class LinuxMethod(object):
    def __init__(self, linux_dic, ssh_user, ssh_pass):
        self.linux_dic=linux_dic
        self.ssh_user=ssh_user
        self.ssh_pass=ssh_pass

    def enhmac(self,str):
        newstr = hmac.new('yingzi')
        newstr.update(str)
        return newstr
    def try_ssh_login(self):
        obj2 = models.LinuxInfo.objects.all()
        # # 创建SSH对象
        ssh = paramiko.SSHClient()
        # # 允许连接不在know_hosts文件中的主机
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        infos = {}
        for host in self.linux_dic.keys():
            for user in self.ssh_user:
                for pas in self.ssh_pass:
                    # # 连接服务器
                    info = []
                    try:
                        ssh.connect(hostname=host, port=22, username=user, password=pas)
                        info.append(user)
                        info.append(pas)
                        # # 执行命令
                        for cmd in syscmd_list:
                            # print cmd
                            stdin, stdout, stderr = ssh.exec_command(cmd)
                            # # 获取命令结果
                            result = stdout.read()
                            # print(result)
                            res=str((result).replace('\\n','').replace('\\l','').replace('\S','').replace('\\','').strip().replace('Kernel r on an m',''))
                            info.append(res)
                        infos[host] = info
                        break
                    except paramiko.ssh_exception.AuthenticationException:
                        # pass
                        print(host,user,pas,'用户名密码错误....')
                    except paramiko.ssh_exception.SSHException:
                        print(host, user, pas, '用户名密码错误....')
                    except EOFError:
                        print('EOFError')

                    # # # 关闭连接
        print('-------------------->>>>>>', infos)
        ssh.close()
        dicc={}
        for host_ip, j in infos.items():
            # print("ip地址:", i, '操作系统:', j[0], j[1], '主机名:', j[2], 'MAC地址:', j[3], 'SN序列号:', j[4], '制造商:', j[5], '型号：',
            #       j[6], '根磁盘使用率：', j[7], '内存使用率：', j[8], 'G', '负载：', j[9])
            print ("ip地址:",host_ip,'操作系统:',j[2],j[3],'主机名:',j[4],'MAC地址:',j[5],'SN序列号:',j[6].replace(' ',''),'制造商:',j[7].replace(' ',''),'型号：',j[8].replace(' ',''),'根磁盘使用率：',j[9],'内存使用率：',j[10],'G','负载：',j[11])
            # print(i,j)
            obj2.create(
                ip=host_ip,
                hostname=j[4],
                system_ver=j[2]+j[3],
                ssh_port=22,
                ssh_user=j[0],
                ssh_passwd=j[1],
                mac_address=j[5],
                sn=j[6],
                manufacturer=j[7],
                cpu_cores=j[11],
                mem_total=j[10],
                disk_total=j[9]
            )

class WindowsMethod(object):
    def __init__(self,windows_dic):
        self.windows_dic=windows_dic
    def windowsInfo(self):
        dic={}
        obj3=models.WindowsInfo.objects.all()
        for ip,port in self.windows_dic.items():
            print(ip,port)
            # dic[ip]=str(port)

            obj3.create(
                ip=ip,
                port=str(port),
            )

# coding:utf8
import yaml, nmap, os, time, json, paramiko, hmac

# os.environ['DJANGO_SETTINGS_MODULE'] = 'YingOps.settings'
# import django
# django.setup()
# from assets import models
import pymysql

"""开始扫描"""


class ScanHostMethod(object):
    """初始化数据"""

    def __init__(self, nets):
        self.nets = nets

    """收集扫描出来22端口"""

    def hostItems(self):
        linux_list = []
        nm = nmap.PortScanner()
        nm.scan(self.nets, arguments='-n sP PE')
        all_host = nm.all_hosts()
        for host in all_host:
            try:
                if nm[host]['tcp'][22]['state'] == 'open':
                    linux_list.append(host)
                else:
                    pass
            except KeyError:
                pass
        print(linux_list)
        return linux_list


class GetLinuxMethod(object):
    def __init__(self):
        self.syscmd_list = [
            # ip
            "ip a|egrep 192.168.|head -1|awk -F ' ' '{print $2}'|awk -F '/' '{print $1}'",
            # 主机名
            "hostname",
            # cpu核数
            "cat /proc/cpuinfo|grep 'processor'|wc -l",
            # 内存大小
            "free | grep 'Mem:' | awk '{print substr(($2)/1000/1000,1,4)}'",
            # 根磁盘大小
            "df -h |grep -w '/' |awk '{print $2}'",
            # CPU当前负载
            "uptime|awk -F ':' '{print $NF}'|awk -F ',' '{print $1}'|sed 's/ //g'",
            # 内存使用率
            "free | grep 'Mem:' | awk '{print substr(($3)/($2)*100,1,4)}'",
            # 根磁盘使用率
            "df |grep -w '/'|awk '{print substr(($3)/($2)*100,1,4)}'",
            # 当前系统时间
            "date '+%Y-%m-%d %H:%M:%S'",
            # 系统运行时间
            "uptime|awk -F ' ' '{print $2,$3$4}'|sed 's/,//g'",
            # 系统版本
            "cat /etc/redhat-release",
            # mac地址
            "cat /sys/class/net/[^vtlsb]*/address|tail -1",
            # sn序列号
            "dmidecode -s system-serial-number",
            # 厂家
            "dmidecode -s system-manufacturer",
            # 型号
            "dmidecode -s system-product-name",
            "cat /proc/cpuinfo | grep name | cut -f2 -d: | uniq ",
        ]

    """收集扫描出来22端口"""

    def get_linux_list(self,nets):
        linux_list = []
        nm = nmap.PortScanner()
        for net in nets:
            # print(net)
            # 该方式支持多个端口模式，运行速度慢
            # nm.scan(net, arguments='-n -sP -PE')
            # 该方式只支持22号端口，运行速度块
            nm.scan(net, ports='22', arguments='-sV')
            all_host = nm.all_hosts()
            # print(all_host)
            linux_list = all_host
            # print('------>', linux_list)
            # 使用多端口模式时，使用下面的方法
            # for host in all_host:
            #     try:
            #         if nm[host]['tcp'][22]['state'] == 'open':
            #             print('-->',host)
            #             linux_list.append(host)
            #         else:
            #             pass
            #     except KeyError:
            #         pass
        return linux_list



    """尝试登陆，登录成功就记录下来"""
    def try_ssh_login(self,linux_list, user_list, port_list, passwd_list):
        # # 创建SSH对象
        ssh = paramiko.SSHClient()
        # # 允许连接不在know_hosts文件中的主机
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        assets_dict = {}
        print('正在获取服务器{0}信息...'.format(linux_list[0]))
        # # 连接服务器
        for host in linux_list:
            for user in user_list:
                for port in port_list:
                    for passwd in passwd_list:
                        info = []
                        try:
                            ssh.connect(hostname=host, port=port, username=user, password=passwd)
                            info.append(user)
                            info.append(passwd)
                            info.append(port)

                            # # 执行命令
                            for cmd in self.syscmd_list:
                                stdin, stdout, stderr = ssh.exec_command(cmd)
                                # # 获取命令结果
                                result = stdout.read()
                                res = str(result.decode('utf-8')).replace('\n', '')
                                # print(host,':',cmd,'-->>',res)
                                # res=str((result).replace('\\n','').replace('\\l','').replace('\S','').replace('\\','').strip().replace('Kernel r on an m',''))
                                info.append(res)
                            assets_dict[host] = info
                            break
                        except Exception as e:
                            # pass
                            print(host,'_error:',e)
        # # # 关闭连接
        ssh.close()
        return assets_dict
# glm=GetLinuxMethod()
# glm.get_linux_list(['192.168.185.181-247'])

# nm=nmap.PortScanner()
# res=nm.scan('192.168.185.0/24',ports='22',arguments='sV')
# print(nm.all_hosts())

#！/bin/bash
# 该脚本用于客户端服务器
# 创建一个定时任务，定时更新资产数据
ip=`/usr/sbin/ip a|egrep 192.168.|head -1|awk -F ' ' '{print $2}'|awk -F '/' '{print $1}'`
hostname=`hostname`
cpu_cores=`cat /proc/cpuinfo|grep 'processor'|wc -l`
mem_total=`free | grep 'Mem:' | awk '{print substr(($2)/1000/1000,1,4)}'`
disk_total=`df -h |grep -w '/' |awk '{print $2}'`
cpu_status=`uptime|awk -F ':' '{print $NF}'|awk -F ',' '{print $1}'|sed 's/ //g'`
mem_status=`free | grep 'Mem:' | awk '{print substr(($3)/($2)*100,1,4)}'`
disk_status=`df |grep -w '/'|awk '{print substr(($3)/($2)*100,1,4)}'`
system_time=`date '+%Y-%m-%d %H:%M:%S'`
up_time=`uptime|awk -F ' ' '{print $2,$3$4}'|sed 's/,//g'`
system_ver=`cat /etc/redhat-release`
mac_address=`cat /sys/class/net/[^vtlsb]*/address|tail -1`
sn=`/usr/sbin/dmidecode -s system-serial-number`
manufacturer=`/usr/sbin/dmidecode -s system-manufacturer`
product=`/usr/sbin/dmidecode -s system-product-name`
cpu_info=`cat /proc/cpuinfo | grep name | uniq|awk -F ':' '{print $2}'`

# 这里的IP为该项目发布的服务器+端口
curl http://192.168.5.155:8001/assets/live_status/ -X POST \
-d ip="$ip" \
-d hostname="$hostname" \
-d cpu_cores="$cpu_cores" \
-d mem_total="$mem_total" \
-d disk_total"=$disk_total" \
-d cpu_status="$cpu_status" \
-d mem_status="$mem_status" \
-d disk_status="$disk_status" \
-d system_time="$system_time" \
-d up_time="$up_time" \
-d system_ver="$system_ver" \
-d mac_address="$mac_address" \
-d sn="$sn" \
-d manufacturer="$manufacturer" \
-d product="$product" \
-d cpu_info="$cpu_info"
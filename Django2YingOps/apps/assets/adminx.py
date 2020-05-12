from django.contrib import admin
from .models import *

import xadmin
# Register your models here.
# -*- coding: utf-8 -*-
__author__ = 'ying'
__date__ = '2020/03/25 23:52'
import xadmin

from .models import *



class AssetsInfoAdmin(object):
    # list_display = ['ip', 'hostname', 'is_online', 'ssh_port', 'ssh_user', 'ssh_passwd', 'cpu_cores',
    #                 'mem_total', 'disk_total', 'cpu_status', 'mem_status', 'disk_status',
    #                 'desc', 'computer_room', 'system_time', 'up_time', 'system_ver', 'mac_address',
    #                 'sn', 'manufacturer', 'cpu_info']
    list_display = ['ip', 'hostname', 'is_online', 'ssh_port', 'ssh_user', 'ssh_passwd', 'is_delete', 'is_online']
    search_fields =['ip']
    list_filter = ['ip', 'hostname', 'is_online', 'ssh_port', 'ssh_user', 'ssh_passwd', 'cpu_cores',
                    'mem_total', 'disk_total', 'cpu_status', 'mem_status', 'disk_status',
                    'desc', 'computer_room', 'system_time', 'up_time', 'system_ver', 'mac_address',
                    'sn', 'manufacturer', 'cpu_info']
    # style_fields = ["ssh_passwd":]
    # relfield_style = 'fk-ajax'
    # style_fields = {"desc":"ueditor"}
    # inlines = [CategoryInline]
    # model_icon = 'fa fa-university'

class ComputerRoomAdmin(object):
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['name']
"""
ip = models.CharField(max_length=32,null=True, blank=True, verbose_name=u"主机IP信息", default="")
hostname = models.CharField(max_length=32, null=True, blank=True, verbose_name=u"操作系统主机名", default="")
is_online = models.BooleanField(default=True)
ssh_port = models.CharField(max_length=32, null=True, blank=True, verbose_name=u"ssh登录的端口", default="")
ssh_user = models.CharField(max_length=32, null=True, blank=True, verbose_name=u"ssh登录的用户", default="")
ssh_passwd = models.CharField(max_length=64, null=True, blank=True, verbose_name=u"ssh登录的密码", default="")
cpu_cores = models.CharField(max_length=32, null=True, blank=True, verbose_name=u"cpu核数", default="")
mem_total = models.CharField(max_length=32, null=True, blank=True, verbose_name=u"内存总大小", default="")
disk_total = models.CharField(max_length=32, null=True, blank=True, verbose_name=u"磁盘总大小", default="")
cpu_status = models.CharField(max_length=32, null=True, blank=True, verbose_name=u"cpu使用率", default="")
mem_status = models.CharField(max_length=32, null=True, blank=True, verbose_name=u"内存使用率", default="")
disk_status = models.CharField(max_length=32, null=True, blank=True, verbose_name=u"磁盘使用率", default="")
desc = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'描述信息', default="")
computer_room = models.ForeignKey(ComputerRoom, on_delete=models.CASCADE, verbose_name=u"所在机房", default=1)

system_time = models.CharField(max_length=32, null=True, blank=True, verbose_name=u"系统当前时间", default="")
up_time = models.CharField(max_length=32, null=True, blank=True, verbose_name=u"系统运行时间", default="")
system_ver = models.CharField(max_length=256, null=True, blank=True, verbose_name=u"操作系统版本", default="")
mac_address = models.CharField(max_length=64, null=True, blank=True, verbose_name=u"mac地址", default="")
sn = models.CharField(max_length=64, null=True, blank=True, verbose_name=u"SN－主机的唯一标示", default="")
manufacturer = models.CharField(max_length=256, null=True, blank=True, verbose_name=u"制造商", default="")
cpu_info = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"cpu型号", default="")
"""

xadmin.site.register(ComputerRoom, ComputerRoomAdmin)
xadmin.site.register(AssetsInfo, AssetsInfoAdmin)


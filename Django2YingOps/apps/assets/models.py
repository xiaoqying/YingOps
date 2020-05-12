# coding:utf8
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext


# Create your models here.
class ComputerRoom(models.Model):
    name = models.CharField(max_length=64, null=True, blank=True, verbose_name=u'机房名称', default='')

    class Meta:
        verbose_name = u'机房表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class AssetsInfo(models.Model):
    ip = models.CharField(max_length=32,null=True, blank=True, verbose_name=u"主机IP信息", default="")
    hostname = models.CharField(max_length=32, null=True, blank=True, verbose_name=u"操作系统主机名", default="")
    cpu_cores = models.CharField(max_length=32, null=True, blank=True, verbose_name=u"cpu核数", default="")
    mem_total = models.CharField(max_length=32, null=True, blank=True, verbose_name=u"内存总大小", default="")
    disk_total = models.CharField(max_length=32, null=True, blank=True, verbose_name=u"磁盘总大小", default="")
    cpu_status = models.CharField(max_length=32, null=True, blank=True, verbose_name=u"cpu使用率", default="")
    mem_status = models.CharField(max_length=32, null=True, blank=True, verbose_name=u"内存使用率", default="")
    disk_status = models.CharField(max_length=32, null=True, blank=True, verbose_name=u"磁盘使用率", default="")
    system_time = models.CharField(max_length=32, null=True, blank=True, verbose_name=u"系统当前时间", default="")
    up_time = models.CharField(max_length=32, null=True, blank=True, verbose_name=u"系统运行时间", default="")
    system_ver = models.CharField(max_length=256, null=True, blank=True, verbose_name=u"操作系统版本", default="系统版本")
    mac_address = models.CharField(max_length=64, null=True, blank=True, verbose_name=u"mac地址", default="")
    sn = models.CharField(max_length=64, null=True, blank=True, verbose_name=u"SN－主机的唯一标示", default="Unknow")
    manufacturer = models.CharField(max_length=256, null=True, blank=True, verbose_name=u"制造商", default="Unknow")
    product = models.CharField(max_length=256, null=True, blank=True, verbose_name=u"型号", default="Unknow")
    cpu_info = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"cpu型号", default="")
    is_online = models.BooleanField(verbose_name=u'状态',default=True)
    is_delete = models.BooleanField(verbose_name=u'是否删除',default=False)
    desc = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'描述信息', default="Unknow")
    computer_room = models.ForeignKey(ComputerRoom, on_delete=models.CASCADE, verbose_name=u"所在机房", default=1)
    ssh_port = models.CharField(max_length=32, null=True, blank=True, verbose_name=u"ssh登录的端口", default="")
    ssh_user = models.CharField(max_length=32, null=True, blank=True, verbose_name=u"ssh登录的用户", default="")
    ssh_passwd = models.CharField(max_length=64, null=True, blank=True, verbose_name=u"ssh登录的密码", default="")

    class Meta:
        verbose_name = u'资产信息表'
        verbose_name_plural = verbose_name

        def __str__(self):
            return self.ip

class IbmStatus(models.Model):
    ip = models.CharField(max_length=64, null=True, verbose_name=u"IMM接口IP", default="")
    Processors = models.CharField(max_length=64, null=True, verbose_name=u"处理器", default="")
    Disks = models.CharField(max_length=64, null=True, verbose_name=u"磁盘", default="")
    System = models.CharField(max_length=64, null=True, verbose_name=u"操作系统", default="")
    Memory = models.CharField(max_length=64, null=True, verbose_name=u"内存", default="")
    Power_Modules = models.CharField(max_length=64, null=True, verbose_name=u"电源模块", default="")
    Cooling_Devices = models.CharField(max_length=64, null=True, verbose_name=u"风扇", default="")
    Adapters = models.CharField(max_length=64, null=True, verbose_name=u"适配器", default="")
    date_time = models.CharField(max_length=64, null=True, verbose_name=u"更新时间", default="")

    class Meta:
        verbose_name = u'IBM服务器状态表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ip

# Generated by Django 2.1.8 on 2020-04-21 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0008_auto_20200421_1004'),
    ]

    operations = [
        migrations.CreateModel(
            name='IbmStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(default='', max_length=64, null=True, verbose_name='IMM接口IP')),
                ('Processors', models.CharField(default='', max_length=64, null=True, verbose_name='处理器')),
                ('Disks', models.CharField(default='', max_length=64, null=True, verbose_name='磁盘')),
                ('System', models.CharField(default='', max_length=64, null=True, verbose_name='操作系统')),
                ('Memory', models.CharField(default='', max_length=64, null=True, verbose_name='内存')),
                ('Power_Modules', models.CharField(default='', max_length=64, null=True, verbose_name='电源模块')),
                ('Cooling_Devices', models.CharField(default='', max_length=64, null=True, verbose_name='风扇')),
                ('Adapters', models.CharField(default='', max_length=64, null=True, verbose_name='适配器')),
                ('date_time', models.CharField(default='', max_length=64, null=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': 'IBM服务器状态表',
                'verbose_name_plural': 'IBM服务器状态表',
            },
        ),
    ]

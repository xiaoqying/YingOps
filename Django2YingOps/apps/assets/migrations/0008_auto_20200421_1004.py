# Generated by Django 2.1.8 on 2020-04-21 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0007_auto_20200421_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetsinfo',
            name='ssh_passwd',
            field=models.CharField(blank=True, default='', max_length=64, null=True, verbose_name='ssh登录的密码'),
        ),
    ]

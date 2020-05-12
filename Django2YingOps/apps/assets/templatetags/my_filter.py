#!/usr/bin/env python
#coding:utf8
#++++++++++++description++++++++++++#
"""
@author:ying
@contact:249462971@qq.com
@site: 
@software: PyCharm
@file: my_filter.py
@time: 2019/7/17 下午3:56
"""
#+++++++++++++++++++++++++++++++++++#
from django import template
register=template.Library()


@register.filter
def split_str(value):
    res=value.split('_')
    return res


@register.filter
def replace_str(value):
    if value=='Normal':
        res='正常'
    else:
        res='不正常'
    return res
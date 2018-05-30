# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 00:35:15 2018

@author: Juchen
"""
import boto3
user_data = 0

def class_gpa(classname, userdata):
    return userdata[classname]
def calculategpa(userdata):
    value = 0
    tick = 0
    for i in userdata.values():
        value = value + float(i)
        tick += 1
    return value/tick
    

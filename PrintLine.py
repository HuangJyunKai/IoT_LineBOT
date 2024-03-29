#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 22:08:53 2019

@author: huangjunkai
"""
import time, random, requests
import DAN

ServerURL = 'https://6.iottalk.tw' #with SSL connection
Reg_addr = 'qwwfoijefoiqhfeoiqvho' #if None, Reg_addr = MAC address

DAN.profile['dm_name']='L0858605'
DAN.profile['df_list']=['Line_Out','Dummy_Sensor']
DAN.device_registration_with_retry(ServerURL, Reg_addr)
while True:
    try:
        ANS=DAN.pull('Line_Out')
        print(ANS)
    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    
    time.sleep(5)

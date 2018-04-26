# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 21:53:53 2018

@author: gxsage
"""

import tushare as ts
import pandas as pd
import time
import os
import datetime
import matplotlib.pyplot as plt

import MyDefs


def Get_tradedays(days):
    dates = []
    dtStr = datetime.date.today().strftime("%Y-%m-%d")
    dt=datetime.date.today()
    dates.append(dtStr)
    cnt=1
    while cnt<days:
        dt = dt - datetime.timedelta(1)
        dtStr=dt.strftime("%Y-%m-%d")
        if not ts.is_holiday(dtStr):
            dates.append(dtStr)
            cnt+=1
    dates.reverse()
    return dates

def Get_Kdatadays(code,days):
    dates = Get_tradedays(days)
    dt =ts.get_k_data(code,start=dates[0], end=dates[1])
    dt = dt.reset_index(drop=True)
    
    print(dt)
    date = dt.loc[dt.shape[0]-1,'date']
    if not date==datetime.date.today().strftime("%Y-%m-%d"):
        df =ts.get_today_all()
        df=df[df.code==code][['open','high','low','volume','code']]
        df.volume=df.volume/100
        df.insert(0,'date',datetime.date.today().strftime("%Y-%m-%d"))
        df.insert(2,'close',1000)
        print(df)
        ret = pd.concat([dt,df])
    else:
        ret = dt
    ret = ret.reset_index(drop=True)
    return ret
    
def Is_VolumeChange(df,low,high):
    dflen = df.shape[0]
    if(df.loc[dflen-1,'volume']>df.loc[dflen-2,'volume']*low) & (df.loc[dflen-1,'volume']<df.loc[dflen-2,'volume']*high):
        return 1
    else:
        return 0

def dateRange(beginDate, endDate):
    dates = []
    dt = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y-%m-%d")
    return dates

#4-5% 量相等
if __name__ == '__main__':

    dates = Get_tradedays(3)
    for dtStr in dates[0:len(dates)-1]:
        print(dtStr)
        df = ts.get_tick_data('600579',date=dtStr)
    
    #df = ts.get_today_ticks('601333')
    print(df)


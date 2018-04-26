# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 08:57:15 2018

@author: gxsag
"""

import tushare as ts
import pandas as pd
import os
import datetime


def get_today_all_ts(date):

    date_now = date

# 先获得所有股票的收盘数据
    df_close = ts.get_today_all()
    #df_close.to_csv(str(date_now) + '_today.csv', index=False, encoding='gbk')
    
       # 获得所有股票的基本信息
    df_basics = ts.get_stock_basics()
    df_basics.to_csv(str(date_now) + '_todaybasics.csv', index=False, encoding='gbk')
    df_all = pd.merge(left=df_close, right=df_basics, on='name', how='left')
    
    df_all['code'] = df_all['code'].astype(str) + ' '
    
    # 保存数据
    #df_all.to_csv(str(date_now) + '_ts.csv', index=False, encoding='gbk')
    
    #print(df_all)
    return df_all

def Output_Csv(df,Filename):
    #reload(sys)
    #sys.setdefaultencoding( "gbk" )
    df.to_csv(Filename,index=False,encoding='gbk')#选择保存 
    
def Input_Csv(Filename):
    #reload(sys)
    #sys.setdefaultencoding( "gbk" )
    df = pd.read_csv(Filename, encoding='gbk')
    return df
    
def Get_MyGroup_Count(df,colsName):
    out = pd.DataFrame({colsName : df[colsName].drop_duplicates(),
                       'count':0.})
    for str in out[colsName]:
        out.loc[out[colsName] == str,'count']= df[df[colsName] == str].shape[0]
    out = out.sort_values('count',ascending=0)
    return out



def Get_today_analysis(df):
    
    df.fillna(0, inplace=True)
    df.replace('nan ', 0, inplace=True)
    df['timeToMarket'] = pd.to_datetime(df['timeToMarket'])
    
    df[['changepercent', 'pe', 'mktcap', 'nmc']] = df[['changepercent', 'pe', 'mktcap', 'nmc']].astype(float)
    df['timeToMarket'] = pd.to_datetime(df['timeToMarket'])
    
    df['code'] = df['code'].astype(str)  # 转化成str后，NAN也变成nan str格式
    # 添加 交易所 列
    df.loc[df['code'].str.startswith('3'), 'exchange'] = 'CY'
    df.loc[df['code'].str.startswith('6'), 'exchange'] = 'SH'
    df.loc[df['code'].str.startswith('0'), 'exchange'] = 'SZ'
    
    ret = In_Get_df_info(df,'ALL')
    indudf = Get_MyGroup_Count(df,'industry')
    print(indudf)
    
    for str1 in indudf['industry']:
        re = In_Get_df_info(df[df.industry==str1],str1)
        ret = pd.concat([ret,re])

    ret['apm'] = ret['UP']*100/(ret['UP']+ret['DOWN'])
    ret = ret.sort_values('apm',ascending=0)
    ret = ret.reset_index(drop=True)
    return ret


def In_Get_df_info(df,classify):
    # 找出上涨的股票
    df_up = df[df['changepercent'] > 0.00]
    # 走平股数
    df_even = df[df['changepercent'] == 0.00]
    # 找出下跌的股票
    df_down = df[df['changepercent'] < 0.00]
    
    # 找出涨停的股票
    limit_up = df[df['changepercent'] >= 9.70]
    limit_down = df[df['changepercent'] <= -9.70]
    
    limit_up_6 = df[df['changepercent'] >= 6]
    limit_down_6 = df[df['changepercent'] <= -6]
    
    out = pd.DataFrame({'classify':[classify],
                        'UP':[df_up.shape[0]],
                        'DOWN':[df_down.shape[0]],
                        'EVEN':[df_even.shape[0]],
                        '10UP':[limit_up.shape[0]],
                        '10DN':[limit_down.shape[0]],
                        '6UP':[limit_up_6.shape[0]],
                        '6DN':[limit_down_6.shape[0]]})
    out = out[['classify','UP','EVEN','DOWN','10DN','10UP','6DN','6UP']]
   
    return out


def Get_SomeStockIndustry(df):
    out = Get_MyGroup_Count(df,'industry')
    
    ret = pd.DataFrame()
    for str1 in out['industry'].head(5):
        re=df[(df['industry']==str1) & (df['changepercent'] >= 6)].sort_values('changepercent',ascending=0).head(5)
        ret= ret.append(re)
    out = ret[['code','name','industry','changepercent']]

    return out


def Is_VolumeChange(df,low,high):
    print(df)
    dflen = df.shape[0]
    print(df.volume[dflen-1])
    if(df.loc[dflen-1,'volume']>df.loc[dflen-2,'volume']*low) & (df.loc[dflen-1,'volume']<df.loc[dflen-2,'volume']*high):
        return True
    else:
        return False

def Get_SomeStockVolume(df,low,high):
    for code in df.code:
        print(code)
        out = Get_Kdatadays(code,5)
        if Is_VolumeChange(out,low,high):
            print(code+" OKKKKKKKKK")
    return 0

def Get_StockCP(df,low,high):
    df.fillna(0, inplace=True)
    df.replace('nan ', 0, inplace=True)
    df['timeToMarket'] = pd.to_datetime(df['timeToMarket'])
    
    df[['changepercent', 'pe', 'mktcap', 'nmc']] = df[['changepercent', 'pe', 'mktcap', 'nmc']].astype(float)
    df['timeToMarket'] = pd.to_datetime(df['timeToMarket'])
    
    df['code'] = df['code'].astype(str)  # 转化成str后，NAN也变成nan str格式
    # 添加 交易所 列
    df.loc[df['code'].str.startswith('3'), 'exchange'] = 'CY'
    df.loc[df['code'].str.startswith('6'), 'exchange'] = 'SH'
    df.loc[df['code'].str.startswith('0'), 'exchange'] = 'SZ'
    
    ret = df[(df['changepercent'] >= low) & (df['changepercent'] <= high)]
    return ret
    

def Get_tradeday():
    date_now = datetime.date.today().strftime("%Y-%m-%d")
    while ts.is_holiday(date_now): 
        print(date_now)        # 循环条件为1必定成立
        date_now = getYesterday(date_now).strftime("%Y-%m-%d")
    return date_now


def Get_tradedays(days):
    dates = []
    dtStr = datetime.date.today().strftime("%Y-%m-%d")
    dt=datetime.date.today()
    cnt=0
    dates.append(dtStr)
    while cnt<days:
        dt = dt - datetime.timedelta(1)
        dtStr=dt.strftime("%Y-%m-%d")
        if not ts.is_holiday(dtStr):
            cnt+=1
    dates.append(dtStr)
    dates.reverse()
    print(dates)
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


def getYesterday(daystr):  #
  #today=datetime.date.today() 
  today=datetime.datetime.strptime(daystr,'%Y-%m-%d')
  oneday=datetime.timedelta(days=1) 
  yesterday=today-oneday  
  return yesterday


def a():
    date_now = Get_tradeday()
    date = datetime.date.today().strftime("%Y-%m-%d")
    df = get_today_all_ts(date)
    df = Get_StockCP(df,2,5)
    #df = Get_Kdatadays('000037',3)
    print(df)
    
    
    out = Get_StockCP(df,6,10)
    out = Get_SomeStockIndustry(out)
    print(out)
    
    df = Get_StockCP(df,2,3)
    df=Get_SomeStockVolume(df,2,3)
    Output_Csv(df,"D:\\123\\"+date_now+'_an.csv')
    print(df)
    #print(out)
    Output_Csv(out,"D:\\123\\"+date_now+'_analysis.csv')
    return 0
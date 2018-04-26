# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 22:07:35 2018

@author: gxsage
"""




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
    return dates

def Get_Kdatadays(days):
    dates = Get_tradedays(5)
    dt =ts.get_k_data('603083',start=dates[0], end=dates[1])




entstr=temp.Get_tradeday()
print(entstr)
startstr=temp.getYesterday(entstr).strftime("%Y-%m-%d")
startstr=temp.getYesterday(startstr).strftime("%Y-%m-%d")
startstr=temp.getYesterday(startstr).strftime("%Y-%m-%d")
startstr=temp.getYesterday(startstr).strftime("%Y-%m-%d")
print(startstr)

dt =ts.get_k_data('603083',start=startstr, end=entstr)
df =ts.get_today_all()
df=df[df.code=='603083'][['open','high','low','volume','code']]
df.insert(0,'date',entstr)
df.insert(2,'close',1000)
dt = dt.concat(df)
print(dt)

dflen = df.shape[0]
df = df.reset_index(drop=True)
print(dflen)

print(df)
a= df.loc[dflen-1,'volume']
b= df.loc[dflen-2,'volume'].astype(float)
print(a)
if(a>b*1.8):
    print("OK")
else:
    print('NO')
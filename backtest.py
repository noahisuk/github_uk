import pyupbit
import numpy as np

#open,high,low,close,volume으로 당일시가,고가,저가,종가,거래량

df = pyupbit.get_ohlcv("KRW-BTC", count=7) 
df['range'] = (df['high'] - df['low']) * 0.5  #range 변동폭
df['target'] = df['open'] + df['range'].shift(1) #target 매수가

fee = 0.005 #수수료
#ror 수익률
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'] - fee,
                     1)
df['hpr'] = df['ror'].cumprod() #hpr 누적수익률
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100 #dd낙폭
print("MDD(%): ", df['dd'].max()) #Mdd max of dd
df.to_excel("dd.xlsx")
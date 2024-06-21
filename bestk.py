import pyupbit  
import numpy as np  

# k값에 따른 수익률(ROR, Rate of Return)을 계산
def get_ror(k=0.5):
    # 업비트 API를 사용하여 최근 7일간의 비트코인 시세 데이터를 가져옴
    df = pyupbit.get_ohlcv("KRW-BTC", count=7)
    
    # range (고가 - 저가) * k로 당일 변동 범위를 계산
    df['range'] = (df['high'] - df['low']) * k
    
    # target 다음 날의 목표가, 전일 종가 + 변동 범위
    df['target'] = df['open'] + df['range'].shift(1)

    fee = 0.005  

    # ror 목표가 달성 시 수익률 계산, 달성하지 못하면 1
    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'] - fee,  # 목표가 달성 시 (종가 / 목표가 - 수수료)
                         1)  # 목표가 미달성 시 수익률 1

    # 누적 수익률 계산
    ror = df['ror'].cumprod()[-2]
    return ror

# k 값을 0.1부터 0.9까지 0.1 단위로 변경하며 수익률 계산 및 출력
for k in np.arange(0.1, 1.0, 0.1):
    ror = get_ror(k)
    print("%.1f %f" % (k, ror))

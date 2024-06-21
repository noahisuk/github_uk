import time  
import pyupbit  
import datetime  

# API 키 설정
access = "VxmYulqOA62j2Dly5txxptpJuRxaIR5stpzfAxbU"
secret = "mBPS12mNADybgLJELDqiAdtPudBs4Vq0JVLHZ0KD"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)  # 최근 2일간의 시세 데이터를 가져옴
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k  # 목표가 계산
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)  # 최근 1일간의 시세 데이터를 가져옴
    start_time = df.index[0]  # 시작 시간
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()  # 계좌 잔고를 조회
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])  # 잔고 반환
            else:
                return 0  # 잔고가 없을 경우 0 반환
    return 0  # 해당 통화가 없을 경우 0 반환

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]  # 현재가 조회

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()  # 현재 시간
        start_time = get_start_time("KRW-BTC")  # 거래 시작 시간
        end_time = start_time + datetime.timedelta(days=1)  # 거래 종료 시간

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-BTC", 0.5)  # 목표가
            current_price = get_current_price("KRW-BTC")  # 현재가
            if target_price < current_price:
                krw = get_balance("KRW")  # 원화 잔고
                if krw > 5000:
                    upbit.buy_market_order("KRW-BTC", krw*0.9995)  # 시장가로 비트코인 매수
        else:
            btc = get_balance("BTC")  # 비트코인 잔고
            if btc > 0.00008:
                upbit.sell_market_order("KRW-BTC", btc*0.9995)  # 시장가로 비트코인 매도
        time.sleep(1)  # 1초 대기
    except Exception as e:
        print(e)  # 예외 발생 시 출력
        time.sleep(1)  # 1초 대기

import time
import pyupbit
import datetime
import numpy as np

access = "IPs6coOa3zg7ZgVdMdXZb4RnDbyrnFxr4vLTGr66"          # 본인 값으로 변경
secret = "wdaYlczI3x12bLeL2xAAcFktwYslCiJYxkBhgN88"          # 본인 값으로 변경
coin = "SAND" # 원화마켓 코인


def get_ror(k=0.5):
    df = pyupbit.get_ohlcv("KRW-"+coin, count=7)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'],
                         1)

    ror = df['ror'].cumprod()[-2]
    return ror

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-"+coin)
        end_time = start_time + datetime.timedelta(days=1)

        bestK = 0.5
        bestRor = 0
        for k in np.arange(0.1, 1.0, 0.1):
            ror = get_ror(k)
            if ror > bestRor:
                bestRor = ror
                bestK = k

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-"+coin, bestK)
            current_price = get_current_price("KRW-"+coin)
            if target_price < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-"+coin, krw*0.9995)
        else:
            coinBal = get_balance(coin)
            if coinBal > 5100/pyupbit.get_current_price("KRW-"+coin):
                upbit.sell_market_order("KRW-"+coin, coinBal*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
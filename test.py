import pyupbit

access = "IPs6coOa3zg7ZgVdMdXZb4RnDbyrnFxr4vLTGr66"          # 본인 값으로 변경
secret = "wdaYlczI3x12bLeL2xAAcFktwYslCiJYxkBhgN88"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

print(upbit.get_balance("KRW"))     # 현금
print(upbit.get_balance("SAND"))    # 코인 갯수
print(upbit.get_avg_buy_price("SAND"))
print(5000/pyupbit.get_current_price("KRW-BTC"))
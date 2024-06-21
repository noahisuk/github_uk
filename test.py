import pyupbit


access = "VxmYulqOA62j2Dly5txxptpJuRxaIR5stpzfAxbU"          # Acess API
secret = "mBPS12mNADybgLJELDqiAdtPudBs4Vq0JVLHZ0KD"          # Secret API
upbit = pyupbit.Upbit(access, secret)

print(upbit.get_balance("KRW-BTC"))     # 보유 비트코인 조회
print(upbit.get_balance("KRW"))         # 보유 현금 조회
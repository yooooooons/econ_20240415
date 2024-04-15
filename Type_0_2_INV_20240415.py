#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import pyupbit
import datetime
import pandas as pd
import numpy as np
import warnings
import traceback
import math

warnings.filterwarnings('ignore')

#from scipy.signal import savgol_filter
#from scipy.signal import savitzky_golay

#import matplotlib.pyplot as plt


# In[2]:


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)


# In[3]:


# 투자 대상 코인 및 설정값

# Type_0

BTC_0_dic = {'type': 'type_0', 'coin_No': 0, 'coin_Name': 'KRW-BTC', 'ma_duration_long': 69, 'ma_duration_mid': 23, 'ma_duration_short': 5, 'ratio_ema_long_rise': 1.0001, 'ratio_ema_mid_rise': 1.0005, 'recent_ratio_ema_long_plus': 0.0002, 'successive_rise': 7, 'ratio_ema_mid_long': 0.98, 'ref_vol_duration': 3, 'diff_m_l_factor': 0, 'coe_vol_comp': 1.0, 'under_long_duration': 17, 'recent_vol_duration': 0, 'sell_method_vol_cri': 0.2, 'sell_ma_duration_1': 68, 'sell_ma_duration_2': 0, 'ratio_peak_diff': 0.88, 'ratio_sell_ema_mid': 0.999, 'ratio_std_1': 0.1, 'ratio_std_2': 0.05, 'ratio_sell_forced': 0.03, 'bought_state': 0, 'bought_price': 0.0, 'bought_time': 0.0}

ETH_1_dic = {'type': 'type_0', 'coin_No': 1, 'coin_Name': 'KRW-ETH', 'ma_duration_long': 69, 'ma_duration_mid': 44, 'ma_duration_short': 19, 'ratio_ema_long_rise': 1.0, 'ratio_ema_mid_rise': 1.0005, 'recent_ratio_ema_long_plus': 0, 'successive_rise': 12, 'ratio_ema_mid_long': 0.98, 'ref_vol_duration': 3, 'diff_m_l_factor': -0.002, 'coe_vol_comp': 1.5, 'under_long_duration': 19, 'recent_vol_duration': 0, 'sell_method_vol_cri': 0.3, 'sell_ma_duration_1': 47, 'ratio_peak_diff': 0.84, 'ratio_sell_ema_mid': 0.998, 'ratio_std_1': 0.03, 'ratio_std_2': 0.03, 'sell_ma_duration_2': 0, 'ratio_sell_forced': 0.065, 'bought_state': 0, 'bought_price': 0.0, 'bought_time': 0.0}

WAVES_7_dic = {'type': 'type_0', 'coin_No': 7, 'coin_Name': 'KRW-WAVES', 'ma_duration_long': 98, 'ma_duration_mid': 26, 'ma_duration_short': 1, 'ratio_ema_long_rise': 1.0, 'ratio_ema_mid_rise': 1.0004, 'recent_ratio_ema_long_plus': 0, 'successive_rise': 9, 'ratio_ema_mid_long': 0.985, 'ref_vol_duration': 3, 'diff_m_l_factor': -0.003, 'coe_vol_comp': 0.5, 'under_long_duration': 14, 'recent_vol_duration': 0, 'sell_method_vol_cri': 0.1, 'sell_ma_duration_1': 129, 'ratio_peak_diff': 0.77, 'ratio_sell_ema_mid': 0.998, 'ratio_std_1': 0.14, 'ratio_std_2': 0.05, 'sell_ma_duration_2': 0, 'ratio_sell_forced': 0.06, 'bought_state': 0, 'bought_price': 0.0, 'bought_time': 0.0}

STEEM_11_dic = {'type': 'type_0', 'coin_No': 11, 'coin_Name': 'KRW-STEEM', 'ma_duration_long': 70, 'ma_duration_mid': 39, 'ma_duration_short': 7, 'ratio_ema_long_rise': 1.0002, 'ratio_ema_mid_rise': 1.0005, 'recent_ratio_ema_long_plus': 0, 'successive_rise': 13, 'ratio_ema_mid_long': 0.99, 'ref_vol_duration': 1, 'diff_m_l_factor': -0.002, 'coe_vol_comp': 0.5, 'under_long_duration': 26, 'recent_vol_duration': 0, 'sell_method_vol_cri': 0.3, 'sell_ma_duration_1': 85, 'ratio_peak_diff': 0.8, 'ratio_sell_ema_mid': 0.998, 'ratio_std_1': 0, 'ratio_std_2': 0, 'sell_ma_duration_2': 0, 'ratio_sell_forced': 0.085, 'bought_state': 0, 'bought_price': 0.0, 'bought_time': 0.0}

#HIVE_67_dic = {'type': 'type_0', 'coin_No': 67, 'coin_Name': 'KRW-HIVE', 'ma_duration_long': 72, 'ma_duration_mid': 33, 'ma_duration_short': 2, 'ratio_ema_long_rise': 1.0, 'ratio_ema_mid_rise': 1.0004, 'recent_ratio_ema_long_plus': 0.0002, 'successive_rise': 9, 'ratio_ema_mid_long': 0.99, 'ref_vol_duration': 1.0, 'diff_m_l_factor': 0, 'coe_vol_comp': 0.5, 'under_long_duration': 17, 'recent_vol_duration': 0.16, 'sell_method_vol_cri': 0.3, 'ratio_peak_diff': 0.008, 'ratio_std_1': 0.1, 'ratio_std_2': 0.05, 'ratio_sell_ema_mid': 0.0, 'ratio_open_check': 1.0055, 'ratio_prior_to_cur_long': 0.995, 'ratio_mean_long': 0.1, 'ratio_sell_forced': 0.06, 'ratio_sell_forced_peak': 0.16, 'bought_state': 0, 'bought_price': 0.0, 'bought_time': 0.0}



# Type_2

ETC_5_dic = {'type': 'type_2', 'coin_No': 'KRW-ETC', 'coin_Name': 'KRW-ETC', 'ma_duration_long': 102, 'ma_duration_mid': 30, 'ma_duration_short': 75, 'ratio_ema_long_rise': 1.0001, 'ratio_ema_mid_rise': 1.0003, 'recent_ratio_ema_long_plus': 0, 'successive_rise': 8, 'ratio_ema_mid_long': 0.99, 'ratio_vol_curr_prior': 1.0, 'diff_m_l_factor': 0.005, 'diff_vol_aver': 0.5, 'under_long_duration': 29, 'recent_vol_duration': 9, 'sell_method_vol_cri': 0.6, 'ratio_peak_diff': 0.014, 'ratio_open_check': 1.0027, 'ratio_reduced': 0.7, 'ratio_prior_to_cur_long': 0.996, 'ratio_mean_long': 0.5, 'ratio_sell_forced': 0.07, 'bought_state': 0, 'bought_price': 0.0}

BTG_20_dic = {'type': 'type_2', 'coin_No': 'KRW-BTG', 'coin_Name': 'KRW-BTG', 'ma_duration_long': 76, 'ma_duration_mid': 33, 'ma_duration_short': 53, 'ratio_ema_long_rise': 1.0001, 'ratio_ema_mid_rise': 1.0004, 'recent_ratio_ema_long_plus': 0.0002, 'successive_rise': 7, 'ratio_ema_mid_long': 0.99, 'ratio_vol_curr_prior': 1.0, 'diff_m_l_factor': 0.0, 'diff_vol_aver': 0.5, 'under_long_duration': 26, 'recent_vol_duration': 9, 'sell_method_vol_cri': 1.0, 'ratio_peak_diff': 0.013, 'ratio_open_check': 1.0016, 'ratio_reduced': 0.7, 'ratio_prior_to_cur_long': 0.996, 'ratio_mean_long': 0.5, 'ratio_sell_forced': 0.06, 'bought_state': 0, 'bought_price': 0.0}

ARK_14_dic = {'type': 'type_2', 'coin_No': 'KRW-ARK', 'coin_Name': 'KRW-ARK', 'ma_duration_long': 88, 'ma_duration_mid': 26, 'ma_duration_short': 39, 'ratio_ema_long_rise': 1.0, 'ratio_ema_mid_rise': 1.0003, 'recent_ratio_ema_long_plus': 0, 'successive_rise': 8, 'ratio_ema_mid_long': 0.98, 'ratio_vol_curr_prior': 1.0, 'diff_m_l_factor': 0.005, 'diff_vol_aver': 1.0, 'under_long_duration': 42, 'recent_vol_duration': 10, 'sell_method_vol_cri': 0.6, 'ratio_peak_diff': 0.018, 'ratio_open_check': 1.0027, 'ratio_reduced': 10.0, 'ratio_prior_to_cur_long': 0.997, 'ratio_mean_long': 0.5, 'ratio_sell_forced': 0.06, 'bought_state': 0, 'bought_price': 0.0}

WAXP_57_dic = {'type': 'type_2', 'coin_No': 'KRW-WAXP', 'coin_Name': 'KRW-WAXP', 'ma_duration_long': 100, 'ma_duration_mid': 23, 'ma_duration_short': 55, 'ratio_ema_long_rise': 1.0, 'ratio_ema_mid_rise': 1.0003, 'recent_ratio_ema_long_plus': 0.0001, 'successive_rise': 8, 'ratio_ema_mid_long': 0.99, 'ratio_vol_curr_prior': 1.0, 'diff_m_l_factor': 0.0, 'diff_vol_aver': 0.5, 'under_long_duration': 37, 'recent_vol_duration': 8, 'sell_method_vol_cri': 0.3, 'ratio_peak_diff': 0.018, 'ratio_open_check': 1.0016, 'ratio_reduced': 8.0, 'ratio_prior_to_cur_long': 0.997, 'ratio_mean_long': 0.5, 'ratio_sell_forced': 0.05, 'bought_state': 0, 'bought_price': 0.0}

QTUM_9_dic = {'type': 'type_2', 'coin_No': 'KRW-QTUM', 'coin_Name': 'KRW-QTUM', 'ma_duration_long': 89, 'ma_duration_mid': 33, 'ma_duration_short': 77, 'ratio_ema_long_rise': 1.0, 'ratio_ema_mid_rise': 1.0004, 'recent_ratio_ema_long_plus': 0.0001, 'successive_rise': 10, 'ratio_ema_mid_long': 0.98, 'ratio_vol_curr_prior': 1.0, 'diff_m_l_factor': 0.005, 'diff_vol_aver': 0.5, 'under_long_duration': 39, 'recent_vol_duration': 9, 'sell_method_vol_cri': 0.4, 'ratio_peak_diff': 0.006, 'ratio_open_check': 1.0028, 'ratio_reduced': 9.0, 'ratio_prior_to_cur_long': 0.994, 'ratio_mean_long': 0.4, 'ratio_sell_forced': 0.08, 'bought_state': 0, 'bought_price': 0.0}

BCH_30_dic = {'type': 'type_2', 'coin_No': 'KRW-BCH', 'coin_Name': 'KRW-BCH', 'ma_duration_long': 99, 'ma_duration_mid': 29, 'ma_duration_short': 71, 'ratio_ema_long_rise': 1.0, 'ratio_ema_mid_rise': 1.0004, 'recent_ratio_ema_long_plus': 0.0001, 'successive_rise': 8, 'ratio_ema_mid_long': 0.98, 'ratio_vol_curr_prior': 1.0, 'diff_m_l_factor': 0.0, 'diff_vol_aver': 1.0, 'under_long_duration': 50, 'recent_vol_duration': 8, 'sell_method_vol_cri': 0.8, 'ratio_peak_diff': 0.008, 'ratio_open_check': 1.0027, 'ratio_reduced': 8.0, 'ratio_prior_to_cur_long': 0.995, 'ratio_mean_long': 0.3, 'ratio_sell_forced': 0.05, 'bought_state': 0, 'bought_price': 0.0}

BORA_72_dic = {'type': 'type_2', 'coin_No': 'KRW-BORA', 'coin_Name': 'KRW-BORA', 'ma_duration_long': 100, 'ma_duration_mid': 32, 'ma_duration_short': 57, 'ratio_ema_long_rise': 1.0, 'ratio_ema_mid_rise': 1.0003, 'recent_ratio_ema_long_plus': 0.0001, 'successive_rise': 11, 'ratio_ema_mid_long': 0.99, 'ratio_vol_curr_prior': 1.0, 'diff_m_l_factor': 0.0, 'diff_vol_aver': 1.0, 'under_long_duration': 44, 'recent_vol_duration': 9, 'sell_method_vol_cri': 0.9, 'ratio_peak_diff': 0.015, 'ratio_open_check': 1.0039, 'ratio_reduced': 9.0, 'ratio_prior_to_cur_long': 0.993, 'ratio_mean_long': 0.3, 'ratio_sell_forced': 0.07, 'bought_state': 0, 'bought_price': 0.0}


# In[4]:


LIST_target = [BTC_0_dic, ETH_1_dic, WAVES_7_dic, STEEM_11_dic, ETC_5_dic, BTG_20_dic, ARK_14_dic, WAXP_57_dic, QTUM_9_dic, BCH_30_dic, BORA_72_dic]


# In[5]:


len(LIST_target)


# In[6]:


transaction_fee_ratio = 0.0005 + 0.001   # 거래 수수료 비율 + 여유 마진


# In[7]:


#No_of_buyable_items = round(len(LIST_target) * 0.7)   # 동시에 매수 상태일수 있는 최대 종목 수

No_of_buyable_items = 5

print ('No_of_buyable_items :', No_of_buyable_items)


# In[8]:



buyable_budget_ratio = [ ((1 / (No_of_buyable_items - 0)) - transaction_fee_ratio), ((1 / (No_of_buyable_items - 1)) - transaction_fee_ratio), ((1 / (No_of_buyable_items - 2)) - transaction_fee_ratio), ((1 / (No_of_buyable_items - 3)) - transaction_fee_ratio), ((1 / (No_of_buyable_items - 4)) - transaction_fee_ratio)]

'''
buyable_budget_ratio_1 = 0.333 - transaction_fee_ratio - 0.001     # 0.333..  보다 살짝 작은 수치
buyable_budget_ratio_2 = 0.5 - transaction_fee_ratio - 0.001     # 0.5  보다 살짝 작은 수치
buyable_budget_ratio_3 = 1 - transaction_fee_ratio - 0.001     # 1  보다 살짝 작은 수치
'''

time_factor = 9   # 클라우드 서버와 한국과의 시차

check_currency = 'KRW'


# In[9]:


#업비트 계정 설정


# 클라우드용 API 키
access_key = "obNlDOPCCovskd4j3xVrx8taelkC2mJTRN6pxQm2"
secret_key = "VWSFHDTHzPGb0XQ6xZ0aZCFZz5ZsP7sU2zTuxxzt"

'''
# 집 PC용 API 키
access_key = "6Lncpb5qFIVNgqrD08dlefkRSYxTthq6uR2aA3iW"
secret_key = "JbxXQxXQ7HxOxySTFLKBqor8rBhsvbGW5HK3Z9PP"
'''

upbit = pyupbit.Upbit(access_key, secret_key)


# In[10]:


candle_type = '60min'
#candle_type = 'day'

if candle_type == '1min' :
    candle_adapt = 'minute1'
    time_unit = 1
elif candle_type == '3min' :
    candle_adapt = 'minute3'
    time_unit = 3
elif candle_type == '5min' :
    candle_adapt = 'minute5'
    time_unit = 5
elif candle_type == '10min' :
    candle_adapt = 'minute10'
    time_unit = 10
elif candle_type == '15min' :
    candle_adapt = 'minute15'
    time_unit = 15
elif candle_type == '30min' :
    candle_adapt = 'minute30'
    time_unit = 30
elif candle_type == '60min' :
    candle_adapt = 'minute60'
    time_unit = 60
elif candle_type == '240min' :
    candle_adapt = 'minute240'
    time_unit = 240
elif candle_type == 'day' :
    candle_adapt = 'day'
    time_unit = (60 * 24)
elif candle_type == 'month' :
    candle_adapt = 'month'
    time_unit = 60 * 24 * 30


# In[11]:


# Test setting
vol_duration = 12
buy_price_up_unit = 1


# In[12]:



# 코인번호로 코인 명칭 추출
tickers = pyupbit.get_tickers()

LIST_coin_KRW = []

for i in range (0, len(tickers), 1):
    if tickers[i][0:3] == 'KRW':
        LIST_coin_KRW.append(tickers[i])

LIST_check_coin_currency = []

for i in range (0, len(LIST_coin_KRW), 1):
    LIST_check_coin_currency.append(LIST_coin_KRW[i][4:])

LIST_check_coin_currency_2 = []

for i in range (0, len(LIST_check_coin_currency), 1) :
    temp = 'KRW-' + LIST_check_coin_currency[i]
    LIST_check_coin_currency_2.append(temp)


# In[13]:


#LIST_check_coin_currency


# In[14]:


# 매수 최소단위 산출

def unit_value_calc (DF_test) :
    unit_factor = 0
    unit_value = 0
        
    if DF_test['open'][-1] >= 1000000 :  # 200만원 이상은 거래단위가 1000원, 100~200만원은 거래단위가 500원이지만 편의상 200만원 이상과 함께 처리
        unit_factor = -3
        unit_value = 1000
    elif DF_test['open'][-1] >= 100000 :
        unit_factor = -2
        unit_value = 50
    elif DF_test['open'][-1] >= 10000 :
        unit_factor = -1
        unit_value = 10
    elif DF_test['open'][-1] >= 1000 :
        unit_factor = -1
        unit_value = 5
    elif DF_test['open'][-1] >= 100 :
        unit_factor = 0
        unit_value = 1
    else :
        unit_factor = 1
        unit_value = 0.1
    
    print ('DF_test[open][-1] : {0}  /  unit_factor : {1}  /  unit_value : {2}'.format(DF_test['open'][-1], unit_factor, unit_value))
        
    return unit_value


# In[15]:


# 몇건의 과거 이력을 참조할 것인가

candle_count = round((60/time_unit) * 24 * 300)


# In[16]:


# 잔고 조회, 현재가 조회 함수 정의

def get_balance(target_currency):   # 현급 잔고 조회
    """잔고 조회"""
    balances = upbit.get_balances()   # 통화단위, 잔고 등이 Dictionary 형태로 balance에 저장
    for b in balances:
        if b['currency'] == target_currency:   # 화폐단위('KRW', 'KRW-BTC' 등)에 해당하는 잔고 출력
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_balance_locked(target_currency):   # 거래가 예약되어 있는 잔고 조회
    """잔고 조회"""
    balances = upbit.get_balances()   # 통화단위, 잔고 등이 Dictionary 형태로 balance에 저장
    for b in balances:
        if b['currency'] == target_currency:   # 화폐단위('KRW', 'KRW-BTC' 등)에 해당하는 잔고 출력
            if b['locked'] is not None:
                return float(b['locked'])
            else:
                return 0
    return 0

def get_avg_buy_price(target_currency):   # 거래가 예약되어 있는 잔고 조회
    """평균 매수가 조회"""
    balances = upbit.get_balances()   # 통화단위, 잔고 등이 Dictionary 형태로 balance에 저장
    for b in balances:
        if b['currency'] == target_currency:   # 화폐단위('KRW', 'KRW-BTC' 등)에 해당하는 잔고 출력
            if b['avg_buy_price'] is not None:
                return float(b['avg_buy_price'])
            else:
                return 0
    return 0

'''
def get_current_price(invest_coin):
    """현재가 조회"""
    #return pyupbit.get_orderbook(tickers=invest_coin)[0]["orderbook_units"][0]["ask_price"]
    return pyupbit.get_current_price(invest_coin)
'''
#price = pyupbit.get_current_price("KRW-BTC")


# In[17]:


#upbit.get_balances()


# In[18]:


# Type_0 방식 매수/매도 함수 정의

def type_0_buy_sell_normal (target_dic) :
    
    coin_inv = target_dic['coin_Name']
    
    print('\n\ncheck_coin :', coin_inv)
    
    # Buy logic 점검
    
    if target_dic['bought_state'] == 0 :   # 매수가 없는 상태라면 
        
        # 전처리
        
        print ('\nCheking coin is {0}_{1}:'.format(coin_inv, target_dic['coin_No']))
        
        DF_vol_ref = pyupbit.get_ohlcv(coin_inv, count = vol_duration, interval = 'month')
        ref_vol = DF_vol_ref['volume'].sum() / (24 * 30 * vol_duration)
        
        DF_check = pyupbit.get_ohlcv(coin_inv, count = candle_count, interval = candle_adapt)
        
        DF_check['ratio_prior_to_cur'] = DF_check['open'] / DF_check['open'].shift(1)
        
        DF_check['ema_long'] = DF_check['open'].ewm(span = target_dic['ma_duration_long'], adjust=False).mean()
        DF_check['ema_mid'] = DF_check['open'].ewm(span = target_dic['ma_duration_mid'], adjust=False).mean()
        DF_check['ema_short'] = DF_check['open'].ewm(span = target_dic['ma_duration_short'], adjust=False).mean()
        
        DF_check['ratio_ema_long'] = DF_check['ema_long'] / DF_check['ema_long'].shift(1)
        
        DF_check['fall_check'] = 0
        DF_check.loc[(DF_check['ratio_ema_long'] < 1), 'fall_check'] = 1
        
        DF_check['ratio_ema_mid'] = DF_check['ema_mid'] / DF_check['ema_mid'].shift(1)
        
        DF_check['rise_check_mid'] = 0
        DF_check.loc[(DF_check['ratio_ema_mid'] > 1), 'rise_check_mid'] = 1
        
        DF_check['ratio_ema_short'] = DF_check['ema_short'] / DF_check['ema_short'].shift(1)
        
        DF_check['rise_check_short'] = 0
        DF_check.loc[(DF_check['ratio_ema_short'] > 1), 'rise_check_short'] = 1
        
        DF_check['diff_m_l'] = DF_check['ema_mid'] - DF_check['ema_long']
        
        DF_check['mid_under_long'] = 0
        DF_check.loc[(DF_check['diff_m_l'] > 0), 'mid_under_long'] = 1
        
        DF_check['ref_vol'] = 0.0
        DF_check['ref_vol'] = DF_check['volume'].ewm(span = (1 * target_dic['ref_vol_duration']), adjust = False).mean()
        DF_check['ref_vol_amount'] = 0.0
        
        DF_check.loc[(DF_check['ref_vol'] >= (3.0 * ref_vol)), 'ref_vol_amount'] = 3.0
        DF_check.loc[(DF_check['ref_vol'] < (3.0 * ref_vol)) & (DF_check['ref_vol'] >= (2.5 * ref_vol)), 'ref_vol_amount'] = 2.5
        DF_check.loc[(DF_check['ref_vol'] < (2.5 * ref_vol)) & (DF_check['ref_vol'] >= (2.0 * ref_vol)), 'ref_vol_amount'] = 2.0
        DF_check.loc[(DF_check['ref_vol'] < (2.0 * ref_vol)) & (DF_check['ref_vol'] >= (1.5 * ref_vol)), 'ref_vol_amount'] = 1.5
        DF_check.loc[(DF_check['ref_vol'] < (1.5 * ref_vol)) & (DF_check['ref_vol'] >= (1.0 * ref_vol)), 'ref_vol_amount'] = 1.0
        DF_check.loc[(DF_check['ref_vol'] < (1.0 * ref_vol)) & (DF_check['ref_vol'] >= (0.5 * ref_vol)), 'ref_vol_amount'] = 0.5
        DF_check.loc[(DF_check['ref_vol'] < (0.5 * ref_vol)), 'ref_vol_amount'] = 0  
        
        #print ('DF_check :\n', DF_check)
        

        
        # Buy logic
        
        investable_budget = 0
        
        No_of_bought_items = len(upbit.get_balances())
        
        '''                
        print('No_of_bought_items < No_of_buyable_items _____ {0} < {1}'.format(No_of_bought_items, No_of_buyable_items))
        print('DF_check[ratio_ema_long][-4] & [-3] & [-2] > criteria _____ {0} & {1} & {2} > {3}'.format(DF_check['ratio_ema_long'][-4], DF_check['ratio_ema_long'][-3], DF_check['ratio_ema_long'][-2], target_dic['ratio_ema_long_rise']))
        print('DF_check[ratio_ema_long][-1] > criteria _____ {0} & {1}'.format(DF_check['ratio_ema_long'][-1], (target_dic['ratio_ema_long_rise'] + target_dic['recent_ratio_ema_long_plus'])))
        print('DF_check[ratio_ema_mid][-1] > criteria _____ {0} > {1}'.format(DF_check['ratio_ema_mid'][-1], target_dic['ratio_ema_mid_rise']))
        print('DF_check.iloc[-target_dic[successive_rise] : ][rise_check_short].sum() >= (target_dic[successive_rise] - 2) _____ {0} >= {1}'.format(DF_check.iloc[-target_dic['successive_rise'] : ]['rise_check_short'].sum(), (target_dic['successive_rise'] - 2)))
        print('(DF_check[ema_mid][-1] / DF_check[ema_long][-1]) > target_dic[ratio_ema_mid_long] _____ {0} > {1}'.format((DF_check['ema_mid'][-1] / DF_check['ema_long'][-1]), target_dic['ratio_ema_mid_long']))
        print('(DF_check[ref_vol_amount][-2] >= target_dic[coe_vol_comp]) and (DF_check[ref_vol_amount][-2] >= DF_check[ref_vol_amount][-3]) and (DF_check[ref_vol_amount][-2] >= DF_check[ref_vol_amount][-4]) _____ {0} > {1} & {2} & {3}'.\
              format(DF_check['ref_vol_amount'][-2], target_dic['coe_vol_comp'], DF_check['ref_vol_amount'][-3], DF_check['ref_vol_amount'][-4]))
        print('(-DF_check.loc[DF_check.iloc[-(target_dic[under_long_duration] + 1) : -1][diff_m_l].idxmin()][diff_m_l] > (target_dic[diff_m_l_factor] * DF_check[open][-1]) _____ {0} > {1}'.\
              format(-DF_check.loc[DF_check.iloc[-(target_dic['under_long_duration'] + 1) : -1]['diff_m_l'].idxmin()]['diff_m_l'], (target_dic['diff_m_l_factor'] * DF_check['open'][-1])))
        '''
                       
        
        if (No_of_bought_items <= No_of_buyable_items) and         (DF_check['ratio_ema_long'][-4] > target_dic['ratio_ema_long_rise']) and (DF_check['ratio_ema_long'][-3] > target_dic['ratio_ema_long_rise']) and (DF_check['ratio_ema_long'][-2] > target_dic['ratio_ema_long_rise']) and         (DF_check['ratio_ema_long'][-1] > (target_dic['ratio_ema_long_rise'] + target_dic['recent_ratio_ema_long_plus'])) and (DF_check['ratio_ema_mid'][-1] > target_dic['ratio_ema_mid_rise']) and         (DF_check.iloc[-(target_dic['successive_rise'] + 2) : ]['rise_check_short'].sum() >= (target_dic['successive_rise'] - 2)) and         ((DF_check['ema_mid'][-1] / DF_check['ema_long'][-1]) > target_dic['ratio_ema_mid_long']) and         (DF_check['ref_vol_amount'][-2] >= target_dic['coe_vol_comp']) and (DF_check['ref_vol_amount'][-2] >= DF_check['ref_vol_amount'][-3]) and (DF_check['ref_vol_amount'][-2] >= DF_check['ref_vol_amount'][-4]) and         (-DF_check.loc[DF_check.iloc[-(target_dic['under_long_duration'] + 1) : -1]['diff_m_l'].idxmin()]['diff_m_l'] > (target_dic['diff_m_l_factor'] * DF_check['open'][-1])) :
            
            print ('$$$$$ [{0}] buying_transaction is coducting $$$$$'.format(coin_inv))
            
            
            if (No_of_bought_items - 1) == 1 :
                investable_budget = get_balance(check_currency) * buyable_budget_ratio[0]
            elif (No_of_bought_items - 1) == 2 :
                investable_budget = get_balance(check_currency) * buyable_budget_ratio[1]
            elif (No_of_bought_items - 1) == 3 :
                investable_budget = get_balance(check_currency) * buyable_budget_ratio[2]
            elif (No_of_bought_items - 1) == 4 :
                investable_budget = get_balance(check_currency) * buyable_budget_ratio[3]
            elif (No_of_bought_items - 1) == 5 :
                investable_budget = get_balance(check_currency) * buyable_budget_ratio[4]
            
            
            currrent_price = pyupbit.get_current_price(coin_inv)
            print ('\ncurrent_price : ', currrent_price)
            buyable_price = currrent_price + (buy_price_up_unit * unit_value_calc(DF_check))
            buying_volume = investable_budget / buyable_price
            print ('investable_budget : {0} / buyable_price : {1} / buying_volume : {2}'.format(investable_budget, buyable_price, buying_volume))
            
            #transaction_buy = upbit.buy_market_order(coin_inv, investable_budget)   # 시장가로 매수
            transaction_buy1 = upbit.buy_limit_order(coin_inv, buyable_price, buying_volume)   # 지정가로 매수
            time.sleep(30)            
            print ('buy_1ST_transaction_result :', transaction_buy1)
            print ('time : {0}  /  buying_target_volume : {1}  /  bought_volume_until_now : {2}'.format((datetime.datetime.now() + datetime.timedelta(seconds = (time_factor*3600))), buying_volume, get_balance(coin_inv[4:])))
            
            transaction_buy_cancel1 = upbit.cancel_order(transaction_buy1['uuid'])
            
            #target_dic['bought_state'] = 1
            #target_dic['buy_signal_flag'] = 1
            target_dic['bought_time'] = datetime.datetime.now() + datetime.timedelta(seconds = (time_factor * 3600))

                        
    # 매수상태 점검
        
    if get_balance(coin_inv[4:]) > 0 :
        target_dic['bought_state'] = 1
        print ('bought_state_in mid check : {0}'.format(target_dic['bought_state']))
    else :
        target_dic['bought_state'] = 0
        print ('bought_state_in mid check : {0}'.format(target_dic['bought_state']))
    
    
    
            
        
    # Sell logic
    if target_dic['bought_state'] == 1 :   # 매수가 되어 있는 상태라면
        
        current_time = datetime.datetime.now() + datetime.timedelta(seconds = (time_factor * 3600))
            
        print ('Now : ', current_time)        

        target_coin = target_dic['coin_Name']
        
        time_elapse_bought = math.ceil(((current_time - target_dic['bought_time']).days * 24) + (current_time - target_dic['bought_time']).seconds / 3600)
        
        DF_check_peak = pyupbit.get_ohlcv(target_coin, count=round(time_elapse_bought + target_dic['ma_duration_long'] + 1000), interval = candle_adapt)
        
        DF_check_peak['ratio_prior_to_cur'] = DF_check_peak['open'] / DF_check_peak['open'].shift(1)
        DF_check_peak['gap_prior_to_1'] = abs(1 - DF_check_peak['ratio_prior_to_cur'])
        
        DF_check_peak['ema_short'] = DF_check_peak['open'].ewm(span = target_dic['ma_duration_short'], adjust=False).mean()
        DF_check_peak['ema_mid'] = DF_check_peak['open'].ewm(span = target_dic['ma_duration_mid'], adjust=False).mean()
        DF_check_peak['ema_long'] = DF_check_peak['open'].ewm(span = target_dic['ma_duration_long'], adjust=False).mean()
        
        DF_check_peak['ema_sell_ma_duration_1'] = DF_check_peak['open'].ewm(span = target_dic['sell_ma_duration_1'], adjust=False).mean()
        
        DF_check_peak['ratio_ema_short'] = DF_check_peak['ema_short'] / DF_check_peak['ema_short'].shift(1)
        DF_check_peak['ratio_ema_mid'] = DF_check_peak['ema_mid'] / DF_check_peak['ema_mid'].shift(1)
        DF_check_peak['ratio_ema_long'] = DF_check_peak['ema_long'] / DF_check_peak['ema_long'].shift(1)
        
                
        print('Cheking Peak_difference with coin :', target_coin)
        
        '''
        print('(DF_check_peak[volume][-2] < (target_dic[sell_method_vol_cri] * DF_check_peak.iloc[(-5) : -2][volume].mean())) _____ {0} < {1}'.format(DF_check_peak['volume'][-2], (target_dic['sell_method_vol_cri'] * DF_check_peak.iloc[(-5) : -2]['volume'].mean())))
        print('((DF_check_peak.loc[DF_check_peak.iloc[-time_elapse_bought : ][ratio_ema_long].idxmax()][ratio_ema_long] - DF_check_peak[ratio_ema_long][-1] >  target_dic[ratio_peak_diff]) ____ {0} > {1}'. \
                    format((DF_check_peak.loc[DF_check_peak.iloc[-time_elapse_bought : ]['ratio_ema_long'].idxmax()]['ratio_ema_long'] - DF_check_peak['ratio_ema_long'][-1]), target_dic['ratio_peak_diff']))
        
        print('Or (DF_check_peak[ratio_ema_mid][-1] < target_dic[ratio_sell_ema_mid]) ____ {0} < {1}'.format(DF_check_peak['ratio_ema_mid'][-1], target_dic['ratio_sell_ema_mid']))
        '''
        
        
        if (time_elapse_bought > 1) and (DF_check_peak['volume'][-2] < (target_dic['sell_method_vol_cri'] * DF_check_peak.iloc[-5 : -2]['volume'].mean())) and         (((DF_check_peak['ema_sell_ma_duration_1'][-1] / DF_check_peak.loc[DF_check_peak.iloc[-(time_elapse + 1) : -1]['high'].idxmax()]['high']) < target_dic['ratio_peak_diff']) or          (DF_check_peak['ratio_ema_mid'][-1] < target_dic['ratio_sell_ema_mid'])) :
            
            transaction_sell = upbit.sell_market_order(target_coin, get_balance(target_coin[4:]))  # 시장가에 매도
            time.sleep(5)
            print('\nnow :', (datetime.datetime.now() + datetime.timedelta(seconds=(time_factor * 3600))))
            print('sell_transaction_result_by_ Peak_difference :', transaction_sell)
            
            target_dic['bought_state'] = 0
            target_dic['bought_price'] = 0.0
            target_dic['bought_time'] = 0.0
            
            time.sleep(5)
            
        
        print('Cheking Ratio_trend sell with coin :', target_coin)
        
        '''
        print('(DF_check_peak.iloc[-11 : -1][high].std() < (target_dic[ratio_std_1] * DF_check_peak.iloc[-(time_elapse_bought + 5 + 1) : -(time_elapse_bought - 5 + 1)][high].std())) _____ {0} < {1}'.\
              format(DF_check_peak.iloc[-11 : -1]['high'].std(), (target_dic['ratio_std_1'] * DF_check_peak.iloc[-(time_elapse_bought + 5 + 1) : -(time_elapse_bought - 5 + 1)]['high'].std())))
        print('(DF_check_peak.iloc[-6 : -1][high].std() < (target_dic[ratio_std_2] * DF_check_peak.iloc[-(time_elapse_bought + 5 + 1) : -(time_elapse_bought - 5 + 1)][high].std())) _____ {0} < {1}'.\
              format(DF_check_peak.iloc[-6 : -1]['high'].std(), (target_dic['ratio_std_2'] * DF_check_peak.iloc[-(time_elapse_bought + 5 + 1) : -(time_elapse_bought - 5 + 1)]['high'].std())))
        print('(DF_check_peak[open][-1] < DF_check_peak[open][-2]) and (DF_check_peak[open][-1] < DF_check_peak[open][-4]) and (DF_check_peak[open][-1] < DF_check_peak[open][-7]) ___ {0} < {1}_{2}_{3}'.\
              format(DF_check_peak['open'][-1], DF_check_peak['open'][-2], DF_check_peak['open'][-4], DF_check_peak['open'][-7]))
        '''
                     
        
        if (time_elapse_bought > 5) and         (((DF_check_peak.iloc[-11 : -1]['high'].std() < (target_dic['ratio_std_1'] * DF_check_peak.iloc[-(time_elapse_bought + 5 + 1) : -(time_elapse_bought - 5 + 1)]['high'].std())) and         (DF_check_peak.iloc[-6 : -1]['high'].std() < (target_dic['ratio_std_2'] * DF_check_peak.iloc[-(time_elapse_bought + 5 + 1) : -(time_elapse_bought - 5 + 1)]['high'].std()))) or          ((DF_check_peak.iloc[-11: -1]['low'].std() < (target_dic['ratio_std_1'] * DF_check_peak.iloc[-(time_elapse_bought + 5 + 1) : -(time_elapse_bought - 5 + 1)]['low'].std())) and           (DF_check_peak.iloc[-6 : -1]['low'].std() < (target_dic['ratio_std_2'] * DF_check_peak.iloc[-(time_elapse_bought + 5 + 1) : -(time_elapse_bought - 5 + 1)]['low'].std())))) and         (DF_check_peak['open'][-1] < DF_check_peak['open'][-2]) and (DF_check_peak['open'][-1] < DF_check_peak['open'][-4]) and (DF_check_peak['open'][-1] < DF_check_peak['open'][-7]) :
            
            transaction_sell = upbit.sell_market_order(target_coin, get_balance(target_coin[4:]))  # 시장가에 매도
            time.sleep(5)
            print('\nnow :', (datetime.datetime.now() + datetime.timedelta(seconds=(time_factor * 3600))))
            print('sell_transaction_result_by_ Ratio_trend :', transaction_sell)
            
            target_dic['bought_state'] = 0
            target_dic['bought_price'] = 0.0
            target_dic['bought_time'] = 0.0
            
            time.sleep(5)
            
        
        '''
        print ('DF_check_peak.loc[DF_check_peak.iloc[-13 : -1][ratio_prior_to_cur].idxmax()][ratio_prior_to_cur] < target_dic[ratio_open_check] _____ {0} < {1}'.\
               format(DF_check_peak.loc[DF_check_peak.iloc[-13 : -1]['ratio_prior_to_cur'].idxmax()]['ratio_prior_to_cur'], target_dic['ratio_open_check']))
        print ('DF_check_peak[ratio_prior_to_cur][-13 : -1].mean() < target_dic[ratio_prior_to_cur_long] _____ {0} < {1}'.\
               format(DF_check_peak['ratio_prior_to_cur'][-13 : -1].mean(), target_dic['ratio_prior_to_cur_long']))
        print ('DF_check_peak.iloc[-25 : -1][gap_prior_to_1].mean() < (target_dic[ratio_mean_long] * DF_check_peak.iloc[(50 * 24) : ][gap_prior_to_1].mean()) _____ {0} < {1}'.\
               format(DF_check_peak.iloc[-25 : -1]['gap_prior_to_1'].mean(), (target_dic['ratio_mean_long'] * DF_check_peak.iloc[(50 * 24) : ]['gap_prior_to_1'].mean())))
        '''
        
        if (time_elapse_bought > 5) and         ((DF_check_peak['ema_long'][-1] / DF_check_peak['ema_long'][-(time_elapse_bought + 1)]) < 1.0) and         ((DF_check_peak['ema_mid'][-1] / DF_check_peak['ema_mid'][-(time_elapse_bought + 1)]) < 1.0) and         ((DF_check_peak['ema_sell_ma_duration_1'][-1] / DF_check_peak['ema_sell_ma_duration_1'][-(time_elapse_bought + 1)]) < 1.0) :
            
            transaction_sell = upbit.sell_market_order(target_coin, get_balance(target_coin[4:]))  # 시장가에 매도
            time.sleep(5)
            print('\nnow :', (datetime.datetime.now() + datetime.timedelta(seconds=(time_factor * 3600))))
            print('sell_transaction_result_by_ EMA long and mid and ma_duration_1 are below 1 compare to buying timing :', transaction_sell)
            
            target_dic['bought_state'] = 0
            target_dic['bought_price'] = 0.0
            target_dic['bought_time'] = 0.0
            
            time.sleep(5)
            


# In[19]:


# Type_2 방식 매수/매도 함수 정의

def type_2_buy_sell_normal (target_dic) :
    
    #coin_inv = LIST_check_coin_currency_2[target_dic['coin_No']]
    coin_inv = target_dic['coin_Name']
    
    print('\n\ncheck_coin :', coin_inv)
    
    # Buy logic 점검
    
    if target_dic['bought_state'] == 0 :   # 매수가 없는 상태라면 
        
        # 전처리
        
        print ('\nCheking coin is {0}_{1}:'.format(coin_inv, target_dic['coin_No']))
        
        DF_vol_ref = pyupbit.get_ohlcv(coin_inv, count = vol_duration , interval = 'month')
        ref_vol = DF_vol_ref['volume'].sum() / (24 * 30 * vol_duration)
        
        DF_check = pyupbit.get_ohlcv(coin_inv, count=candle_count, interval=candle_adapt)
        
        DF_check['ratio_prior_to_cur'] = DF_check['open'] / DF_check['open'].shift(1)
        
        DF_check['ema_long'] = DF_check['open'].ewm(span = target_dic['ma_duration_long'], adjust=False).mean()
        DF_check['ema_mid'] = DF_check['open'].ewm(span = target_dic['ma_duration_mid'], adjust=False).mean()
        DF_check['ema_short'] = DF_check['open'].ewm(span = target_dic['ma_duration_short'], adjust=False).mean()
        
        DF_check['ratio_ema_long'] = DF_check['ema_long'] / DF_check['ema_long'].shift(1)
        
        DF_check['fall_check'] = 0
        DF_check.loc[(DF_check['ratio_ema_long'] < 1), 'fall_check'] = 1
        
        DF_check['ratio_ema_mid'] = DF_check['ema_mid'] / DF_check['ema_mid'].shift(1)
        
        DF_check['rise_check_mid'] = 0
        DF_check.loc[(DF_check['ratio_ema_mid'] > 1), 'rise_check_mid'] = 1
        
        DF_check['ratio_ema_short'] = DF_check['ema_short'] / DF_check['ema_short'].shift(1)
        
        DF_check['rise_check_short'] = 0
        DF_check.loc[(DF_check['ratio_ema_short'] > 1), 'rise_check_short'] = 1
        
        DF_check['diff_m_l'] = DF_check['ema_mid'] - DF_check['ema_long']
        
        DF_check['mid_under_long'] = 0
        DF_check.loc[(DF_check['diff_m_l'] > 0), 'mid_under_long'] = 1
        
        
        DF_check['vol_amount'] = 0.0
        
        DF_check.loc[(DF_check['volume'] >= (2.0 * DF_check.sort_values('volume', ascending = False).tail(round(0.9 * len(DF_check)))['volume'].mean())), 'vol_amount'] = 2.0
        DF_check.loc[(DF_check['volume'] < (2.0 * DF_check.sort_values('volume', ascending = False).tail(round(0.9 * len(DF_check)))['volume'].mean())) & (DF_check['volume'] >= (1.8 * DF_check.sort_values('volume', ascending = False).tail(round(0.9 * len(DF_check)))['volume'].mean())), 'vol_amount'] = 1.8
        DF_check.loc[(DF_check['volume'] < (1.8 * DF_check.sort_values('volume', ascending = False).tail(round(0.9 * len(DF_check)))['volume'].mean())) & (DF_check['volume'] >= (1.6 * DF_check.sort_values('volume', ascending = False).tail(round(0.9 * len(DF_check)))['volume'].mean())), 'vol_amount'] = 1.6
        DF_check.loc[(DF_check['volume'] < (1.6 * DF_check.sort_values('volume', ascending = False).tail(round(0.9 * len(DF_check)))['volume'].mean())) & (DF_check['volume'] >= (1.4 * DF_check.sort_values('volume', ascending = False).tail(round(0.9 * len(DF_check)))['volume'].mean())), 'vol_amount'] = 1.4
        DF_check.loc[(DF_check['volume'] < (1.4 * DF_check.sort_values('volume', ascending = False).tail(round(0.9 * len(DF_check)))['volume'].mean())) & (DF_check['volume'] >= (1.2 * DF_check.sort_values('volume', ascending = False).tail(round(0.9 * len(DF_check)))['volume'].mean())), 'vol_amount'] = 1.2
        DF_check.loc[(DF_check['volume'] < (1.2 * DF_check.sort_values('volume', ascending = False).tail(round(0.9 * len(DF_check)))['volume'].mean())) & (DF_check['volume'] >= (1.0 * DF_check.sort_values('volume', ascending = False).tail(round(0.9 * len(DF_check)))['volume'].mean())), 'vol_amount'] = 1.0
        DF_check.loc[(DF_check['volume'] < (1.0 * DF_check.sort_values('volume', ascending = False).tail(round(0.9 * len(DF_check)))['volume'].mean())) & (DF_check['volume'] >= (0.8 * DF_check.sort_values('volume', ascending = False).tail(round(0.9 * len(DF_check)))['volume'].mean())), 'vol_amount'] = 0.8
        DF_check.loc[(DF_check['volume'] < (0.8 * DF_check.sort_values('volume', ascending = False).tail(round(0.9 * len(DF_check)))['volume'].mean())) & (DF_check['volume'] >= (0.6 * DF_check.sort_values('volume', ascending = False).tail(round(0.9 * len(DF_check)))['volume'].mean())), 'vol_amount'] = 0.6
        DF_check.loc[(DF_check['volume'] < (0.6 * DF_check.sort_values('volume', ascending = False).tail(round(0.9 * len(DF_check)))['volume'].mean())) & (DF_check['volume'] >= (0.4 * DF_check.sort_values('volume', ascending = False).tail(round(0.9 * len(DF_check)))['volume'].mean())), 'vol_amount'] = 0.4
        DF_check.loc[(DF_check['volume'] < (0.4 * DF_check.sort_values('volume', ascending = False).tail(round(0.9 * len(DF_check)))['volume'].mean())) & (DF_check['volume'] >= (0.2 * DF_check.sort_values('volume', ascending = False).tail(round(0.9 * len(DF_check)))['volume'].mean())), 'vol_amount'] = 0.2
        
        DF_check['recent_vol_aver'] = 0.0
        
        for j in range (0, len(DF_check), 1) :
            DF_check['recent_vol_aver'][j] = DF_check.iloc[(j - target_dic['recent_vol_duration']) : j]['vol_amount'].sum()
        
        #print ('DF_check :\n', DF_check)
        
        
        # Buy logic
        
        investable_budget = 0
        
        No_of_bought_items = len(upbit.get_balances())
        
        '''                
        print('No_of_bought_items < No_of_buyable_items _____ {0} < {1}'.format(No_of_bought_items, No_of_buyable_items))        
        print('DF_check[ratio_ema_long][-3] & [-2] & [-1] > criteria _____ {0} & {1} & {2} > {3}'.format(DF_check['ratio_ema_long'][-3], DF_check['ratio_ema_long'][-2], DF_check['ratio_ema_long'][-1], target_dic['ratio_ema_long_rise']))
        print('DF_check[ratio_ema_mid][-1] > criteria _____ {0} > {1}'.format(DF_check['ratio_ema_mid'][-1], target_dic['ratio_ema_mid_rise']))
        print('DF_check.iloc[-(target_dic[successive_rise] + 2) : ][rise_check_short].sum() >= (target_dic[successive_rise] - 0) _____ {0} >= {1}'.\
              format(DF_check.iloc[-(target_dic['successive_rise'] + 2) : ]['rise_check_short'].sum(), (target_dic['successive_rise'] - 0)))
        print('DF_check[volume][-2] >= (target_dic[ratio_vol_curr_prior] * DF_check.iloc[-4 : -2][volume].mean()) _____ {0} >= {1}'.format(DF_check['volume'][-2], (target_dic['ratio_vol_curr_prior'] * DF_check.iloc[-4 : -2]['volume'].mean())))
        print('DF_check.iloc[-(target_dic[under_long_duration] + 1) : -1][mid_under_long].sum() _____ {0} == 0'.format(DF_check.iloc[-(target_dic['under_long_duration'] + 1) : -1]['mid_under_long'].sum()))
        print('-DF_check.loc[DF_check.iloc[-(target_dic[under_long_duration] + 1) : -1][diff_m_l].idxmin()][diff_m_l] > (target_dic[diff_m_l_factor] * DF_check[open][-1]) _____ {0} > {1}'.\
              format(-DF_check.loc[DF_check.iloc[-(target_dic['under_long_duration'] + 1) : -1]['diff_m_l'].idxmin()]['diff_m_l'], (target_dic['diff_m_l_factor'] * DF_check['open'][-1])))
        print('(DF_check.loc[DF_check.iloc[-6 : -2][recent_vol_aver].idxmax()][recent_vol_aver] - DF_check[recent_vol_aver][-2]) < target_dic[diff_vol_aver]) _____ {0} < {1}'.\
              format((DF_check.loc[DF_check.iloc[-6 : -2]['recent_vol_aver'].idxmax()]['recent_vol_aver'] - DF_check['recent_vol_aver'][-2]), target_dic['diff_vol_aver']))
        print('(DF_check[ema_mid][-1] / DF_check[ema_long][-1]) > target_dic[ratio_ema_mid_long] _____{0} > {1}'.format((DF_check['ema_mid'][-1] / DF_check['ema_long'][-1]), target_dic['ratio_ema_mid_long']))
        '''
        
        if (No_of_bought_items <= No_of_buyable_items) and         (DF_check['ratio_ema_long'][-3] > target_dic['ratio_ema_long_rise']) and (DF_check['ratio_ema_long'][-2] > target_dic['ratio_ema_long_rise']) and (DF_check['ratio_ema_long'][-1] > (target_dic['ratio_ema_long_rise'] + target_dic['recent_ratio_ema_long_plus'])) and (DF_check['ratio_ema_mid'][-1] > target_dic['ratio_ema_mid_rise']) and         (DF_check.iloc[-(target_dic['successive_rise'] + 2) : ]['rise_check_short'].sum() >= (target_dic['successive_rise'] - 0)) and         (DF_check['volume'][-2] >= (target_dic['ratio_vol_curr_prior'] * DF_check.iloc[-4 : -2]['volume'].mean())) and         (DF_check.iloc[-(target_dic['under_long_duration'] + 1) : -1]['mid_under_long'].sum() == 0) and (-DF_check.loc[DF_check.iloc[-(target_dic['under_long_duration'] + 1) : -1]['diff_m_l'].idxmin()]['diff_m_l'] > (target_dic['diff_m_l_factor'] * DF_check['open'][-1])) and         ((DF_check.loc[DF_check.iloc[-6 : -2]['recent_vol_aver'].idxmax()]['recent_vol_aver'] - DF_check['recent_vol_aver'][-2]) < target_dic['diff_vol_aver']) and         ((DF_check['ema_mid'][-1] / DF_check['ema_long'][-1]) > target_dic['ratio_ema_mid_long']) :
            
            if (No_of_bought_items - 1) == 1 :
                investable_budget = get_balance(check_currency) * buyable_budget_ratio[0]
            elif (No_of_bought_items - 1) == 2 :
                investable_budget = get_balance(check_currency) * buyable_budget_ratio[1]
            elif (No_of_bought_items - 1) == 3 :
                investable_budget = get_balance(check_currency) * buyable_budget_ratio[2]
            elif (No_of_bought_items - 1) == 4 :
                investable_budget = get_balance(check_currency) * buyable_budget_ratio[3]
            elif (No_of_bought_items - 1) == 5 :
                investable_budget = get_balance(check_currency) * buyable_budget_ratio[4]
            
            
            
            print ('$$$$$ [{0}] buying_transaction is coducting $$$$$'.format(coin_inv))
            
            currrent_price = pyupbit.get_current_price(coin_inv)
            print ('\ncurrent_price : ', currrent_price)
            buyable_price = currrent_price + (buy_price_up_unit * unit_value_calc(DF_check))
            buying_volume = investable_budget / buyable_price
            print ('investable_budget : {0} / buyable_price : {1} / buying_volume : {2}'.format(investable_budget, buyable_price, buying_volume))
            
            #transaction_buy = upbit.buy_market_order(coin_inv, investable_budget)   # 시장가로 매수
            transaction_buy1 = upbit.buy_limit_order(coin_inv, buyable_price, buying_volume)   # 지정가로 매수
            time.sleep(30)            
            print ('buy_1ST_transaction_result :', transaction_buy1)
            print ('time : {0}  /  buying_target_volume : {1}  /  bought_volume_until_now : {2}'.format((datetime.datetime.now() + datetime.timedelta(seconds = (time_factor*3600))), buying_volume, get_balance(coin_inv[4:])))
            
            transaction_buy_cancel1 = upbit.cancel_order(transaction_buy1['uuid'])
            
            #target_dic['bought_state'] = 1
            #target_dic['buy_signal_flag'] = 1
            target_dic['bought_time'] = datetime.datetime.now() + datetime.timedelta(seconds = (time_factor * 3600))
                      

                        
    # 매수상태 점검
        
    if get_balance(coin_inv[4:]) > 0 :
        target_dic['bought_state'] = 1
        print ('bought_state_in mid check : {0}'.format(target_dic['bought_state']))
    else :
        target_dic['bought_state'] = 0
        print ('bought_state_in mid check : {0}'.format(target_dic['bought_state']))
    
    
    
            
        
    # Sell logic
    if target_dic['bought_state'] == 1 :   # 매수가 되어 있는 상태라면
        
        current_time = datetime.datetime.now() + datetime.timedelta(seconds = (time_factor * 3600))
            
        print ('Now : ', current_time)        

        target_coin = target_dic['coin_Name']
                
        time_elapse_bought = math.ceil(((current_time - target_dic['bought_time']).days * 24) + (current_time - target_dic['bought_time']).seconds / 3600)
                
        #time_auto_interm_sell_duration = round(target_dic['interm_sell_duration'] * (1 / 5))  
        
        DF_check_peak = pyupbit.get_ohlcv(target_coin, count=round(time_elapse_bought + target_dic['ma_duration_long'] + 1000), interval = candle_adapt)
        
        DF_check_peak['ratio_prior_to_cur'] = DF_check_peak['open'] / DF_check_peak['open'].shift(1)
        DF_check_peak['gap_prior_to_1'] = abs(1 - DF_check_peak['ratio_prior_to_cur'])
        
        DF_check_peak['ema_short'] = DF_check_peak['open'].ewm(span = target_dic['ma_duration_short'], adjust=False).mean()
        DF_check_peak['ema_long'] = DF_check_peak['open'].ewm(span = target_dic['ma_duration_long'], adjust=False).mean()
        
        DF_check_peak['ratio_ema_short'] = DF_check_peak['ema_short'] / DF_check_peak['ema_short'].shift(1)
        DF_check_peak['ratio_ema_long'] = DF_check_peak['ema_long'] / DF_check_peak['ema_long'].shift(1)
        
        print('Cheking Peak_difference with coin :', target_coin)
        
        '''
        print('(DF_check_peak[volume][-2] < (target_dic[sell_method_vol_cri] * DF_check_peak.iloc[(-5) : -2][volume].mean())) _____ {0} < {1}'.format(DF_check_peak['volume'][-2], (target_dic['sell_method_vol_cri'] * DF_check_peak.iloc[(-5) : -2]['volume'].mean())))
        print('((DF_check_peak.loc[DF_check_peak.iloc[-(time_elapse_bought + 1) : -1][ratio_ema_short].idxmax()][ratio_ema_short] - DF_check_peak[ratio_ema_short][-1]) >  target_dic[ratio_peak_diff]) ____ {0} > {1}'. \
              format((DF_check_peak.loc[DF_check_peak.iloc[-(time_elapse_bought + 1) : -1]['ratio_ema_short'].idxmax()]['ratio_ema_short'] - DF_check_peak['ratio_ema_short'][-1]), target_dic['ratio_peak_diff']))
        '''
        
        if (time_elapse_bought > 1) and (DF_check_peak['volume'][-2] < (target_dic['sell_method_vol_cri'] * DF_check_peak.iloc[(-5) : -2]['volume'].mean())) and         ((DF_check_peak.loc[DF_check_peak.iloc[-(time_elapse_bought + 1) : -1]['ratio_ema_short'].idxmax()]['ratio_ema_short'] - DF_check_peak['ratio_ema_short'][-1]) > target_dic['ratio_peak_diff']) :
            
            transaction_sell = upbit.sell_market_order(target_coin, get_balance(target_coin[4:]))  # 시장가에 매도
            time.sleep(5)
            print('\nnow :', (datetime.datetime.now() + datetime.timedelta(seconds=(time_factor * 3600))))
            print('sell_transaction_result_by_ Peak_difference :', transaction_sell)
            
            target_dic['bought_state'] = 0
            target_dic['bought_price'] = 0.0
            target_dic['bought_time'] = 0.0
            
            time.sleep(5)
            
        
        print('Cheking sell_forced_by_Peak with coin :', target_coin)
        
        '''
        print('(time_elapse_bought > 24 _____ {0} > 24'.format(time_elapse_bought))
        print('DF_check_peak.loc[DF_check_peak.iloc[-13 : -1][ratio_prior_to_cur].idxmax()][ratio_prior_to_cur] < target_dic[ratio_open_check] _____ {0} < {1}'.\
              format(DF_check_peak.loc[DF_check_peak.iloc[-13 : -1]['ratio_prior_to_cur'].idxmax()]['ratio_prior_to_cur'], target_dic['ratio_open_check']))
        print('DF_check_peak[ratio_prior_to_cur][-13 : -1].mean() < target_dic[ratio_prior_to_cur_long] _____ {0} < {1}'.\
              format(DF_check_peak['ratio_prior_to_cur'][-13 : -1].mean(), target_dic['ratio_prior_to_cur_long']))
        print('DF_check_peak.iloc[-25 : -1][gap_prior_to_1].mean() < (target_dic[ratio_mean_long] * (DF_check_peak.iloc[(50 * 24):][gap_prior_to_1].mean())) _____ {0} < {1}'.\
              format(DF_check_peak.iloc[-25 : -1]['gap_prior_to_1'].mean(), (target_dic['ratio_mean_long'] * (DF_check_peak.iloc[(50 * 24):]['gap_prior_to_1'].mean()))))
        '''
                     
        if (time_elapse_bought > 24) and         (DF_check_peak.loc[DF_check_peak.iloc[-13 : -1]['ratio_prior_to_cur'].idxmax()]['ratio_prior_to_cur'] < target_dic['ratio_open_check']) and         ((DF_check_peak['ratio_prior_to_cur'][-13 : -1].mean() < target_dic['ratio_prior_to_cur_long']) or          (DF_check_peak.iloc[-25 : -1]['gap_prior_to_1'].mean() < (target_dic['ratio_mean_long'] * (DF_check_peak.iloc[(50 * 24):]['gap_prior_to_1'].mean())))) :
            
            transaction_sell = upbit.sell_market_order(target_coin, get_balance(target_coin[4:]))  # 시장가에 매도
            time.sleep(5)
            print('\nnow :', (datetime.datetime.now() + datetime.timedelta(seconds=(time_factor * 3600))))
            print('sell_transaction_result_by_sell_forced_by_Peak :', transaction_sell)
            
            target_dic['bought_state'] = 0
            target_dic['bought_price'] = 0.0
            target_dic['bought_time'] = 0.0
            
            time.sleep(5)
            


# In[ ]:


while True:
    try:
        now = datetime.datetime.now() + datetime.timedelta(seconds=(time_factor * 3600))  # 클라우드 서버와 한국과의 시간차이 보정 (9시간)
        print('\n', now)

        if (0 < (now.minute % time_unit) <= 5) & (0 < (now.second % 60) <= 59):  # N시:01:00초 ~ N시:01:59초 사이 시각이면
            balances = upbit.get_balances()
            print('current_aseet_status\n', balances)

            for i in range(0, len(LIST_target), 1):
                if LIST_target[i]['type'] == 'type_0' :
                    buy_sell_check = type_0_buy_sell_normal (LIST_target[i])                    
                                   
                elif LIST_target[i]['type'] == 'type_2' :
                    buy_sell_check = type_2_buy_sell_normal (LIST_target[i])
                                    
                #buy_sell_check = buy_sell_normal(LIST_target[i])
                time.sleep(5)


        

        # 손실율이 임계수준을 초과하였을때 강제 매도
        for k in range(0, len(LIST_target), 1):
            coin_inv_2 = LIST_target[k]['coin_Name']

            if LIST_target[k]['bought_state'] == 1:
                print('[Radical falling] Cheking coin is :', coin_inv_2)
                print('Cheking radical falling over criteria Loss with coin :', coin_inv_2)
                print('(pyupbit.get_current_price(coin_inv_2) / get_avg_buy_price(coin_inv_2[4:])) < (1 - LIST_target[k][ratio_sell_forced]) ____ {0} < {1}'.                      format((pyupbit.get_current_price(coin_inv_2) / get_avg_buy_price(coin_inv_2[4:])), (1 - LIST_target[k]['ratio_sell_forced'])))

                if ((pyupbit.get_current_price(coin_inv_2) / get_avg_buy_price(coin_inv_2[4:])) < (1 - LIST_target[k]['ratio_sell_forced'])):
                    transaction_sell = upbit.sell_market_order(coin_inv_2, get_balance(coin_inv_2[4:]))  # 시장가에 매도
                    time.sleep(5)
                    print('\nnow :', (datetime.datetime.now() + datetime.timedelta(seconds=(time_factor * 3600))))
                    print('sell_transaction_result_by_ radical falling :', transaction_sell)

                    LIST_target[k]['bought_state'] = 0
                    LIST_target[k]['bought_price'] = 0.0
                    LIST_target[k]['bought_time'] = 0.0

                    time.sleep(5)

        time.sleep(10)

    except :
        print ('Error has occured!!!')
        err_msg = traceback.format_exc()
        print(err_msg)


# In[ ]:





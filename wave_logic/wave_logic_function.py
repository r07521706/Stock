import math
import datetime
import sys
sys.path.append("../")
from wave_info.deal_with_wave import *
from matplotlib import pyplot as plt
from FinMind.Data import Load
import numpy as np
import json
import pandas as pd
def stoploss_or_not(purchase_price,now_price,stop_loss_factor,wave_control_condition):
    if  purchase_price-now_price>purchase_price*(stop_loss_factor/100):
        return True
    elif now_price<wave_control_condition:
        return True
    else:
        return False

def book_profit_or_not(now_price,purchase_price,first_wave_gap,nfactor):
    if (now_price-purchase_price)>first_wave_gap*nfactor:
        return True
    else:
        return False

def buy_or_not(now_price,wave_control_condition,start_point):
    if now_price<wave_control_condition:
        return False
    elif now_price> start_point:
        return True

def test1(stock_id,some_days_ago=700,rolling_num=20,nfactor=1,stop_loss_factor=10):

    try:

        #資料準備區

        data                 = Load.FinData(dataset = 'TaiwanStockPrice',select = [str(stock_id)],date = str(datetime.date.today()-datetime.timedelta(days = some_days_ago)))#資料取得
        critical_point_data  =  get_critical_point(data,rolling_num)            #簡化波型(粗糙)
        simple_wave          =  get_simple_wave(critical_point_data)            #處理簡化過的波型 把兩個下跌的波整併成一個波
        wave_info            =  get_wave_info(simple_wave,critical_point_data)  #計算使用波浪理論需要的參數
        lose_list              = []
        earn_list              = []

        #邏輯運算區

        for i in wave_info[wave_info['type1_buy']].iterrows():
            #必要資訊
            start_index            = i[1]['next_index']         #起始日期的INDEX
            list_obj               = i[1]                       #上面那個表(essential_data)的一列
            now_index              = start_index                #開始迴圈時當前日期的index
            #邏輯資訊
            start_point            = list_obj['close']          #第一波的最高點 當超過最高點時就啟動了
            wave_control_condition = list_obj['last_mid_point'] #第一波的中間點 當低於這個點波型破壞
            first_wave_gap         = abs(start_point-wave_control_condition)*2
            purchase               = False
            purchase_price         = 0
            stop_loss_factor       = stop_loss_factor           #跌超過20%就停損
            nfactor                = nfactor                    #漲超過第一波的n倍就停利

            #logic compute
            while(now_index<=(len(data)-1)):
                now_price    =data['close'][now_index]
                now_index+=1
                if(purchase):

                            stoploss = stoploss_or_not(purchase_price,now_price,stop_loss_factor,wave_control_condition)

                            if  stoploss:
                                purchase         =False
                                lose_list.append([-now_price+purchase_price,now_price,start_index,now_index,first_wave_gap])
                                break

                            book_profit = book_profit_or_not(now_price,purchase_price,first_wave_gap,nfactor)

                            if book_profit:
                                purchase         =False
                                earn_list.append([now_price-purchase_price,now_price,start_index,now_index,first_wave_gap])
                                break

                elif(not purchase):

                            buy     =   buy_or_not(now_price,wave_control_condition,start_point)
                            if buy:
                                purchase       = True
                                purchase_price = now_price
                            else:
                                pass

        earn_list=pd.DataFrame(earn_list,columns=['賺了','當前價格','買入日','賣出日','波一漲幅'])
        earn_list['號碼']=stock_id
        lose_list=pd.DataFrame(lose_list,columns=['賠了','當前價格','買入日','賣出日','波一漲幅'])
        lose_list['號碼']=stock_id

        return [earn_list,lose_list]

    except KeyError:
        print('沒抓到資料')


if __name__ == "__main__":
    print("main exc")

import math
import datetime
from matplotlib import pyplot as plt
from FinMind.Data import Load
import numpy as np
import json
import pandas as pd
def get_critical_point(data,rolling_num):
    critical_point_data=pd.DataFrame()
    critical_point_data['close']=data['close']
    critical_point_data['rmax']=data['close'].rolling(rolling_num,min_periods=1,center=True).max()
    critical_point_data['rmin']=data['close'].rolling(rolling_num,center=True,min_periods=1).min()
    critical_point_data['critical']=np.logical_or(critical_point_data['close']==critical_point_data['rmax'],
                                                  critical_point_data['close']==critical_point_data['rmin'])
    return critical_point_data
def get_simple_wave(critical_point_data):
    critical_point_list=critical_point_data['critical']
    simple_wave       =critical_point_data[['close']][critical_point_list]
    simple_wave['index']= simple_wave.index
    simple_wave['gap']=simple_wave['close']-simple_wave['close'].shift(1)
    ans=map(lambda x:'up' if x>0  else 'down' if x<0 else 'flat' if x==0 else 'non',simple_wave['gap'])
    simple_wave['type']=list(ans)
    simple_wave=simple_wave[simple_wave['type']!='flat']
    simple_wave['next_type']=simple_wave['type'].shift(-1)
    simple_wave=simple_wave[simple_wave['next_type']!=simple_wave['type']]
    del simple_wave['next_type']
    return simple_wave

def get_wave_info(simple_wave,critical_point_data):
    wave_info=critical_point_data.iloc[simple_wave.index][['close']]
    wave_info['next_close']=wave_info['close'].shift(-1)
    wave_info['type']=simple_wave['type'].shift(-1)
    wave_info['mid_point']=(wave_info['close']+wave_info['close'].shift(-1))/2
    wave_info['last_mid_point']=wave_info['mid_point'].shift(1)
    wave_info['type1_buy']=np.logical_and(list(wave_info['type']=='down'),list(wave_info['next_close']>= wave_info['last_mid_point']))
    wave_info['type1_sell']=np.logical_and(list(wave_info['type']=='up'),list(wave_info['next_close']<wave_info['last_mid_point']))
    wave_info['index']=wave_info.index
    wave_info['next_index']=wave_info['index'].shift(-1)
    return wave_info

if __name__ == "__main__":
    print('main_excute')

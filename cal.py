from matplotlib import pyplot as plt
import warnings
import numpy as np


class stock_cal:
        
        def __init__(self,data):
            self.data=data
            self.plt_or_not=True
            s_point=None
            
            
        def make_line(self,plt_or_not,rolling_num=12):
            
            warnings.filterwarnings('ignore')
            data=self.data
            data['close'].plot(figsize=(16,9))
            #center 和 min_periods很重要
            data['rmax']=data['close'].rolling(rolling_num,min_periods=1,center=True).max()
            data['rmin']=data['close'].rolling(rolling_num,center=True,min_periods=1).min()
            data['local_max_or_not']=data['rmax']==data['close']
            data['local_min_or_not']=data['rmin']==data['close']
            data['critical_point']=data['local_max_or_not' or 'local_min_or_not']
            data['local_min_or_not'][len(data)-1]=True
            data['local_min_or_not'][len(data)-1]=True
            #data[['local_max_or_not']].iloc[59]=True
            #找到重要的直
            s=[]
            for i in data.itertuples():

                if i[13]==True or i[14]==True:

                    s.append(i[0])
            plt.plot(data['close'][s],'r-')
            if(not plt_or_not): 
                plt.close()
            self.data=data
            return s
        def get_slope(self,x,y):
#             s=self.s_point
            s1=x
            n1=np.array(y)

            s1=np.array(x)
            s2=s1[1:]#x後項
            s3=s1[:-1]#x前
            s4=s2-s3#後項減前項

            n2=n1[1:]#值得後項
            n3=n1[:-1]#值得前項
            n4=n2-n3

            slope=n4/s4

            return slope
        def get_wave_raw_data(self,x,slope):
            
            
            
            stack=[]
            s3=x
            wave_list=[]
            for i,k in zip(slope,s3):
                if len(stack)==0:
                    if i >0:
                        stack.append([i,k])

                else:#stack內有放東西了
                    if i==0:
                        if stack[-1][0]>0:
                            stack.append([i,k])
                    elif i<0:

                        if stack[-1][0]<0:
                            stack.append([i,k])

                        else:
                            stack.append([i,k])
                            wave_list.append(stack)
                            stack=[]
                    elif i>0:
                        stack.append([i,k])
            wave_list.append(stack)

            return wave_list
        
        
def get_complete_wave(sp,wave_raw_data,data):
    
    def get_largest_index_in_wave(d_col,start_end):
        max1=0
        indexa=0
        start=start_end[0]
        end=start_end[1]
        for i in range(start,end+1):
            if  d_col.iloc[i][0]>max1:
                max1=d_col.iloc[i][0]
                indexa=i
        #     print(data[['close']].iloc[i][0])
        # print(max1,indexa)
        return indexa
    
    l=[]
    for i in wave_raw_data:
        if(len(i)<2):
            pass
        else:
            index=0
            for j in sp:
                if j ==i[-1][1]:
                    break
                index+=1  
            #print("start:",i[0][1],"end:",sp[index+1])
            l.append((i[0][1],sp[index+1]))
            
    ll=[]
    for i in l:
        
        
        k=(get_largest_index_in_wave(data[['close']],i))
        ll.append((i[0],k,i[1]))
        
    return ll

def get_complete_wave(sp,wave_raw_data,data):
    
    def get_largest_index_in_wave(d_col,start_end):
        max1=0
        indexa=0
        start=start_end[0]
        end=start_end[1]
        for i in range(start,end+1):
            if  d_col.iloc[i][0]>max1:
                max1=d_col.iloc[i][0]
                indexa=i
        #     print(data[['close']].iloc[i][0])
        # print(max1,indexa)
        return indexa
    
    l=[]
    for i in wave_raw_data:
        if(len(i)<2):
            pass
        else:
            index=0
            for j in sp:
                if j ==i[-1][1]:
                    break
                index+=1  
            #print("start:",i[0][1],"end:",sp[index+1])
            l.append((i[0][1],sp[index+1]))
            
    ll=[]
    for i in l:
        
        #print(i)
        
        k=(get_largest_index_in_wave(data[['close']],i))
        ll.append((i[0],k,i[1]))
        
    return ll

def get_simple_wave_dig(sp,wave_raw_data,data):
    
    wave_start_end=get_complete_wave(sp,wave_raw_data,data)
    a1=[]
    gcw=wave_start_end
    for i in gcw:
        for j in i:
            a1.append(j)
    a1=list(set(a1))
    a1.sort()
    data['close'][a1].plot()
    return a1
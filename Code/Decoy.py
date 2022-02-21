import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#mean,std
#abc assortment
#abcd 
#Seasonality
data=pd.read_csv("sales#3.csv",index_col='Unnamed: 0')
print(data)
print(data.isnull().sum())

data_store=pd.read_csv("store.csv")

data_merged=pd.merge(data,data_store,on='Store',how='left')
print(data_merged)
#data_merged.to_csv("final.csv")
print(data_merged.isnull().sum())



DoW_pivot=data_merged.set_index('DayOfWeek')
DoW_pivot.sort_index()
DoW_pivot.drop(7,axis=0,inplace=True)
DoW_pivot.reset_index(inplace=True)
DoW_pivot.set_index(['Store','Date'],inplace=True)
#Sales_arr1=np.array(DoW_pivot.loc[1,'Sales'])
print(DoW_pivot)
#print(Sales_arr1)
m_std=[]
for i in range(1,1116):
    try:
        print(i,'  ',DoW_pivot.loc[i,'Sales'].mean(),'  ',np.std(DoW_pivot.loc[i,'Sales']))
    except:
        continue
#%% Validating Data
def valid_data(sales):
    SH=list(sales['StateHoliday'])
    ScH=list(sales['SchoolHoliday'])
    promo=list(sales['Promo'])
    DoW=list(sales['DayOfWeek'])
    Store=list(sales['Store'])
    Opn=list(sales['Open'])
    for i in DoW:
        if i in [1,2,3,4,5]:
            continue
        else:
            ValueError

    for i in Store:
        if i in range(1,1116):
            continue
        else:
            ValueError
        
    for i in ScH:
        if i in [1,0]:
            continue
        else:
            ValueError

    for i in promo:
        if i in [1,0]:
            continue
        else:
            ValueError

    for i in Opn:
        if i in [1,0]:
            continue
        else:
            ValueError
    
    for i in SH:
        if i in [1,0]:
            continue
        else:
            ValueError
valid_data(sales)

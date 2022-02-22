#%% Intro
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sales=pd.read_csv("D:\Rohit\Study Books\Sem - 6\LBP\Files\Files\sales.csv")
print(sales)
store=pd.read_csv("D:\Rohit\Study Books\Sem - 6\LBP\Files\Files\store.csv")
print(store)
#%% Changing State Holidays
def change_StateHolidays(sales):
    SH=list(sales['StateHoliday'])
    #ScH=list(sales['SchoolHoliday'])
    #promo=list(sales['Promo'])
    for i in range(len(SH)):
        try:
            if SH[i].isalpha(): #and promo[i]==0 and ScH[i]==1:
                SH[i]=1
            else:
                SH[i]=0
        except:
            continue
    sales.drop(['StateHoliday'],axis=1,inplace=True)
    sales.insert(loc=7,column="StateHoliday",value=SH)
    print(sales)
change_StateHolidays(sales)
#%% Sorting
sales=sales.sort_values(['Store','Date'])
print(sales)
#%% Cleansing
def remove_stores_with_missingData(sales):
    sales.set_index(['Store'],inplace=True)
    sales.sort_index()
    for i in range(1,1116):
        if len(sales.loc[i])!=942:
            sales.drop(i,axis=0,inplace=True)
    print(sales)
    sales.reset_index(inplace=True)
    print(sales)
remove_stores_with_missingData(sales)
#%% Checking for Null Values
print(sales.isnull().sum())        
#%% Merging and Checking for Null Values
merged_data=pd.merge(sales,store,on='Store',how='left')
print(merged_data)
#data_merged.to_csv("final.csv")
print(merged_data.isnull().sum())     
#%% Mean vs. STD plot
def mean_std(merged_data):
    merged_data1=merged_data.copy()
    merged_data1.set_index(['Store','Date'],inplace=True)
    print(merged_data1)
    lst_s=[]
    lst_m=[]
    lst_std=[]
    for i in range(1,1116):
        try:
            lst_s.append(i)
            lst_m.append(merged_data1.loc[i,'Sales'].mean())
            lst_std.append(np.std(merged_data1.loc[i,'Sales']))
        except:
            continue
    plt.style.use('seaborn')
    lst_s.append('Cumulative')
    lst_m.append(merged_data1['Sales'].mean())
    lst_std.append(np.std(merged_data1['Sales']))
    plt.scatter(lst_m,lst_std,linewidths=1,edgecolor='black')
    plt.ylabel('Standard Deviation')
    plt.xlabel('Mean')
    plt.title('Mean vs. STD chart')
mean_std(merged_data)
#%% Store Type Pie Chart 
def Store_type(merged_data):
    data=merged_data.copy()
    data.set_index(['StoreType'],inplace=True)
    data.sort_index()
    lst_type=['A','B','C','D']
    lst_m=[]
    for i in ['a','b','c','d']:
        try:
            lst_m.append(data.loc[i,'Sales'].mean())
        except:
            continue
    plt.pie(lst_m,labels=lst_type,colors=['r','g','b','y'],shadow=True,autopct = '%1.1f%%')
    plt.title('Store Type Effect on Sales')
    plt.show()
Store_type(merged_data)
#%% Assortment Type Pie Chart
def Assortment_type(merged_data):
    data=merged_data.copy()
    data.set_index(['Assortment'],inplace=True)
    data.sort_index()
    typ=['A','B','C']
    m=[]
    for i in ['a','b','c']:
        try:
            m.append(data.loc[i,'Sales'].mean())
        except:
            continue
    plt.pie(m,labels=typ,colors=['r','g','b'],shadow=True,autopct = '%1.1f%%')
    plt.title('Assortment Level Effect on Sales')
    plt.show()
Assortment_type(merged_data)
#%% Day of Week effect on Sales
def DoW_sales(merged_data):
    data=merged_data.copy()
    data.set_index(['DayOfWeek'],inplace=True)
    data.sort_index()
    lst=[]
    for i in range(1,8):
        lst.append(data.loc[i,'Sales'].mean())
    lst2=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    lst3=np.arange(len(lst2))
    plt.xticks(lst3,lst2)
    plt.title('Day of Week Effect on Sales')
    plt.ylabel('Mean Sales')
    plt.xlabel('Day of Week')
    plt.bar(lst3,lst)
DoW_sales(merged_data)
#%% School Holidays effect on Sales
def ScH_sales(merged_data):
    data=merged_data.copy()
    data.set_index('SchoolHoliday',inplace=True)
    data.sort_index()
    lst1=[data.loc[1,'Sales'].mean(),data.loc[0,'Sales'].mean()]
    lst2=['Yes','No']
    lst3=np.arange(len(lst2))
    plt.xticks(lst3,lst2)
    plt.title('School Holiday Effect on Sales')
    plt.ylabel('Mean Sales')
    plt.xlabel('Shool Holidays')
    plt.bar(lst3,lst1)
ScH_sales(merged_data)    
#%% State Holidays effect on Sales
def SH_sales(merged_data):
    data=merged_data.copy()
    data.set_index('StateHoliday',inplace=True)
    data.sort_index()
    lst1=[data.loc[1,'Sales'].mean(),data.loc[0,'Sales'].mean()]
    lst2=['Yes','No']
    lst3=np.arange(len(lst2))
    plt.xticks(lst3,lst2)
    plt.title('State Holiday Effect on Sales')
    plt.ylabel('Mean Sales')
    plt.xlabel('State Holidays')
    plt.bar(lst3,lst1)
SH_sales(merged_data)    
#%% Effect of Promo on Sales
def Promo_sales(merged_data):
    data=merged_data.copy()
    data.sort_values(['Promo','StoreType'],inplace=True)
    data.set_index(['Promo','StoreType','Store'],inplace=True)
    #print(data)  
    lst_m=[]
    lst_type=['A','B','C','D']
    lst_1=np.arange(len(lst_type))
    for i in range(0,2):
        lst=[]
        tmp=data.loc[i]
        for j in ['a','b','c','d']:
            lst.append(tmp.loc[j,'Sales'].mean())
        lst_m.append(lst)
    plt.xticks(lst_1,lst_type)
    plt.title('Effect of Promo on Sales')
    plt.ylabel('Mean Sales')
    plt.xlabel('Store Type')
    plt.bar(lst_1-0.2,lst_m[1],width=0.5,label='Yes')
    plt.bar(lst_1+0.2,lst_m[0],width=0.5,label='No')
    plt.legend()
    plt.show()
Promo_sales(merged_data)  

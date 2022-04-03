#%% Intro
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


sales=pd.read_csv("Files/sales.csv")
print(sales)
store=pd.read_csv("Files/store.csv")
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

#%% Changing to Date_time
print(sales['Date'].dtype)
sales['Date']=pd.to_datetime(sales['Date'])
print(sales['Date'].dtype)
print(sales)

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
    #print(merged_data1)
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

#%% Effect of Competition Distance
def Compdis_sales(merged_data):
    data=merged_data.copy()
    data.dropna(axis=0,subset=['CompetitionDistance'],how='any',inplace=True)
    #print(data.dtypes)    
    Min=data['CompetitionDistance'].min()
    Max=data['CompetitionDistance'].max()
    first=Min+((Max-Min)//4)
    second=Min+((Max-Min)//2)
    third=Max-((Max-Min)//4)
    lst=['Very Close','Close','Moderate','Far']
    lst1=np.arange(len(lst))
    vc=data.loc[(data['CompetitionDistance'] >= Min)&(data['CompetitionDistance'] < first),'Sales'].mean()
    c=data.loc[(data['CompetitionDistance'] >= first)&(data['CompetitionDistance'] < second),'Sales'].mean()
    m=data.loc[(data['CompetitionDistance'] >= second)&(data['CompetitionDistance'] < third),'Sales'].mean()
    f=data.loc[data['CompetitionDistance'] >= third,'Sales'].mean()
    lst2=[vc,c,m,f]
    plt.xticks(lst1,lst)
    plt.title('Effect of Competition Distance on Sales')
    plt.ylabel('Mean Sales')
    plt.xlabel('Competition Distance')
    plt.bar(lst1,lst2,width=0.5)
    plt.show()
Compdis_sales(merged_data)

#%% Removing Competition info
merged_data.drop(['CompetitionDistance','CompetitionOpenSinceMonth','CompetitionOpenSinceYear'],axis=1,inplace=True)
print(merged_data.head()) 
merged_data.to_csv("D:/Rohit/Study Books/Sem - 6/LBP/Files/Files/Final.csv")
#%% StoreType Variation of Sales with Promos
def Storetype_promos(merged_data):
    data=merged_data.copy()
    data.sort_values(['StoreType','Promo','Date'],inplace=True)
    data.set_index(['StoreType','Promo','Date','Store'],inplace=True)
    print(data.head())
    for i in 'abcd':
        data_1=data.loc[i]
        data_11=data_1.loc[0]
        data_12=data_1.loc[1]
        A=data_11.loc[pd.to_datetime('2013-01-01'):pd.to_datetime('2013-04-01'),'Sales'].mean()
        B=data_11.loc[pd.to_datetime('2013-04-01'):pd.to_datetime('2013-07-01'),'Sales'].mean()
        C=data_11.loc[pd.to_datetime('2013-07-01'):pd.to_datetime('2013-10-01'),'Sales'].mean()
        D=data_11.loc[pd.to_datetime('2013-10-01'):pd.to_datetime('2014-01-01'),'Sales'].mean()
        E=data_11.loc[pd.to_datetime('2014-01-01'):pd.to_datetime('2014-04-01'),'Sales'].mean()
        F=data_11.loc[pd.to_datetime('2014-04-01'):pd.to_datetime('2014-07-01'),'Sales'].mean()
        G=data_11.loc[pd.to_datetime('2014-07-01'):pd.to_datetime('2014-10-01'),'Sales'].mean()
        H=data_11.loc[pd.to_datetime('2014-10-01'):pd.to_datetime('2015-01-01'),'Sales'].mean()
        I=data_11.loc[pd.to_datetime('2015-01-01'):pd.to_datetime('2015-04-01'),'Sales'].mean()
        J=data_11.loc[pd.to_datetime('2015-04-01'):pd.to_datetime('2015-08-01'),'Sales'].mean()
        lst_0=[A,B,C,D,E,F,G,H,I,J]
        A=data_12.loc[pd.to_datetime('2013-01-01'):pd.to_datetime('2013-04-01'),'Sales'].mean()
        B=data_12.loc[pd.to_datetime('2013-04-01'):pd.to_datetime('2013-07-01'),'Sales'].mean()
        C=data_12.loc[pd.to_datetime('2013-07-01'):pd.to_datetime('2013-10-01'),'Sales'].mean()
        D=data_12.loc[pd.to_datetime('2013-10-01'):pd.to_datetime('2014-01-01'),'Sales'].mean()
        E=data_12.loc[pd.to_datetime('2014-01-01'):pd.to_datetime('2014-04-01'),'Sales'].mean()
        F=data_12.loc[pd.to_datetime('2014-04-01'):pd.to_datetime('2014-07-01'),'Sales'].mean()
        G=data_12.loc[pd.to_datetime('2014-07-01'):pd.to_datetime('2014-10-01'),'Sales'].mean()
        H=data_12.loc[pd.to_datetime('2014-10-01'):pd.to_datetime('2015-01-01'),'Sales'].mean()
        I=data_12.loc[pd.to_datetime('2015-01-01'):pd.to_datetime('2015-04-01'),'Sales'].mean()
        J=data_12.loc[pd.to_datetime('2015-04-01'):pd.to_datetime('2015-08-01'),'Sales'].mean()
        lst_1=[A,B,C,D,E,F,G,H,I,J]
        x=['2013\nQ1','2013\nQ2','2013\nQ3','2013\nQ4','2014\nQ1','2014\nQ2','2014\nQ3','2014\nQ4','2015\nQ1','2015\nQ2']
        plt.plot(x,lst_0,linestyle='dashed',marker='D',label='Promo = 0')
        plt.plot(x,lst_1,linestyle='dashed',marker='D',label='Promo = 1')
        plt.xlabel('Dates')
        plt.ylabel('Avg. Sales')
        plt.title('Promo-Sales Analysis for StoreType {}'.format(i.upper()))
        plt.legend()
        plt.show()       
Storetype_promos(merged_data)

#%% StoreType Variation of Sales with Holidays
def Storetype_stateholidays_promos(merged_data):
    data=merged_data.copy()
    data.sort_values(['StateHoliday','StoreType','Promo','Date'],inplace=True)
    data.set_index(['StateHoliday','StoreType','Promo','Date','Store'],inplace=True)
    print(data.head())

    data_1=data.loc[1]
    lst=['A','B','C','D']
    lst1=np.arange(len(lst))
    lst2=[]
    for i in 'abcd':
        lst2.append(data_1.loc[i,'Sales'].mean())
    plt.xticks(lst1,lst)
    plt.title('Sales on State Holidays')
    plt.ylabel('Mean Sales')
    plt.xlabel('Store Types')
    plt.bar(lst1,lst2,width=0.5)
    plt.show()    
    data_111=data_1.loc['b']
    data_11=data_111.loc[0]
    data_12=data_111.loc[1]
    A=data_11.loc[pd.to_datetime('2013-01-01'):pd.to_datetime('2013-04-01'),'Sales'].mean()
    B=data_11.loc[pd.to_datetime('2013-04-01'):pd.to_datetime('2013-07-01'),'Sales'].mean()
    C=data_11.loc[pd.to_datetime('2013-07-01'):pd.to_datetime('2013-10-01'),'Sales'].mean()
    D=data_11.loc[pd.to_datetime('2013-10-01'):pd.to_datetime('2014-01-01'),'Sales'].mean()
    E=data_11.loc[pd.to_datetime('2014-01-01'):pd.to_datetime('2014-04-01'),'Sales'].mean()
    F=data_11.loc[pd.to_datetime('2014-04-01'):pd.to_datetime('2014-07-01'),'Sales'].mean()
    G=data_11.loc[pd.to_datetime('2014-07-01'):pd.to_datetime('2014-10-01'),'Sales'].mean()
    H=data_11.loc[pd.to_datetime('2014-10-01'):pd.to_datetime('2015-01-01'),'Sales'].mean()
    I=data_11.loc[pd.to_datetime('2015-01-01'):pd.to_datetime('2015-04-01'),'Sales'].mean()
    J=data_11.loc[pd.to_datetime('2015-04-01'):pd.to_datetime('2015-08-01'),'Sales'].mean()
    lst_0=[A,B,C,D,E,F,G,H,I,J]
    A=data_12.loc[pd.to_datetime('2013-01-01'):pd.to_datetime('2013-04-01'),'Sales'].mean()
    B=data_12.loc[pd.to_datetime('2013-04-01'):pd.to_datetime('2013-07-01'),'Sales'].mean()
    C=data_12.loc[pd.to_datetime('2013-07-01'):pd.to_datetime('2013-10-01'),'Sales'].mean()
    D=data_12.loc[pd.to_datetime('2013-10-01'):pd.to_datetime('2014-01-01'),'Sales'].mean()
    E=data_12.loc[pd.to_datetime('2014-01-01'):pd.to_datetime('2014-04-01'),'Sales'].mean()
    F=data_12.loc[pd.to_datetime('2014-04-01'):pd.to_datetime('2014-07-01'),'Sales'].mean()
    G=data_12.loc[pd.to_datetime('2014-07-01'):pd.to_datetime('2014-10-01'),'Sales'].mean()
    H=data_12.loc[pd.to_datetime('2014-10-01'):pd.to_datetime('2015-01-01'),'Sales'].mean()
    I=data_12.loc[pd.to_datetime('2015-01-01'):pd.to_datetime('2015-04-01'),'Sales'].mean()
    J=data_12.loc[pd.to_datetime('2015-04-01'):pd.to_datetime('2015-08-01'),'Sales'].mean()
    lst_1=[A,B,C,D,E,F,G,H,I,J]
    x=['2013\nQ1','2013\nQ2','2013\nQ3','2013\nQ4','2014\nQ1','2014\nQ2','2014\nQ3','2014\nQ4','2015\nQ1','2015\nQ2']
    plt.plot(x,lst_0,linestyle='dashed',marker='D',label='Promo = 0')
    plt.plot(x,lst_1,linestyle='dashed',marker='D',label='Promo = 1')
    plt.xlabel('Dates')
    plt.ylabel('Avg. Sales')
    plt.title('Promo-Sales Analysis for StoreType B on State Holidays')
    plt.legend()
    plt.show() 
Storetype_stateholidays_promos(merged_data)
    
#%% StoreType Variation of Sales with School Holidays
def Storetype_schoolholidays_promos(merged_data):
    data=merged_data.copy()
    data.sort_values(['SchoolHoliday','StoreType','Promo','Date'],inplace=True)
    data.set_index(['SchoolHoliday','StoreType','Promo','Date','Store'],inplace=True)
    print(data.head())

    data_1=data.loc[1]
    for i in 'abcd':
        data_111=data_1.loc[i]
        data_11=data_111.loc[0]
        data_12=data_111.loc[1]
        A=data_11.loc[pd.to_datetime('2013-01-01'):pd.to_datetime('2013-04-01'),'Sales'].mean()
        B=data_11.loc[pd.to_datetime('2013-04-01'):pd.to_datetime('2013-07-01'),'Sales'].mean()
        C=data_11.loc[pd.to_datetime('2013-07-01'):pd.to_datetime('2013-10-01'),'Sales'].mean()
        D=data_11.loc[pd.to_datetime('2013-10-01'):pd.to_datetime('2014-01-01'),'Sales'].mean()
        E=data_11.loc[pd.to_datetime('2014-01-01'):pd.to_datetime('2014-04-01'),'Sales'].mean()
        F=data_11.loc[pd.to_datetime('2014-04-01'):pd.to_datetime('2014-07-01'),'Sales'].mean()
        G=data_11.loc[pd.to_datetime('2014-07-01'):pd.to_datetime('2014-10-01'),'Sales'].mean()
        H=data_11.loc[pd.to_datetime('2014-10-01'):pd.to_datetime('2015-01-01'),'Sales'].mean()
        I=data_11.loc[pd.to_datetime('2015-01-01'):pd.to_datetime('2015-04-01'),'Sales'].mean()
        J=data_11.loc[pd.to_datetime('2015-04-01'):pd.to_datetime('2015-08-01'),'Sales'].mean()
        lst_0=[A,B,C,D,E,F,G,H,I,J]
        A=data_12.loc[pd.to_datetime('2013-01-01'):pd.to_datetime('2013-04-01'),'Sales'].mean()
        B=data_12.loc[pd.to_datetime('2013-04-01'):pd.to_datetime('2013-07-01'),'Sales'].mean()
        C=data_12.loc[pd.to_datetime('2013-07-01'):pd.to_datetime('2013-10-01'),'Sales'].mean()
        D=data_12.loc[pd.to_datetime('2013-10-01'):pd.to_datetime('2014-01-01'),'Sales'].mean()
        E=data_12.loc[pd.to_datetime('2014-01-01'):pd.to_datetime('2014-04-01'),'Sales'].mean()
        F=data_12.loc[pd.to_datetime('2014-04-01'):pd.to_datetime('2014-07-01'),'Sales'].mean()
        G=data_12.loc[pd.to_datetime('2014-07-01'):pd.to_datetime('2014-10-01'),'Sales'].mean()
        H=data_12.loc[pd.to_datetime('2014-10-01'):pd.to_datetime('2015-01-01'),'Sales'].mean()
        I=data_12.loc[pd.to_datetime('2015-01-01'):pd.to_datetime('2015-04-01'),'Sales'].mean()
        J=data_12.loc[pd.to_datetime('2015-04-01'):pd.to_datetime('2015-08-01'),'Sales'].mean()
        lst_1=[A,B,C,D,E,F,G,H,I,J]
        x=['2013\nQ1','2013\nQ2','2013\nQ3','2013\nQ4','2014\nQ1','2014\nQ2','2014\nQ3','2014\nQ4','2015\nQ1','2015\nQ2']
        plt.plot(x,lst_0,linestyle='dashed',marker='D',label='Promo = 0')
        plt.plot(x,lst_1,linestyle='dashed',marker='D',label='Promo = 1')
        plt.xlabel('Dates')
        plt.ylabel('Avg. Sales')
        plt.title('Promo-Sales Analysis for StoreType {} on School Holidays'.format(i.upper()))
        plt.legend()
        plt.show() 
Storetype_schoolholidays_promos(merged_data)

#%% Number of stores in each Assortment type
def assortment_type_distribution(merged_data):
    data=store.copy()
    data.sort_values(['Assortment'],inplace=True)
    data.set_index(['Assortment'],inplace=True)
    print(data.head())
    lst=[]
    lst_1=['a','b','c']
    sm=0
    for i in lst_1:
        sm+=len(data.loc[i])
        lst.append(len(data.loc[i]))
    plt.pie(lst,labels=lst_1,colors=['r','g','b'],shadow=True,autopct = '%1.1f%%')
    plt.title('Stores Distribution According to Assortment Type')
    plt.show()
assortment_type_distribution(merged_data)

#%% AssortmentType Variation of Sales with Promos
def Assortmenttype_promos(merged_data):
    data=merged_data.copy()
    data.sort_values(['Assortment','Promo','Date'],inplace=True)
    data.set_index(['Assortment','Promo','Date','Store'],inplace=True)
    print(data.head())
    for i in 'abc':
        data_1=data.loc[i]
        data_11=data_1.loc[0]
        data_12=data_1.loc[1]
        A=data_11.loc[pd.to_datetime('2013-01-01'):pd.to_datetime('2013-04-01'),'Sales'].mean()
        B=data_11.loc[pd.to_datetime('2013-04-01'):pd.to_datetime('2013-07-01'),'Sales'].mean()
        C=data_11.loc[pd.to_datetime('2013-07-01'):pd.to_datetime('2013-10-01'),'Sales'].mean()
        D=data_11.loc[pd.to_datetime('2013-10-01'):pd.to_datetime('2014-01-01'),'Sales'].mean()
        E=data_11.loc[pd.to_datetime('2014-01-01'):pd.to_datetime('2014-04-01'),'Sales'].mean()
        F=data_11.loc[pd.to_datetime('2014-04-01'):pd.to_datetime('2014-07-01'),'Sales'].mean()
        G=data_11.loc[pd.to_datetime('2014-07-01'):pd.to_datetime('2014-10-01'),'Sales'].mean()
        H=data_11.loc[pd.to_datetime('2014-10-01'):pd.to_datetime('2015-01-01'),'Sales'].mean()
        I=data_11.loc[pd.to_datetime('2015-01-01'):pd.to_datetime('2015-04-01'),'Sales'].mean()
        J=data_11.loc[pd.to_datetime('2015-04-01'):pd.to_datetime('2015-08-01'),'Sales'].mean()
        lst_0=[A,B,C,D,E,F,G,H,I,J]
        A=data_12.loc[pd.to_datetime('2013-01-01'):pd.to_datetime('2013-04-01'),'Sales'].mean()
        B=data_12.loc[pd.to_datetime('2013-04-01'):pd.to_datetime('2013-07-01'),'Sales'].mean()
        C=data_12.loc[pd.to_datetime('2013-07-01'):pd.to_datetime('2013-10-01'),'Sales'].mean()
        D=data_12.loc[pd.to_datetime('2013-10-01'):pd.to_datetime('2014-01-01'),'Sales'].mean()
        E=data_12.loc[pd.to_datetime('2014-01-01'):pd.to_datetime('2014-04-01'),'Sales'].mean()
        F=data_12.loc[pd.to_datetime('2014-04-01'):pd.to_datetime('2014-07-01'),'Sales'].mean()
        G=data_12.loc[pd.to_datetime('2014-07-01'):pd.to_datetime('2014-10-01'),'Sales'].mean()
        H=data_12.loc[pd.to_datetime('2014-10-01'):pd.to_datetime('2015-01-01'),'Sales'].mean()
        I=data_12.loc[pd.to_datetime('2015-01-01'):pd.to_datetime('2015-04-01'),'Sales'].mean()
        J=data_12.loc[pd.to_datetime('2015-04-01'):pd.to_datetime('2015-08-01'),'Sales'].mean()
        lst_1=[A,B,C,D,E,F,G,H,I,J]
        x=['2013\nQ1','2013\nQ2','2013\nQ3','2013\nQ4','2014\nQ1','2014\nQ2','2014\nQ3','2014\nQ4','2015\nQ1','2015\nQ2']
        plt.plot(x,lst_0,linestyle='dashed',marker='D',label='Promo = 0')
        plt.plot(x,lst_1,linestyle='dashed',marker='D',label='Promo = 1')
        plt.xlabel('Dates')
        plt.ylabel('Avg. Sales')
        plt.title('Promo-Sales Analysis for AssortmentType {}'.format(i.upper()))
        plt.legend()
        plt.show()       
Assortmenttype_promos(merged_data)
#%% StoreType Variation of Sales with Holidays
def Assortmenttype_stateholidays_promos(merged_data):
    data=merged_data.copy()
    data.sort_values(['StateHoliday','Assortment','Promo','Date'],inplace=True)
    data.set_index(['StateHoliday','Assortment','Promo','Date','Store'],inplace=True)
    print(data.head())

    data_1=data.loc[1]
    lst=['A','B','C']
    lst1=np.arange(len(lst))
    lst2=[]
    for i in 'abc':
        lst2.append(data_1.loc[i,'Sales'].mean())
    plt.xticks(lst1,lst)
    plt.title('Sales on State Holidays')
    plt.ylabel('Mean Sales')
    plt.xlabel('Store Types')
    plt.bar(lst1,lst2,width=0.5)
    plt.show()    
    data_111=data_1.loc['b']
    data_11=data_111.loc[0]
    data_12=data_111.loc[1]
    A=data_11.loc[pd.to_datetime('2013-01-01'):pd.to_datetime('2013-04-01'),'Sales'].mean()
    B=data_11.loc[pd.to_datetime('2013-04-01'):pd.to_datetime('2013-07-01'),'Sales'].mean()
    C=data_11.loc[pd.to_datetime('2013-07-01'):pd.to_datetime('2013-10-01'),'Sales'].mean()
    D=data_11.loc[pd.to_datetime('2013-10-01'):pd.to_datetime('2014-01-01'),'Sales'].mean()
    E=data_11.loc[pd.to_datetime('2014-01-01'):pd.to_datetime('2014-04-01'),'Sales'].mean()
    F=data_11.loc[pd.to_datetime('2014-04-01'):pd.to_datetime('2014-07-01'),'Sales'].mean()
    G=data_11.loc[pd.to_datetime('2014-07-01'):pd.to_datetime('2014-10-01'),'Sales'].mean()
    H=data_11.loc[pd.to_datetime('2014-10-01'):pd.to_datetime('2015-01-01'),'Sales'].mean()
    I=data_11.loc[pd.to_datetime('2015-01-01'):pd.to_datetime('2015-04-01'),'Sales'].mean()
    J=data_11.loc[pd.to_datetime('2015-04-01'):pd.to_datetime('2015-08-01'),'Sales'].mean()
    lst_0=[A,B,C,D,E,F,G,H,I,J]
    A=data_12.loc[pd.to_datetime('2013-01-01'):pd.to_datetime('2013-04-01'),'Sales'].mean()
    B=data_12.loc[pd.to_datetime('2013-04-01'):pd.to_datetime('2013-07-01'),'Sales'].mean()
    C=data_12.loc[pd.to_datetime('2013-07-01'):pd.to_datetime('2013-10-01'),'Sales'].mean()
    D=data_12.loc[pd.to_datetime('2013-10-01'):pd.to_datetime('2014-01-01'),'Sales'].mean()
    E=data_12.loc[pd.to_datetime('2014-01-01'):pd.to_datetime('2014-04-01'),'Sales'].mean()
    F=data_12.loc[pd.to_datetime('2014-04-01'):pd.to_datetime('2014-07-01'),'Sales'].mean()
    G=data_12.loc[pd.to_datetime('2014-07-01'):pd.to_datetime('2014-10-01'),'Sales'].mean()
    H=data_12.loc[pd.to_datetime('2014-10-01'):pd.to_datetime('2015-01-01'),'Sales'].mean()
    I=data_12.loc[pd.to_datetime('2015-01-01'):pd.to_datetime('2015-04-01'),'Sales'].mean()
    J=data_12.loc[pd.to_datetime('2015-04-01'):pd.to_datetime('2015-08-01'),'Sales'].mean()
    lst_1=[A,B,C,D,E,F,G,H,I,J]
    x=['2013\nQ1','2013\nQ2','2013\nQ3','2013\nQ4','2014\nQ1','2014\nQ2','2014\nQ3','2014\nQ4','2015\nQ1','2015\nQ2']
    plt.plot(x,lst_0,linestyle='dashed',marker='D',label='Promo = 0')
    plt.plot(x,lst_1,linestyle='dashed',marker='D',label='Promo = 1')
    plt.xlabel('Dates')
    plt.ylabel('Avg. Sales')
    plt.title('Promo-Sales Analysis for AssortmentType B on State Holidays')
    plt.legend()
    plt.show()
Assortmenttype_stateholidays_promos(merged_data)
    
#%% StoreType Variation of Sales with School Holidays
def Assortmenttype_schoolholidays_promos(merged_data):
    data=merged_data.copy()
    data.sort_values(['SchoolHoliday','Assortment','Promo','Date'],inplace=True)
    data.set_index(['SchoolHoliday','Assortment','Promo','Date','Store'],inplace=True)
    print(data.head())

    data_1=data.loc[1]
    for i in 'abc':
        data_111=data_1.loc[i]
        data_11=data_111.loc[0]
        data_12=data_111.loc[1]
        A=data_11.loc[pd.to_datetime('2013-01-01'):pd.to_datetime('2013-04-01'),'Sales'].mean()
        B=data_11.loc[pd.to_datetime('2013-04-01'):pd.to_datetime('2013-07-01'),'Sales'].mean()
        C=data_11.loc[pd.to_datetime('2013-07-01'):pd.to_datetime('2013-10-01'),'Sales'].mean()
        D=data_11.loc[pd.to_datetime('2013-10-01'):pd.to_datetime('2014-01-01'),'Sales'].mean()
        E=data_11.loc[pd.to_datetime('2014-01-01'):pd.to_datetime('2014-04-01'),'Sales'].mean()
        F=data_11.loc[pd.to_datetime('2014-04-01'):pd.to_datetime('2014-07-01'),'Sales'].mean()
        G=data_11.loc[pd.to_datetime('2014-07-01'):pd.to_datetime('2014-10-01'),'Sales'].mean()
        H=data_11.loc[pd.to_datetime('2014-10-01'):pd.to_datetime('2015-01-01'),'Sales'].mean()
        I=data_11.loc[pd.to_datetime('2015-01-01'):pd.to_datetime('2015-04-01'),'Sales'].mean()
        J=data_11.loc[pd.to_datetime('2015-04-01'):pd.to_datetime('2015-08-01'),'Sales'].mean()
        lst_0=[A,B,C,D,E,F,G,H,I,J]
        A=data_12.loc[pd.to_datetime('2013-01-01'):pd.to_datetime('2013-04-01'),'Sales'].mean()
        B=data_12.loc[pd.to_datetime('2013-04-01'):pd.to_datetime('2013-07-01'),'Sales'].mean()
        C=data_12.loc[pd.to_datetime('2013-07-01'):pd.to_datetime('2013-10-01'),'Sales'].mean()
        D=data_12.loc[pd.to_datetime('2013-10-01'):pd.to_datetime('2014-01-01'),'Sales'].mean()
        E=data_12.loc[pd.to_datetime('2014-01-01'):pd.to_datetime('2014-04-01'),'Sales'].mean()
        F=data_12.loc[pd.to_datetime('2014-04-01'):pd.to_datetime('2014-07-01'),'Sales'].mean()
        G=data_12.loc[pd.to_datetime('2014-07-01'):pd.to_datetime('2014-10-01'),'Sales'].mean()
        H=data_12.loc[pd.to_datetime('2014-10-01'):pd.to_datetime('2015-01-01'),'Sales'].mean()
        I=data_12.loc[pd.to_datetime('2015-01-01'):pd.to_datetime('2015-04-01'),'Sales'].mean()
        J=data_12.loc[pd.to_datetime('2015-04-01'):pd.to_datetime('2015-08-01'),'Sales'].mean()
        lst_1=[A,B,C,D,E,F,G,H,I,J]
        x=['2013\nQ1','2013\nQ2','2013\nQ3','2013\nQ4','2014\nQ1','2014\nQ2','2014\nQ3','2014\nQ4','2015\nQ1','2015\nQ2']
        plt.plot(x,lst_0,linestyle='dashed',marker='D',label='Promo = 0')
        plt.plot(x,lst_1,linestyle='dashed',marker='D',label='Promo = 1')
        plt.xlabel('Dates')
        plt.ylabel('Avg. Sales')
        plt.title('Promo-Sales Analysis for AssortmentType {} on School Holidays'.format(i.upper()))
        plt.legend()
        plt.show() 
Assortmenttype_schoolholidays_promos(merged_data)

#%% The End
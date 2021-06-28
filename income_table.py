import pandas as pd
import numpy as np
from datetime import datetime
import numpy_financial as npf
import datetime
from collections import OrderedDict
from dateutil.relativedelta import *

def BSV_indicator_payment(x):
    if x <= 10 :
        BVS_payment_indicator = 1
    else :
        BVS_payment_indicator = 0
    return BVS_payment_indicator

def income_table(start_date, income_p1, income_p2, income_increase_rate ,bonus = 0, bonus_month = '12', no_kids = 1, kindergeld_rate = 219, base_living_expenses = 2700, 
                living_cost_inflation= 1.02,no_projection_years = 22, BSV_ind = 1, BSV_extra = 300):
    rng = pd.date_range(datetime.datetime.strptime(str(start_date), '%Y-%m-%d').date(), periods=no_projection_years*12, freq='MS')
    rng.name = "Payment_Date"

    df = pd.DataFrame(index = rng , columns=['income_p2','income_p1','bonus', 'Kindergeld'
                                         ,'tot_Income', 'living_exp'], dtype='float')

    start_year = start_date.year

    for i in df.index:
       # if i < datetime.datetime(2022, 7, 1):
        df.loc[df.index == i,'income_p2'] = income_p2*pow(income_increase_rate, i.year -start_year) 
        df.loc[df.index == i,'income_p1'] = income_p1*pow(income_increase_rate, i.year -start_year) 
        df.loc[df.index == i,'Kindergeld'] = no_kids * kindergeld_rate
        df.loc[df.index == i,'living_exp'] =  (base_living_expenses )*pow(living_cost_inflation, i.year -start_year) +  BSV_extra*BSV_ind*BSV_indicator_payment(i.year -start_year)
 
    for i in df.index:
        if i.strftime("%m") == bonus_month:
            df.loc[df.index == i,'bonus'] = bonus
        else :
            df.loc[df.index == i,'bonus'] = 0
      
    df['tot_Income'] =  df['income_p2'] + df['income_p1'] + df['bonus'] +  df['Kindergeld']
     #= datetime.datetime.strptime(str(start_date), '%Y-%m-%d').date()
    df['cum_net_income'] = (df['tot_Income'] -  df['living_exp']).cumsum()
    df['BSV_ind'] = BSV_ind
    df['BSV_extra'] = BSV_extra
    df.reset_index(inplace = True) 
    df['Payment_Date'] = df['Payment_Date'].dt.date
    df= round(df, 2)
       
    return df

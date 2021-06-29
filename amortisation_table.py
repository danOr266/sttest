import pandas as pd
import numpy as np
from datetime import datetime
import numpy_financial as npf
import datetime
from collections import OrderedDict
from dateutil.relativedelta import *

# Main Amortisation Table Function
def amort_t(interest_rate, years, payments_year, principal,
            kfw_ford =0, m_sond_tilg = 0,y_sond_tilg=0, 
            sond_t_start = 0, start_date='2021-07-01', BSV_ind = 0, Scenario = 'B'):
    
    t = 1
    principal = max(principal,0)
    start_date = datetime.datetime.strptime(str(start_date), '%Y-%m-%d').date()
    Begin_Balance = principal
    Curr_Balance = principal
    per_payment = -round(npf.pmt(interest_rate/payments_year, years*payments_year, principal, when = 'end' ),2)
    Cum_Interest = 0.0
    sonder = np.array([0]*int(years * payments_year*2))
    sonder[0] = kfw_ford
    
    if m_sond_tilg + y_sond_tilg != 0:
        for j in range(1,int(years * payments_year*2)):
            if j >= sond_t_start :
                if (start_date + relativedelta(months=j-1)).month == 1 :
                    sonder[j-1] = (sonder[j-1] + m_sond_tilg + y_sond_tilg)*pow(1.00,j)
                else:
                    sonder[j-1] = (sonder[j-1]+ m_sond_tilg )*pow(1.00,j)
            else :
                sonder[j] = sonder[j-1]+ 0.0
    
    while Curr_Balance >0:
        interest = (interest_rate/payments_year)*Begin_Balance
        per_payment = min(per_payment, Begin_Balance + interest)  
        sonder_tilg = min(Begin_Balance + interest - per_payment, sonder[t-1])
        Tot_Payment = sonder_tilg + per_payment
        Curr_Balance = Begin_Balance + interest - Tot_Payment
        principal_payment = Tot_Payment - interest
    
        yield OrderedDict([('Payment_Date',start_date),
                         #  ('Period', t),
                           ('Begin_Balance', Begin_Balance),
                           ('Sched_Payment', per_payment),
                           ('Add_Payment', sonder_tilg),
                           ('Tot_Payment', Tot_Payment),
                           ('Prin_Payment', principal_payment),
                           ('Interest', interest),                  
                           ('Scenario', Scenario),
                           ('Curr_Balance', Curr_Balance),
                           ('BSV_ind', BSV_ind)])
        t += 1  
        start_date += relativedelta(months=1)
        Begin_Balance = Curr_Balance
    if principal == 0:
        yield OrderedDict([('Payment_Date',start_date),
                          # ('Period', t),
                           ('Begin_Balance', Begin_Balance),
                           ('Sched_Payment', 0),
                           ('Add_Payment', 0),
                           ('Tot_Payment', 0),
                           ('Prin_Payment', 0),
                           ('Interest', 0),
                           ('Scenario', Scenario),
                           ('Curr_Balance', 0),
                           ('BSV_ind', BSV_ind)])

def framer(interest_rate, years, payments_year, principal,
            kfw_ford =0, m_sond_tilg = 0,y_sond_tilg=0,
            sond_t_start = 0, start_date= '2021-07-01', BSV_ind = 0, Scenario = 'B'):
    df = pd.DataFrame(amort_t(interest_rate, years, payments_year, principal, 
                       kfw_ford, m_sond_tilg, y_sond_tilg, 
                       sond_t_start, start_date,BSV_ind , Scenario ))
    df["Cum_Principle"] = df.Prin_Payment.cumsum()
    df["Cum_Interest"] = df.Interest.cumsum()
    df['Cum_tot_Payment'] = df.Tot_Payment.cumsum()
    df.index += 1
    df.index.name = "Period"
    df = df.round(2)
    return df

# Combines amoration tables and reculculates atrributes:

def combiner(  *argv, Scenario = 'B'):
    df = pd.DataFrame()
    for i in argv:
        df = pd.concat([df, i])
        df['Scenario'] = Scenario
        df = df.groupby(['Payment_Date', 'Scenario', 'BSV_ind']).sum()      
        df['Cum_Interest'] = df.Interest.cumsum()
        df['Cum_Principle'] = df.Prin_Payment.cumsum()
        df['Cum_tot_Payment'] = df.Tot_Payment.cumsum()      
        df.reset_index(inplace=True)
        df.index += 1
        df.index.name = "Period"
        return df

# Determines the Remaining Balance, next payment date after Zinsbindung

def anschluss (df, year):
    months = int(year*12)
    months = min(df[df.BSV_ind == 0].shape[0], months)
    df_0 = df[df.BSV_ind == 0][0:months].sort_values(by = 'Payment_Date')
    df_1 = df[df.BSV_ind == 1][0:months].sort_values(by = 'Payment_Date')
    base = pd.concat([df_0, df_1])
    rest_schuld = max(df_0.loc[months, "Curr_Balance"],0)

    if rest_schuld == 0:
        next_payment_DT = df[df.BSV_ind == 0].loc[months, "Payment_Date"]
    else :
        next_payment_DT = df[df.BSV_ind == 0].loc[months+1, "Payment_Date"]
    
    return base, rest_schuld, next_payment_DT
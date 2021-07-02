import pandas as pd


def base_scenarios(start_date, loan_amount, interest_rate, BSV_amount, BSV_loan_amount, BSV_ind, ZB_to_compare):
    df = pd.DataFrame(data ={'start_date' : [start_date],
                            'loan_amount' : [loan_amount],
                            'BSV_amount' : [BSV_amount],
                            'BSV_loan_amount' : [BSV_loan_amount],
                            'BSV_ind' : [BSV_ind]  } )
    
    ZB_scenarios =  pd.DataFrame(data ={'ZB': ZB_to_compare,
                                        'interest_rate': interest_rate} )

    if BSV_ind == 1:
        df1 = df.copy()
        df1['BSV_amount'] = 0
        df1['BSV_ind'] = 0
        df1['BSV_loan_amount'] = 0
        df =  pd.concat([df, df1])
    
    df['key'] = 0
    ZB_scenarios['key'] = 0
    df =pd.merge(df, ZB_scenarios, on ='key').drop("key", 1)

    return df

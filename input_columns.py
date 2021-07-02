
import pandas as pd
import numpy as np
import streamlit as st
from datetime import *

#@st.cache
def input_columns(start_date,loan_amount , ZB_to_compare, BSV_to_compare, BSV_ind, BSV_amount, BSV_loan_amount):
    scenario_df = pd.DataFrame(columns=['ZB','loan_amount','interest_rate','years','payments_year', 'start_date', 'BSV_ind', 'BSV_amount', 'BSV_loan_amount'],
                                dtype='float')
    col1, col2, col3  = st.beta_columns(3)
    with col1 :
        ZB = ZB_to_compare[0]
        with st.form(key=f'my_form{ZB}'):
            st.write(f'For the {ZB} Zinsbindung, enter the following loan details')
            interest_rate = st.number_input(label='Enter the interest_rate on the loan')
            years = st.number_input(label='Enter the loan repayment length in years')
            payments_year = st.number_input(label='Enter the number of payments in a year')
            #start_date = st.date_input(label = 'Selection income start projection date', value =None, min_value = date.today(), )
            st.form_submit_button(label=f'Submit_{ZB}',)
            if BSV_to_compare == 0:
                temp_df = pd.DataFrame( [ZB, loan_amount, interest_rate, years, payments_year, start_date, 0, 0, 0 ]).T
                temp_df.columns = scenario_df.columns
            else :
                temp_df1 = pd.DataFrame( [ZB, loan_amount, interest_rate, years, payments_year, start_date, 0, 0, 0 ]).T
                temp_df2 = pd.DataFrame( [ZB, loan_amount, interest_rate, years, payments_year, start_date, BSV_ind, BSV_amount, BSV_loan_amount ]).T
                temp_df = pd.concat([temp_df1,temp_df2])
            temp_df.columns = scenario_df.columns
            scenario_df = pd.concat([temp_df,scenario_df])
        scenario_df.reset_index(inplace = True, drop=True)
    if len(ZB_to_compare) <= 3 and len(ZB_to_compare) > 1:
        with col2 :
            ZB = ZB_to_compare[1]
            with st.form(key=f'my_form{ZB}'):
                st.write(f'For the {ZB} Zinsbindung, enter the following loan details')
                interest_rate = st.number_input(label='Enter the interest_rate on the loan')
                years = st.number_input(label='Enter the loan repayment length in years')
                payments_year = st.number_input(label='Enter the number of payments in a year')
                #start_date = st.date_input(label = 'Selection income start projection date', value =None, min_value = date.today(), )
                st.form_submit_button(label=f'Submit_{ZB}',)
                if BSV_to_compare == 0:
                    temp_df = pd.DataFrame( [ZB, loan_amount, interest_rate, years, payments_year, start_date, 0, 0, 0 ]).T
                    temp_df.columns = scenario_df.columns
                else :
                    temp_df1 = pd.DataFrame( [ZB, loan_amount, interest_rate, years, payments_year, start_date, 0, 0, 0 ]).T
                    temp_df2 = pd.DataFrame( [ZB, loan_amount, interest_rate, years, payments_year, start_date, BSV_ind, BSV_amount, BSV_loan_amount ]).T
                    temp_df = pd.concat([temp_df1,temp_df2])
                temp_df.columns = scenario_df.columns
                scenario_df = pd.concat([temp_df,scenario_df])
            scenario_df.reset_index(inplace = True, drop=True)
    if  len(ZB_to_compare) == 3:
        with col3 :
            ZB = ZB_to_compare[2]
            with st.form(key=f'my_form{ZB}'):
                st.write(f'For the {ZB} Zinsbindung, enter the following loan details')
                interest_rate = st.number_input(label='Enter the interest_rate on the loan')
                years = st.number_input(label='Enter the loan repayment length in years')
                payments_year = st.number_input(label='Enter the number of payments in a year')
                #start_date = st.date_input(label = 'Selection income start projection date', value =None, min_value = date.today(), )
                st.form_submit_button(label=f'Submit_{ZB}',)
                if BSV_to_compare == 0:
                    temp_df = pd.DataFrame( [ZB, loan_amount, interest_rate, years, payments_year, start_date, 0, 0, 0 ]).T
                    temp_df.columns = scenario_df.columns
                else :
                    temp_df1 = pd.DataFrame( [ZB, loan_amount, interest_rate, years, payments_year, start_date, 0, 0, 0 ]).T
                    temp_df2 = pd.DataFrame( [ZB, loan_amount, interest_rate, years, payments_year, start_date, BSV_ind, BSV_amount, BSV_loan_amount ]).T
                    temp_df = pd.concat([temp_df1,temp_df2])
                temp_df.columns = scenario_df.columns
                scenario_df = pd.concat([temp_df,scenario_df])
            scenario_df.reset_index(inplace = True, drop=True)

    return scenario_df

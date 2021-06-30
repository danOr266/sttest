import streamlit as st
import numpy as np

months = list(map(str, range(1, 13)))
for i in range(0,len(months)):
    months[i]= '0'+months[i]
    months[i] = months[i][-2:]


def income_input() :
    with st.form(label ='Income Input Form', key = 'income_input_form') :
        No_of_incomes = st.radio(label = 'Number of People taking the loan', options = [1,2], index=1, key='No_of_incomes_key')
        person1, person2 = st.beta_columns(2)
        with st.form(label = 'Income Person 1', key = 'income_p1_key'):
            income_p1 = st.number_input( 'Enter Income of Person 1')
            bonus_p1 = st.number_input( 'Enter Income of Person 1')
            bonus_month_p1 = st.selectbox( 'Month bonus expected for Person 1', months )
            income_p1_increase =  st.number_input( 'Enter Income increase of Person 1')
            living_expense =  st.number_input( 'Enter total living expenses exclusing mortgage')
            living_expense_inflation =  st.number_input( 'Enter total living expenses excluding mortgage inflation')
            st.form_submit_button(label='Submit_income_input_P1')
        
        if No_of_incomes == 2:
            with st.form(label = 'Income Person 1', key = 'income_p1_key'):
                income_p2 = st.number_input( 'Enter Income of Person 1')
                bonus_p2 = st.number_input( 'Enter Income of Person 1')
                bonus_month_p2 = st.selectbox( 'Month bonus expected for Person 2', months )
                income_p2_increase =  st.number_input( 'Enter Income increase of Person 1')
                st.form_submit_button(label='Submit_income_input_P2')
        

        st.form_submit_button(label='Submit_income_input')

        income_input_dict = {'income_p1':income_p1,
                            'bonus_p1' : bonus_p1,
                            'bonus_month_p1' : bonus_month_p1 ,
                            'income_p1_increase': income_p1_increase,
                            'living_expense' : living_expense,
                            'living_expense_inflation' : living_expense_inflation,
                            'income_p2':income_p2,
                            'bonus_p2' : bonus_p2,
                            'bonus_month_p2' : bonus_month_p2 ,
                            'income_p2_increase': income_p2_increase
                            }
        return
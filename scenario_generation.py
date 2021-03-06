import pandas as pd
import numpy as np
from datetime import datetime
import numpy_financial as npf
import datetime
from collections import OrderedDict
from dateutil.relativedelta import *
import amortisation_table as at
import streamlit as st

import amortisation_table

@st.cache
def scenario_generation(scenario_table, scenario_vector):
    scenario_table = pd.DataFrame(scenario_table)
    scenario_vector = np.array(scenario_vector)
    All_Scenarios = pd.DataFrame()
    for i in range(0, scenario_table.shape[0]):
        principal = scenario_table['loan_amount'][i]
        years = scenario_table['years'][i]
        payments_year = scenario_table['payments_year'][i]
        start_date = scenario_table['start_date'][i]
        interest_rate = scenario_table['interest_rate'][i]
        ZB = scenario_table['ZB'][i]
        BSV_ind =  scenario_table['BSV_ind'][i]
        BSV_amount =  scenario_table['BSV_amount'][i]
        BSV_loan_amount =  scenario_table['BSV_loan_amount'][i]

        df_start = amortisation_table.framer(interest_rate = interest_rate,
                    years = years,
                    payments_year = payments_year,
                    principal = principal, 
                    kfw_ford = 0,
                    y_sond_tilg=0,
                    sond_t_start = 40,
                    BSV_ind = BSV_ind)
        base, rest_schuld_base, next_DT_base = amortisation_table.anschluss(df_start, ZB)

# still need to insert KfW table
        df_BSV = amortisation_table.framer(interest_rate = 1.01,  # change to BSV rate
                    years = 6.5,    # change to BSV rate
                    payments_year = payments_year,
                    principal = BSV_loan_amount * BSV_ind,                   
                    BSV_ind = BSV_ind )
        
        for s in range(0, len(scenario_vector)):
            df_post_ZB =  amortisation_table.framer(interest_rate = scenario_vector[s],
                        years = 23- ZB,
                        payments_year = payments_year,
                        principal = rest_schuld_base, 
                        kfw_ford = 0,
                        y_sond_tilg=0,
                        BSV_ind = BSV_ind )
            scenario_interest = str(scenario_vector[s]*100) + '%'
            df_scenario= amortisation_table.combiner(df_start, df_BSV, df_post_ZB, Scenario= scenario_interest )
            All_Scenarios = pd.concat([df_scenario, All_Scenarios])
        All_Scenarios.drop_duplicates()

    return All_Scenarios

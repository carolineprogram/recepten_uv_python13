from pages.test_supabase import run_query
import streamlit as st
import pandas as pd


recepten =  [row[1] for row in run_query("select", "recepten_Recepten", "*")]

df = pd.DataFrame.from_dict(recepten[0])

# Group the DataFrame by 'Locatie'
grouped_df = df.groupby('Bron')

filtered_Bron = grouped_df.filter(lambda x: 'Moestuin' in x.name)

st.dataframe(filtered_Bron)
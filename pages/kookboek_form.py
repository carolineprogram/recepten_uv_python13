#This file contains the form to select by ingredient.
import pandas as pd
import streamlit as st

from utils import get_all_receptbron, get_recipes_w_bron_id

from loguru import logger


def select_receptbron_form():
    bron = get_all_receptbron()
    bron_data = bron.data

    bron_data_name = [row["bron"] for row in bron_data]
    bron_data_id = [row["bron_id"] for row in bron_data]

    with st.form(key="Select Receptbron", clear_on_submit=True):
        selected_bron = st.selectbox("Welk kookboek?", bron_data_name)
        submitted = st.form_submit_button("Submit")

    if submitted:
        bron_i_array = [i for i, j in enumerate(bron_data_name) if j == selected_bron]
        bron_id = bron_data_id[bron_i_array[0]]
        recipes = get_recipes_w_bron_id(bron_id)

        recepten = []
        for i in recipes.data:
            recepten.append(i)
        df = pd.DataFrame(recepten)
        if df.empty is False:
            df['Naam'] = df.apply(lambda row: f"[{row['Naam']}](info_recipe_form?recept_id={row['recept_id']})", axis=1)
            st.markdown(df.sort_values("Naam").to_markdown(index=False), unsafe_allow_html=True)

        else:
            st.write("Geen recepten gevonden voor dit type.")

if __name__ == "__main__":
    select_receptbron_form()

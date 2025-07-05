#This file contains the form to select by type.

import streamlit as st

import utils
from utils import get_all_types, get_recipe_id_w_type_id, get_recipe_w_recipe_id
from db import run_query


def select_type():
    types = get_all_types()
    types_data = types.data

    types_data_name = [row["type"] for row in types_data]
    types_data_id = [row["type_id"] for row in types_data]

    with st.form(key="Select Type", clear_on_submit=True):
        selected_type = st.selectbox("Welk type?", types_data_name)
        submitted = st.form_submit_button("Submit")

    if submitted:
        type_i_array = [i for i, j in enumerate(types_data_name) if j == selected_type]
        type_id = types_data_id[type_i_array[0]]
        recipe_ids = get_recipe_id_w_type_id(type_id)

        for i in recipe_ids.data:
            recipe_id = i["recept_id"]
            recipe_details = get_recipe_w_recipe_id(recipe_id)
            st.write(recipe_details.data)
if __name__ == "__main__":
    select_type()

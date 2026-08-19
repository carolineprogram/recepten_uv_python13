"""
Hier kan je terecht komen
- rechtstreeks -> dan moet je nog een recept kiezen in een keuzelijst
- via recipe_info_page(recipe_request)
- via query_params -> dat is de variabele in de link na het vraagteken
"""
#This file contains the form to select recipes.
import streamlit as st
import pandas as pd
from utils import get_recipe_w_recipe_id, get_ingredients, get_types_w_recipe_id
from form_snippets import select_recipe
from loguru import logger

# dit is om variabelen in de link na het vraagteken te kunnen gebruiken
query_params = st.query_params
recept_id = query_params.get("recept_id")

if "clicked"not in st.session_state:
    st.session_state["clicked"] = False

def click_button():
    st.session_state["clicked"] = True

def recipe_info_form(recept_id):
    recipe_data = get_recipe_w_recipe_id(recept_id)
    recipe_id = recept_id

    df = pd.DataFrame(recipe_data.data)
    st.title(df["Naam"].iloc[0]) #df["Naam"] is een serie, als je enkel df["Naam"] vraagt dan krijg je index en dtype erbij
    st.markdown(df.to_markdown(index=False), unsafe_allow_html=True)

    ingredients = get_ingredients(recipe_id, return_modus = "full")
    st.markdown('<h3><strong>Ingrediënten</strong></h3>', unsafe_allow_html=True)

    if len(ingredients) > 0:
        for i in ingredients:
            st.write(i['ingredient'])
    else:
        st.write("Geen ingredienten gevonden")


    st.markdown('<h3><strong>Type</strong></h3>', unsafe_allow_html=True)
    types = get_types_w_recipe_id(recipe_id)
    for j in types:
        st.markdown(f"{j}")

def recipe_info_page(recipe_request=None):
    if recipe_request:
        selected_recipe_id = recipe_request
    elif "recept_id" in query_params:
        selected_recipe_id = query_params.get("recept_id")
    else:
        selected_recipe_id = select_recipe(form_key="Select Recipe Info", button_label="Info")

    if selected_recipe_id:
        recipe_info_form(selected_recipe_id)
        st.session_state["recipe"] = selected_recipe_id
        st.button(label="Update recept", on_click=click_button)

    if st.session_state["clicked"]:
        st.write("session state is True")
        st.switch_page("pages/update_recipe_form.py")
if __name__ == "__main__":
    st.title("Kies op naam")
    recipe_info_page(None)

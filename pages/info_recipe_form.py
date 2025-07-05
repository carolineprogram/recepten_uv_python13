#This file contains the form to select recipes.
import pandas as pd
import streamlit as st
from utils import get_recipe_w_recipe_id, get_ingredients, get_types_w_recipe_id
from form_snippets import select_recipe


if "clicked"not in st.session_state:
    st.session_state["clicked"] = False

def click_button():
    st.session_state["clicked"] = True

def recipe_info_form(recept_id):
    recipe_data = get_recipe_w_recipe_id(recept_id)
    recipe_id = recept_id
    naam = recipe_data.data[0]["Naam"]
    beschrijving = recipe_data.data[0]["Beschrijving"]
    bron = recipe_data.data[0]["Bron"]
    gemaakt = str(recipe_data.data[0]["Gemaakt"])
    locatie = recipe_data.data[0]["Locatie"]
    st.title(naam + "(" + str(recept_id) + ")")
    st.markdown("Beschrijving: " + beschrijving)
    st.markdown("Bron: " + bron)
    st.markdown("Gemaakt: " + gemaakt)
    st.markdown("Locatie: " + locatie)
    ingredients = get_ingredients(recipe_id)
    st.markdown('<h3><strong>Ingrediënten</strong></h3>', unsafe_allow_html=True)

    if len(ingredients) > 0:
        for i in ingredients:
            ingredient_data = {'ingredient': i["ingredient"], 'hele jaar': i["hele_jaar"], 'januari': i["jan"], 'februari': i["feb"], 'maart': i["maa"], 'april': i["apr"], 'mei': i["mei"], 'juni': i["jun"], 'juli': i[
        "jul"], 'augustus': i["aug"], 'september': i["sep"], 'oktober': i["okt"], 'november': i["nov"], 'december': i["dec"]}

            df = pd.DataFrame([ingredient_data])

            # Define a styling function
            def highlight_green(val):
                if val == 1:
                    return 'background-color: green'
                return ''

            # Apply the styling, exclude the ingredient column
            styled_df = df.style.applymap(highlight_green, subset=df.columns.difference(['ingredient_data']))

            st.table(styled_df)
    else:
        st.write("Geen ingredienten gevonden")

    st.markdown('<h3><strong>Type</strong></h3>', unsafe_allow_html=True)
    types = get_types_w_recipe_id(recipe_id)
    for j in types:
        st.markdown(f"{j}")

def recipe_info_page(recipe_request=None):
    if recipe_request:
        selected_recipe_id = recipe_request
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
    recipe_info_page(None)

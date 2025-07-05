#This file contains the form to select by ingredient.
import streamlit as st
from utils import get_all_ingredients, get_all_type_ingredients
from pages.info_recipe_form import recipe_info_page
#from db import run_query
from pages.test_supabase import run_query

def maak_weekmenu(recipe):
    if 'weekmenu_lijst' not in st.session_state:
        st.session_state.weekmenu_lijst = [recipe]
    else:
        st.session_state.weekmenu_lijst.append(recipe)

def select_ingredient(ingredients_this_month=None):
    # wanneer ingeroepen vanuit maak_weekmenu.py
    if ingredients_this_month:
       ingredients = ingredients_this_month
       st.session_state.weekmenu = True
    # wanneer reload is na klikken op button Toevoegen van een recept
    elif ingredients_this_month in st.session_state:
        ingredients = st.session_state.ingredients_this_month
    # wanneer rechtstreeks vanuit ingredient_form.py (=deze pagina) opgeroepen
    else:
        ingredients = get_all_ingredients()
    ingredient_types = []
    ingredient_types = [x[1] for x in ingredients if x[1] not in ingredient_types]
    ingredient_count = len(ingredients)
    col_count = 3
    cols = st.columns(col_count)
    checkbox_states = [False] * ingredient_count

    with st.form(key="Select Ingredient", clear_on_submit=True):
        for i in range(ingredient_count):
            col_index = i % col_count
            with cols[col_index]:
                checkbox_states[i] = st.checkbox(ingredients[i][0], value=checkbox_states[i])

        submitted = st.form_submit_button("Submit")

    #deze code wordt enkel uitgevoerd als je op submit van de form van de ingredienten hebt geklikt
    if submitted:
        selected_ingredients = [ing for ing, state in zip(ingredients, checkbox_states) if state]
        placeholders = ', '.join(['%s'] * len(selected_ingredients))

        query = f"SELECT DISTINCT ingredient_id FROM ingredient WHERE ingredient IN ({placeholders})"
        ingredient_ids = [row[0] for row in run_query(query, tuple(selected_ingredients))]

        recipe_ids = []
        for ingredient_id in ingredient_ids:
            query = "SELECT recept_id FROM MtM_recept_ingredient WHERE ingredient_id = %s"
            recipe_ids_query = run_query(query, (ingredient_id,))
            recipe_ids.append([id for recipe_ids_query[0] in recipe_ids_query for id in recipe_ids_query[0]])
        recipe_ids_uniek = []
        for i in recipe_ids:
            for j in i:
                if j not in recipe_ids_uniek:
                    recipe_ids_uniek.append(j)
        for recipe_id in recipe_ids_uniek:
            query = "SELECT recept_id, Naam, Beschrijving, Bron, Gemaakt, Locatie FROM recepten WHERE recept_id = %s"
            recipe_details = run_query(query, (recipe_id,))
            st.session_state.recipe_details = recipe_details

    # als submit van de ingredientenlijst éénmaal is aangeklikt, dan bestaat st.session_state_recipe_details met de recepten die overeenkomen met de ingredienten
    # hier wordt in 4 kolommen: recepten - toevoegen - weghalen - welke recepten zijn al geselecteerd getoond
    if 'recipe_details' in st.session_state:
        col1, col2, col3, col4 = st.columns(4)
        col1.write(st.session_state.recipe_details[0][1])
        col1.write(st.session_state.recipe_details[0][0])

        if 'weekmenu' in st.session_state: #wanneer dit opgeroepen wordt vanuit maak_weekmenu.py
            col2.button("Toevoegen", key=str(st.session_state.recipe_details[0][0]) + '_ok', on_click=maak_weekmenu, args=[st.session_state.recipe_details[0][0]], type="primary")
            col3.button("Weghalen", key=str(st.session_state.recipe_details[0][0]) + '_not', type="secondary")
        if 'weekmenu_lijst' in st.session_state:
            col4.write(st.session_state.weekmenu_lijst)

if __name__ == "__main__":
    select_ingredient(ingredients_this_month=None)

#This file contains the form to select by ingredient.
import pandas as pd
import numpy as np
import streamlit as st
from pandas.core.dtypes.inference import is_float
from pandas.util import capitalize_first_letter
from loguru import logger

from utils import get_all_ingredients, get_ingredienttype, get_ingredient_naam, get_recipes_with_ingredient_ids

def maak_weekmenu(recipe):
    if 'weekmenu_lijst' not in st.session_state:
        st.session_state.weekmenu_lijst = [recipe]
    else:
        st.session_state.weekmenu_lijst.append(recipe)

@logger.catch
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

    # 1. Find the dictionary with the max ingredient_id
    max_item = max(ingredients, key=lambda item: item['ingredient_id'])
    # 2. Extract the ingredient_id from that dictionary
    highest_id = max_item['ingredient_id']
    ingredient_count = highest_id + 1

    checkbox_states = [False] * ingredient_count
    df_ingredients = pd.DataFrame(ingredients)
    #creëer een groep 'Geen Type' voor de ingredienten zonder type_id
    df_ingredients = df_ingredients.groupby(df_ingredients['type_id'].fillna('Geen type'))[['ingredient_id', 'ingredient']].agg(list)

    # Maak een dataframe voor elk type
    dfs = {}
    for index, row in df_ingredients.iterrows():
        ingredient = row['ingredient']
        ingredient_id = row['ingredient_id']
        # Create a new dataframe for this type_id
        dfs[index] = pd.DataFrame({'ingredient_id': ingredient_id, 'ingredient': ingredient})
    with st.form(key="Select Ingredient", clear_on_submit=True):
        col_count = 3
        for type_id, df in dfs.items():
            if isinstance(type_id, float):
                type_name = get_ingredienttype(int(type_id))
            else:
                type_name = 'Geen type'
            st.subheader(capitalize_first_letter(type_name))
            cols = st.columns(col_count)
            for k in range(len(df)):
                col_index = k % col_count
                with cols[col_index]:
                    checkbox_states[df.ingredient_id[k]] = st.checkbox(df.ingredient[k], value=checkbox_states[df.ingredient_id[k]], key=df.ingredient_id[k])
            st.divider()
        submitted = st.form_submit_button("Submit")


    #deze code wordt enkel uitgevoerd als je op submit van de form van de ingredienten hebt geklikt
    if submitted:
        ingredient_ids = [index for index, is_checked in enumerate(checkbox_states) if is_checked == True]
        logger.info(ingredient_ids)
        recipe_ids = []
        recipes = get_recipes_with_ingredient_ids(ingredient_ids)
        logger.info(recipes)
        for ingredient_id in ingredient_ids:
            ingredient_naam = get_ingredient_naam(ingredient_id)
            logger.info(ingredient_naam[0]['ingredient'])
            #TODO1: zoek recepten waar alle ingredienten inzitten
            #TODO2: zoek per ingredient recepten en sluit recepten die al genoemd zijn uit
        #
        # recipe_ids_uniek = []
        # for i in recipe_ids:
        #     for j in i:
        #         if j not in recipe_ids_uniek:
        #             recipe_ids_uniek.append(j)
        # for recipe_id in recipe_ids_uniek:
        #     query = "SELECT recept_id, Naam, Beschrijving, Bron, Gemaakt, Locatie FROM recepten WHERE recept_id = %s"
        #     recipe_details = run_query(query, (recipe_id,))
        #     st.session_state.recipe_details = recipe_details

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

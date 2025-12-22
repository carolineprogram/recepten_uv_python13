#This file contains the form to select recipes.
import streamlit as st
from utils import get_recipe_w_recipe_id, update_recipe, update_ingredients
from form_snippets import fill_in_recipe

def unclick_button():
    st.session_state.clicked = False

def goto_selectform():
    st.switch_page("pages/info_recipe_form.py")

# def update_in_db(recipe_id, new_title, new_beschrijving, new_bron, new_gemaakt, new_locatie, ingredients_names, new_ingredients):
#     # Update the recipe in the database
#     succes = True
#     try:
#         update_recipe(recipe_id, new_title, new_beschrijving, new_bron, new_gemaakt, new_locatie)
#         st.success(f"Recept '{new_title}' geupdate!")
#     except Exception as e:
#         st.text(f"Error bij update_recipe: {e}")
#         succes = False
#     try:
#         update_ingredients(ingredients_names, new_ingredients, recipe_id)
#         st.success(f"Ingredients aangepast")
#     except Exception as e:
#         st.text(f"Error bij update_ingredients: {e}")
#         succes = False
#
#     return succes

def recipe_update_page(recipe_id=False):
    if not recipe_id:
        goto_selectform()
    else:
        recipe_data = get_recipe_w_recipe_id(recipe_id)
        recipe_id = recipe_data.data[0]["recept_id"]
        naam = recipe_data.data[0]["Naam"]
        beschrijving = recipe_data.data[0]["Beschrijving"]
        bron = recipe_data.data[0]["Bron"]
        gemaakt = recipe_data.data[0]["Gemaakt"]
        locatie = recipe_data.data[0]["Locatie"]
        link = recipe_data.data[0]["Link"]
        st.title("Update: " + naam)

        update_gelukt = fill_in_recipe(form_key="Update Recipe", button_label="Update", recipe_id=recipe_id, recipe_name=naam, beschrijving=beschrijving, bron=bron, locatie=locatie, link=link, gemaakt=gemaakt)

        st.success(update_gelukt)

if __name__ == "__main__":
    unclick_button()
    if "recipe" in st.session_state:
        selected_recipe = st.session_state["recipe"]
        recipe_update_page(selected_recipe)
    else:
        st.write("Geen recept gevonden om up te daten.")

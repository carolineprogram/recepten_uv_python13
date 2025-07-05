#This file will contain the form to add new recipes.
import streamlit as st
from utils import get_all_types, get_all_ingredients, get_ingredient_id, insert_recipe, insert_ingredients_for_recipe, get_type_id, insert_types_for_recipe
from form_snippets import fill_in_recipe

def add_recipe():
    added_recipe = fill_in_recipe(form_key="Add Recipe", button_label="Voeg recept toe", recipe_id='', recipe_name='', beschrijving='', bron='', locatie='', gemaakt='')
    st.success(added_recipe)

if __name__ == "__main__":
    add_recipe()




#This file will contain the form to add new recipes.
import streamlit as st
from form_snippets import fill_in_recipe

def add_recipe():
    added_recipe = fill_in_recipe(form_key="Add Recipe", button_label="Voeg recept toe", recipe_id='', recipe_name='', beschrijving='', bron='', locatie='', link='', gemaakt='')
    st.success(added_recipe)

if __name__ == "__main__":
    add_recipe()




#This file contains the form to check ingredient availability.

import streamlit as st
from utils import get_all_ingredients
from db import run_query

def ingredient_availability():
    ingredients = get_all_ingredients()

    for ingredient in ingredients:
        st.button(ingredient, on_click=lambda i=ingredient: check_ingredient(i))

def check_ingredient(ingredient):
    query = "SELECT * FROM ingredient WHERE ingredient = %s"
    ingredient_details = run_query(query, (ingredient,))
    st.write(ingredient_details[0])

if __name__ == "__main__":
    ingredient_availability()

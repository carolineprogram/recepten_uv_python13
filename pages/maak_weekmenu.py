#Hier maken we het mogelijk om een weekmenu samen te stellen
import pathlib

import streamlit as st
import random
import pandas as pd

from utils import get_all_ingredients_in_month, get_all_recipe_names, get_ingredients, get_ingredient_naam, get_ingredientdetails, get_recipe_w_recipe_name, load_css
from datetime import date
from loguru import logger

@logger.catch()

def vind_ingredients_seizoen():
    today = date.today()
    today_month = today.month
    today_day = today.day
    # als we in de eerste helft van de maand zitten dan worden de groenten van de vorige maand erbij genomen
    # als we in de tweede helft van de maand zitten dan nemen we de groenten van de volgende maand erbij
    if today_day < 16:
        closest_month = -1
    else:
        closest_month = 1

    if today_month + closest_month in range(1,13):
        extra_month = today_month + closest_month
    elif today_month + closest_month == 0:
        extra_month = 12
    elif today_month + closest_month == 13:
        extra_month = 1
    ingredients_thismonth = get_all_ingredients_in_month(today_month)
    st.write(ingredients_thismonth)
    ingredients_extramonth = get_all_ingredients_in_month(extra_month)
    ingredients_extra = [item for item in ingredients_extramonth if item not in ingredients_thismonth]
    ingredient_all = ingredients_thismonth + ingredients_extra
    st.write(ingredient_all)
    return ingredient_all

def random_choice(d):
    keys = list(d.keys())
    random_key = random.choice(keys)
    return random_key, d[random_key]

def maak_weekmenu():
    valid_recipe_names = []
    recipe_ingredient_map = {}
    all_recipe_names = get_all_recipe_names()
    ingredients_thismonth = [r["ingredient_id"] for r in vind_ingredients_seizoen()]
    # kijk of er een ingredient van het seizoen voorkomt in het recept (1 ingredient is voldoende voor een True)
    for rec in all_recipe_names.data:
        ing_ids = get_ingredients(rec["recept_id"], return_modus = "ids")
        if not ing_ids:
            continue
        if any(i in set(ing_ids) for i in set(ingredients_thismonth)):
            valid_recipe_names.append(rec["Naam"])
            recipe_ingredient_map[rec["Naam"]] = ing_ids

    # Kies 10 recepten en zorg dat de steringredienten maar 1 keer voorkomen

    random_recipes = []
    recipes_om_uit_te_kiezen = recipe_ingredient_map
    recipes_niet_kiezen = []
    gebruikte_steringredienten = []
    for _ in range(10):
        choose_recipe = random_choice(recipes_om_uit_te_kiezen)
        random_recipes.append(choose_recipe)
        for i in choose_recipe[1]:
            if get_ingredientdetails(i).data[0]["steringredient"]:
                gebruikte_steringredienten.append(i)
        for k,j in recipes_om_uit_te_kiezen.items():
            for ingr in gebruikte_steringredienten:
                if ingr in j:
                    recipes_niet_kiezen.append(k)
                    break
        for rec in recipes_niet_kiezen:
            try:
                del recipes_om_uit_te_kiezen[rec]
            except:
                pass
    return random_recipes, gebruikte_steringredienten

css_path = pathlib.Path("styles.css")
load_css(css_path)

if __name__ == "__main__":
    selected_recipes = maak_weekmenu()
    selected_recipe_names = selected_recipes[0]
    gebruikte_ingredienten = selected_recipes[1]
    st.write("Gebruikte ingredienten")
    ingredienten = []
    for i, ingr in enumerate(gebruikte_ingredienten, start=1):
        ingr_naam = get_ingredient_naam(ingr)[0]["ingredient"]
        ingredienten.append(ingr_naam)
    st.write(" - ".join(ingredienten))

    st.write("🧑\u200d🍳 10 recepten met een spreiding van de steringredienten:")
    recipe_data = []
    for name in selected_recipe_names:
        this_recipe = {}
        this_recipe["Naam"] = name[0]
        recipe_id = get_recipe_w_recipe_name(name[0]).data[0]["recept_id"]
        this_recipe["recept_id"] = recipe_id
        recipe_ingredients = []
        for ingr in name[1]:
            ingr_naam = get_ingredient_naam(ingr)[0]["ingredient"]
            if ingr in ingredienten:
                recipe_ingredients.append(f'{ingr_naam}')
            else:
                recipe_ingredients.append(f'{ingr_naam}')
        this_recipe["Ingredienten"] = ", ".join(recipe_ingredients)
        recipe_data.append(this_recipe)

    df = pd.DataFrame(recipe_data)
    if df.empty is False:
        # In tabelvorm met linken
        #df['Naam'] = df.apply(lambda row: f"[{row['Naam']}](info_recipe_form?recept_id={row['recept_id']})", axis=1)
        #st.markdown(df.sort_values("Naam").to_markdown(index=False), unsafe_allow_html=True)
        # Display each row as a button

        # Wrap the button in a div with a custom class
        st.markdown(
            """
            <div class="recipe-button">
                <style>
                    .recipe-button { margin-bottom: 20px; }
                </style>
            """,
            unsafe_allow_html=True
        )

        for _, row in df.iterrows():
            recipe_name = row["Naam"]
            recept_id = row["recept_id"]
            recept_ingredienten = row["Ingredienten"]
            # Create a link button for each recipe

            st.link_button(
            f"**{recipe_name}** met {recept_ingredienten}",
            f"info_recipe_form?recept_id={recept_id}",
                width="stretch",
                key=f"recept_weekmenu{recept_id}"
            )

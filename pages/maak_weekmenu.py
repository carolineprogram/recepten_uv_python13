#Hier maken we het mogelijk om een weekmenu samen te stellen
import streamlit as st

from utils import get_all_ingredients_in_month, get_all_recipe_names, get_ingredients
from pages.ingredient_form import select_ingredient
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
    ingredients_extramonth = get_all_ingredients_in_month(extra_month)
    ingredients_extra = [item for item in ingredients_extramonth if item not in ingredients_thismonth]
    ingredient_all = ingredients_thismonth + ingredients_extra

    return ingredient_all
    #select_ingredient(ingredients_this_month = ingredient_all)


def maak_weekmenu():
    valid_recipe_names = []
    recipe_ingredient_map = {}
    all_recipe_names = get_all_recipe_names()
    ingredients_thismonth = [r["ingredient_id"] for r in vind_ingredients_seizoen()]
    for rec in all_recipe_names.data:
        ing_ids = get_ingredients(rec["recept_id"], return_modus = "ids")
        if not ing_ids:
            continue
        if set(ing_ids).issubset(set(ingredients_thismonth)):
            valid_recipe_names.append(rec["Naam"])
            recipe_ingredient_map[rec["Naam"]] = ing_ids

       # -------------------------------------------------
       # 3️⃣ Choose 10 most distinct recipes
       # -------------------------------------------------

        sorted_recipes = sorted(
           recipe_ingredient_map.items(),
           key=lambda item: (len(item[1]), sum(item[1]))
        )
        selected_recipe_names = [name for name, _ in sorted_recipes[:10]]

       # -------------------------------------------------
       # 4️⃣ Output the result
       # -------------------------------------------------

    return selected_recipe_names


if __name__ == "__main__":
    selected_recipe_names = maak_weekmenu()
    st.write("🧑\u200d🍳 10 recipes that use only this‑month ingredients (most distinct):")
    for i, name in enumerate(selected_recipe_names, start=1):
        st.write(f"{i}. {name}")

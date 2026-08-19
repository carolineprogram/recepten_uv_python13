import streamlit as st
import math
from utils import get_all_recipe_names, get_all_types, get_types_w_recipe_id, get_all_ingredients, get_ingredients, insert_recipe, update_recipe, update_ingredients, update_types, get_all_receptbron
from streamlit_tags import st_tags
from loguru import logger

def select_recipe(form_key="Select Recipe", button_label="Info"):
    """ een dropdown selectie om een recept te kiezen  """
    result = get_all_recipe_names()
    recipe_names_to_id = {item["Naam"]:item["recept_id"] for item in result.data if item["Naam"]}

    with st.form(key=form_key, clear_on_submit=True):
        selected_recipe_naam = st.selectbox("Kies recept?", list(recipe_names_to_id.keys()))
        submitted = st.form_submit_button(button_label)

        if submitted:
            return recipe_names_to_id[selected_recipe_naam] #geeft recipe_id door

    return None

@logger.catch
def fill_in_recipe(form_key, button_label, recipe_id, recipe_name, beschrijving, bron, locatie, link, gemaakt):
    with st.form(key=form_key, clear_on_submit=True):
        new_title = st.text_input("Titel", value=recipe_name)
        new_beschrijving = st.text_area("Beschrijving", value=beschrijving)

        bron_data = get_all_receptbron().data
        bron_data_name = [row["bron"] for row in bron_data]
        bron_data_id = [row["bron_id"] for row in bron_data]
        bron_data_dict = dict(zip(bron_data_id, bron_data_name))

        # Convert dictionary keys to a list to locate the index
        bron_keys_list = list(bron_data_dict.keys())
        bron_default_index = bron_keys_list.index(bron) if bron in bron_keys_list else 0

        new_bron_id = st.selectbox("Welk kookboek?", options=list(bron_data_dict.keys()),
                                     index=bron_default_index,
                                     format_func=lambda x: bron_data_dict[x])
        new_bron = new_bron_id

        new_locatie = st.text_input("Locatie", value=locatie)
        new_link = st.text_input("Link", value=link)
        new_gemaakt = st.checkbox("Al gemaakt?", value=gemaakt)
        # Postgres kan niet goed om met omzetting '' naar NULL -> zelf al omzetten, anders error 22P02
        if new_gemaakt == '':
            new_gemaakt = None

        # get_all_ingredients() return is tuple met eerst ingredient en dan type
        all_ingredients = get_all_ingredients()
        all_ingredients_zondertype = [x["ingredient"] for x in all_ingredients]

        if recipe_id:
            ingredients = get_ingredients(recipe_id)
            ingredients_in_db = [item["ingredient"] for item in ingredients]
        else:
            ingredients_in_db = []

        selected_ingredients = st_tags(
            label='# Vul ingredienten aan:',
            text='Press enter om ingredient toe te voegen',
            value=ingredients_in_db,
            suggestions=all_ingredients_zondertype,
            maxtags=20,
            key='ingredient_tags'
        )

        #Vul types aan in checkboxes in 3 kolommen
        st.html('<h3><strong>Vul types aan</h3></strong>')

        types = get_all_types().data
        if recipe_id:
            types_in_db = get_types_w_recipe_id(recipe_id) #resultaat is list met lists[type_id, type_naam] voor bepaald recept
        else:
            types_in_db = []
        available_types = {}
        aantal_cols = 3
        cols = st.columns(aantal_cols)
        lengte_types = len(types)
        aantal_types_in_cols = aantal_types_in_col = math.ceil(lengte_types/aantal_cols)
        i = 0
        col_index = 0
        for t in types:
            i += 1
            if i > aantal_types_in_col:
                col_index += 1
                aantal_types_in_col = aantal_types_in_cols * (col_index + 1)

            with cols[col_index]:
                if t["type"] in types_in_db:
                    value = True
                else:
                    value = False
                checkbox_value = st.checkbox(key=t, label=t["type"], value=value)
                available_types[t["type"]] = checkbox_value

        submitted = st.form_submit_button(button_label)

    if submitted:
        succes = True

        selected_types = [k for k, v in available_types.items() if v]

        if form_key == "Add Recipe":
            result = insert_recipe(new_title, new_beschrijving, new_bron, new_locatie, new_link, new_gemaakt)
            logger.info(result)
            recipe_id = result.data[0]["recept_id"]

            input_old_ingredients = ''
            input_old_types=''

        elif form_key == "Update Recipe":
            input_old_ingredients = ingredients_in_db
            input_old_types = types_in_db
            try:
                update_recipe(recipe_id, new_title, new_beschrijving, new_bron, new_locatie, new_link, new_gemaakt)
                st.success(f"Recept '{new_title}' geupdate!")
            except Exception as e:
                st.text(f"Error bij update_recipe: {e}")
                succes = False
        try:
            update_ingredients(old_ingredients=input_old_ingredients, new_ingredients=selected_ingredients, recipe_id=recipe_id)
            logger.info(input_old_ingredients)
            logger.info(selected_ingredients)
            logger.info(recipe_id)
            st.success(f"Ingredients aangepast")
        except Exception as e:
            st.text(f"Error bij update_ingredients: {e}")
            succes = False

        try:
            update_types(old_types=input_old_types, new_types=selected_types, recipe_id=recipe_id)
            st.success(f"Types aangepast")
        except Exception as e:
            st.text(f"Error bij update_types: {e}")
            succes = False

        return succes
    return None


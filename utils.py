#This file contains utility functions for fetching data.
#from db import run_query
import streamlit as st

from run_query import run_query
from loguru import logger
#TODO: tabel recepten_IngredientBeschikbaar gemaakt - en kolommen 'hele_jaar' en maanden 'jan -> dec' gewist.
"""
SELECT-queries
    bouw query op:
    - query is type query (select, update, insert, delete)
    - data is een list
    - where is een dictionary
    - in_ in een tuple
    - distinct is enkel een opdracht (geen input nodig)
    - order is string
"""


def get_recipe_w_recipe_name(recipe_name):
    """
    Equivalent to "SELECT recept_id, Beschrijving, Bron, Gemaakt, Locatie, Link FROM recepten_Recepten WHERE Naam = %s"
    """
    return run_query("select", "recepten_Recepten", ["recept_id", "Beschrijving", "Bron", "Gemaakt", "Locatie", "Link"], where = {"Naam": recipe_name})

def get_recipe_w_recipe_id(recipe_id):
    """
    Equivalent to query = "SELECT Naam, Beschrijving, Bron, Gemaakt, Locatie, Link FROM recepten_recepten WHERE recept_id = %s ORDER BY Naam"
    """
    return run_query("select", "recepten_Recepten", ["recept_id", "Naam", "Beschrijving", "Bron", "Gemaakt", "Locatie", "Link"], where = {"recept_id": recipe_id}, order="Naam")

def get_recipe_id_w_type_id(type_id):
    """
    Equivalent to "SELECT recept_id FROM MtM_recept_type WHERE type_id = %s"
    """
    return run_query("select", "recepten_Recept_Type", ["recept_id"], where = {"type_id": type_id})

def get_all_recipe_names():
    """
    Equivalent to "SELECT recept_id, Naam FROM recepten_recepten ORDER BY Naam"
    """
    return run_query("select", "recepten_Recepten", ["recept_id", "Naam"], order="Naam")

def get_recipes_with_ingredient_ids(ingredient_ids):
    """
    Equivalent voor SELECT rec.* FROM "recepten_Recepten" as rec LEFT JOIN "recepten_Recept_Ingredient" as RI ON rec.recept_id = RI.recept_id WHERE RI.ingredient_id IN (13, 14, 23, 27)"
    """
    recipes = []
    for i in ingredient_ids:
        recipes_all = run_query("select", "recepten_Recepten, recepten_Recept_Ingredient",["*"], where = {"recepten_Recept_Ingredient.ingredient_id": i})
        recipes.append((recipes_all))
    return recipes
    #     recipe_ids_query = run_query(query, (ingredient_id,))
    #     recipe_ids.append([id for recipe_ids_query[0] in recipe_ids_query for id in recipe_ids_query[0]])

    pass

def get_recipes_w_bron_id(bron_id):
    return run_query("select", "recepten_Recepten", ["*"], where = {"Bron": bron_id})



def get_types_w_recipe_id(recipe_id):
    """
    bouw query op:
    - query is type query (select, update, insert, delete)
    - data is een list
    Equivalent to "SELECT type_id FROM recepten_Recept_Type WHERE recept_id = recipe_id"
    """

    types_ids = run_query("select", "recepten_Recept_Type", "type_id", where={"recept_id": recipe_id})
    types = []

    if types_ids.data and isinstance(types_ids.data, list) and len(types_ids.data) > 0:
        for i in types_ids.data:
            """
            Equivalent to "SELECT * FROM recepten_Recepttype WHERE type_id =type_id)
            """
            type_details = run_query("select", "recepten_Recepttype", where={"type_id": i["type_id"]})
            types.append(type_details.data[0].get("type"))
    else:
        st.write("Probleem: geen type_id toegekend aan dit recept in recepten_Recept_Type")

    return types

def get_type_id(type_naam):
    """
    Equivalent to "SELECT type_id FROM type WHERE type = type_naam"
    """
    rows = run_query("select", "recepten_Recepttype", where={"type": type_naam})
    if rows:
        return rows.data[0]  # Return the first ingredient_id found
    else:
        return None  # Return None if ingredient not found

def get_all_types():
    """
    Equivalent to "SELECT type_id, type FROM recepten_Recepttype ORDER BY type"
    """
    return run_query("select", "recepten_Recepttype", ["type_id", "type"], order="type")

def get_ingredienttype(type_id):
    """
    Equivalent to "SELECT type FROM recepten_Ingredienttype WHERE type_id = type_id"
    """
    rows = run_query("select", "recepten_Ingredienttype", where={"type_id": type_id})
    if rows:
        return rows.data[0]["type"]  # Return the first ingredient_id found
    else:
        return None  # Return None if ingredient not found

def get_ingredients(recipe_id):
    """
    Equivalent to "SELECT ingredient_id FROM recepten_Recept_Ingredient WHERE recept_id = recipe_id"
    """
    ingredient_ids = run_query("select", "recepten_Recept_Ingredient", ["ingredient_id"],
                               where={"recept_id": recipe_id}, order="ingredient_id")

    ingredients = []
    for i in ingredient_ids.data:
        ingredient_id = i["ingredient_id"]
        """
        Equivalent to "SELECT * FROM recepten_Ingredient WHERE ingredient_id = ingredient_id"
        """
        ingredient_details = run_query("select", "recepten_Ingredient", "*", where={"ingredient_id": ingredient_id})
        try:
            for j in ingredient_details.data:
                ingredients.append(j)
        except:
            ingredients = []
    return ingredients

def get_all_ingredients():
    """
    SELECT ingredient_id, ingredient, type FROM recepten_Ingredient ORDER BY ingredient"
    """
    return run_query("select", "recepten_Ingredient", "*").data


def get_all_ingredients_in_month(month):
    """
    SELECT ingredient_id, ingredient, type FROM ingredient WHERE hele_jaar = '1' OR {month} = '1' ORDER BY ingredient"
    """
    return [(row[1], row[2]) for row in run_query("select", "recepten_IngredientBeschikbaar", ["ingredient_id"], [("maand", month)])]

def get_ingredient_id(ingredient_naam):
    """
    SELECT ingredient_id FROM ingredient WHERE ingredient = %s
    """
    return run_query("select", "recepten_Ingredient", ["ingredient_id"], {"ingredient": ingredient_naam}).data

def get_ingredient_naam(ingredient_id):
    """
    SELECT ingredient FROM ingredient WHERE ingredient_id = %s
    """
    return run_query("select", "recepten_Ingredient", ["ingredient_id", "ingredient"], {"ingredient_id": ingredient_id}).data

def get_all_type_ingredients():
    """
    SELECT DISTINCT type FROM ingredient ORDER BY type
    SELECT DISTINCT bestaat niet in PostGRES -> gebruik daarom gewone select en filter dan dubbel uit met set()
    """
    result =  [row[0] for row in run_query("select", "recepten_Recepttype", ["type"])]

    return set(result)

def get_all_receptbron():
    """
    Equivalent to "SELECT type_id, type FROM recepten_Recepttype ORDER BY type"
    """
    return run_query("select", "recepten_Receptbron", ["bron_id", "bron"], order="bron")



"""
INSERT-queries
    bouw query op voor bulk insert:
    - query is type query (insert)
    - data is een list van dictionaries [{}, {}]
    try:
    response = (
        supabase.table("characters")
        .insert([
            {"id": 1, "name": "Frodo"},
            {"id": 2, "name": "Sam"},
        ])
        .execute()
    )
    return response
except Exception as exception:
    return exception
"""

def insert_recipe(new_title, new_beschrijving, new_bron, new_locatie, new_link, new_gemaakt):
    """
    Equivalent voor "INSERT INTO recepten_recepten (Naam, Beschrijving, Bron, Gemaakt, Locatie) VALUES (name, description, source, made, location)"
    """
    data = [{"Naam": new_title, "Beschrijving": new_beschrijving, "Bron": new_bron, "Locatie": new_locatie, "Link": new_link, "Gemaakt": new_gemaakt}]

    return run_query("insert", "recepten_Recepten", data)

def insert_types_for_recipe(type_list, recipe_id):
    data = []
    for i in type_list:
        #Equivalent voor "INSERT INTO MtM_recept_type (recept_id, type_id) VALUES (%s, %s)"
        nieuwe_data = {"recept_id": recipe_id, "type_id": i['type_id']}
        data.append(nieuwe_data)

    return run_query("insert", "recepten_Recept_Type", data)

def insert_ingredients_for_recipe(ingredient_list, recipe_id):
    for i in ingredient_list:
        data = [{"recept_id": recipe_id, "ingredient_id": i}]
        run_query("insert", "recepten_Recept_Ingredient", data)
    return True

def insert_new_ingredients(ingredient_name):
    """
    Equivalent voor query = "INSERT INTO ingredient (ingredient) VALUES (%s)"
    """
    data = [{"ingredient": ingredient_name}]
    return run_query("insert", "recepten_Ingredient", data)
#TODO: zorg dat je type kan ingeven met dropdowmenu

"""
DELETE-queries
"""


def delete_ingredients(ingredient_list, recipe_id):
    for i in ingredient_list:
        """
        query = "DELETE FROM MtM_recept_ingredient WHERE recept_id = (%s) AND ingredient_id = (%s)"
        """
        data = {"recept_id": recipe_id, "ingredient_id": i}
        run_query("delete", "recepten_Recept_Ingredient", where=data)

def delete_types_for_recipe(type_list, recipe_id):
    for i in type_list:
        #query = "DELETE FROM MtM_recept_type WHERE recept_id = (%s) AND type_id = (%s)"
        data = {"recept_id": recipe_id, "type_id": i['type_id']}
        run_query("delete", "recepten_Recept_Type", where=data)

"""
UPDATE-queries
"""

def update_recipe(recipe_id, title, beschrijving, bron, locatie, link, gemaakt):
    data = {
        "Naam": title,
        "Beschrijving": beschrijving,
        "Bron": bron,
        "Locatie": locatie,
        "Link": link,
        "Gemaakt": gemaakt
    }
    return run_query("update", "recepten_Recepten", data, {"recept_id": recipe_id})

def update_types(old_types, new_types, recipe_id):
    unchanged_types = [item for item in old_types if item in new_types]
    todelete_types = [item for item in old_types if item not in unchanged_types]
    todelete_types_ids = [get_type_id(item) for item in todelete_types]
    insert_types = [item for item in new_types if item not in unchanged_types]
    insert_types_ids = []
    for type in insert_types:
        try:
            type_id = get_type_id(type)
            insert_types_ids.append(type_id)
        except Exception as e:
            st.text(f"Error bij update_types - type_id: {e}")

    if todelete_types_ids:
        try:
            delete_types_for_recipe(todelete_types_ids, recipe_id)
        except Exception as e:
            st.text(f"Geen types gewist - error: {e}")
    if insert_types_ids:
        try:
            insert_types_for_recipe(insert_types_ids, recipe_id)
        except Exception as e:
            st.text(f"Geen types ingevoerd - error: {e}")

def update_ingredients(old_ingredients, new_ingredients, recipe_id):
    unchanged_ingredients = [item for item in old_ingredients if item in new_ingredients]
    todelete_ingredients = [item for item in old_ingredients if item not in unchanged_ingredients]
    todelete_ingredients_ids = [get_ingredient_id(item)[0].get("ingredient_id") for item in todelete_ingredients]
    insert_ingredients = [item for item in new_ingredients if item not in unchanged_ingredients]


    insert_ingredients_ids = []
    for i in insert_ingredients:
        ingredient_id = get_ingredient_id(i)
        if ingredient_id:
            insert_ingredients_ids.append(ingredient_id[0].get("ingredient_id") )
        else:
            ingredient_id = insert_new_ingredients(i).data[0].get("ingredient_id")
            insert_ingredients_ids.append(ingredient_id)

    if todelete_ingredients_ids:
        delete_ingredients(todelete_ingredients_ids, recipe_id)
    if insert_ingredients_ids:
        insert_ingredients_for_recipe(insert_ingredients_ids, recipe_id)


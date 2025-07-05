#This file contains utility functions for fetching data.
#from db import run_query
import streamlit as st
from pages.test_supabase import run_query
#TODO: tabel recepten_type is gewijzigd in recepten_Recepttype
#TODO: tabel recepten_IngredientBeschikbaar gemaakt - en kolommen 'hele_jaar' en maanden 'jan -> dec' gewist.
#TODO: tabel recepten_ingredient naar recepten_Ingredient
"""
SELECT-queries
    bouw query op:
    - query is type query (select, update, insert, delete)
    - data is een list
    - where is een dictionary
    - order is string
"""


def get_recipe_w_recipe_name(recipe_name):
    """
    Equivalent to "SELECT recept_id, Beschrijving, Bron, Gemaakt, Locatie FROM recepten_recepten WHERE Naam = %s"
    """
    return run_query("select", "recepten_Recepten", ["recept_id", "Beschrijving", "Bron", "Gemaakt", "Locatie"], where = {"Naam": recipe_name})

def get_recipe_w_recipe_id(recipe_id):
    """
    Equivalent to query = "SELECT Naam, Beschrijving, Bron, Gemaakt, Locatie FROM recepten_recepten WHERE recept_id = %s ORDER BY Naam"
    """
    return run_query("select", "recepten_Recepten", ["recept_id", "Naam", "Beschrijving", "Bron", "Gemaakt", "Locatie"], where = {"recept_id": recipe_id}, order="Naam")

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
        type_id =  types_ids.data[0].get("type_id")  # Get 'type_id' from the first element
        """
        Equivalent to "SELECT * FROM recepten_Recepttype WHERE type_id =type_id)
        """
        type_details = run_query("select", "recepten_Recepttype", where={"type_id": type_id})
        if type_details:
            types.append(type_details.data[0].get("type"))
    else:
        st.write("Probleem: geen type_id toegekend aan dit recept in recepten_Recept_Type")

    return types

def get_type_id(type_naam):
    """
    Equivalent to "SELECT type_id FROM type WHERE type = type_naam"
    """
    rows = run_query("select", "recepten_Recepttype", where={"type_naam": type_naam})
    if rows:
        return rows[0][0]  # Return the first ingredient_id found
    else:
        return None  # Return None if ingredient not found

def get_all_types():
    """
    Equivalent to "SELECT type_id, type FROM recepten_Recepttype ORDER BY type"
    """
    return run_query("select", "recepten_Recepttype", ["type_id", "type"], order="type")

def get_ingredients(recipe_id):
    """
    Equivalent to "SELECT ingredient_id FROM recepten_MtM_recept_ingredient WHERE recept_id = recipe_id"
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
        for j in ingredient_details.data:
            ingredients.append(j)

    return ingredients

def get_all_ingredients():
    """
    SELECT ingredient_id, ingredient, type FROM recepten_Ingredient ORDER BY ingredient"
    """
    return [(row[0]) for row in run_query("select", "recepten_Ingredient", "*")]
    #return [(row[1], row[2]) for row in run_query("select", "recepten_Ingredient", ["ingredient_id, ingredient, type"], order="ingredient")]

def get_all_ingredients_in_month(month):
    """
    SELECT ingredient_id, ingredient, type FROM ingredient WHERE hele_jaar = '1' OR {month} = '1' ORDER BY ingredient"
    """
    return [(row[1], row[2]) for row in run_query("select", "recepten_IngredientBeschikbaar", ["ingredient_id"], [("maand", month)])]

def get_ingredient_id(ingredient_naam):
    """SELECT ingredient_id FROM ingredient WHERE ingredient = %s"
    """
    return [(row[0]) for row in run_query("select", "recepten_Ingredient", ["ingredient_id"])]
    if rows:
        return rows[0][0]  # Return the first ingredient_id found
    else:
        return None  # Return None if ingredient not found
def get_all_type_ingredients():
    """
    SELECT DISTINCT type FROM ingredient ORDER BY type
    SELECT DISTINCT bestaat niet in PostGRES -> gebruik daarom gewone select en filter dan dubbel uit met set()
    """
    result =  [row[0] for row in run_query("select", "recepten_Recepttype, "["type"])]

    return set(result)



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

def insert_recipe(data):
    """
    Equivalent voor "INSERT INTO recepten_recepten (Naam, Beschrijving, Bron, Gemaakt, Locatie) VALUES (name, description, source, made, location)"
    """
    return run_query("insert", "recepten_Recepten", data)

def insert_types_for_recipe(type_list, recipe_id):
    for i in type_list:
        query = "INSERT INTO MtM_recept_type (recept_id, type_id) VALUES (%s, %s)"
        params = (recipe_id, i)
        return run_query(query, tabel, dict)


def insert_ingredients_for_recipe(ingredient_list, recipe_id):
    for i in ingredient_list:
        print(i)
        query = "INSERT INTO MtM_recept_ingredient (recept_id, ingredient_id) VALUES (%s, %s)"
        params = (recipe_id, i)
        run_query(query, params)
    return True

def insert_new_ingredients(ingredient_name):
    query = "INSERT INTO ingredient (ingredient) VALUES (%s)"
    params = (ingredient_name, )
    return run_query(query, tabel, dict)
#TODO: zorg dat je type kan ingeven met dropdowmenu

"""
DELETE-queries
"""


def delete_ingredients(ingredient_list, recipe_id):
    for i in ingredient_list:
        query = "DELETE FROM MtM_recept_ingredient WHERE recept_id = (%s) AND ingredient_id = (%s)"
        params = (recipe_id, i)
        return run_query(query, tabel, dict)

def delete_types(type_list, recipe_id):
    for i in type_list:
        query = "DELETE FROM MtM_recept_type WHERE recept_id = (%s) AND type_id = (%s)"
        params = (recipe_id, i)
        return run_query(query, tabel, dict)

"""
UPDATE-queries
"""

def update_recipe(recipe_id, title, beschrijving, bron, gemaakt, locatie):
    query = "UPDATE recepten SET Naam = %s, Beschrijving = %s, Bron = %s, Gemaakt = %s, Locatie = %s WHERE recept_id = %s"
    params = (title, beschrijving, bron, gemaakt, locatie, recipe_id)
    return run_query(query, tabel, dict)

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
        delete_types(todelete_types_ids, recipe_id)
    if insert_types_ids:
        insert_types_for_recipe(insert_types_ids, recipe_id)


def update_ingredients(old_ingredients, new_ingredients, recipe_id):
    unchanged_ingredients = [item for item in old_ingredients if item in new_ingredients]
    todelete_ingredients = [item for item in old_ingredients if item not in unchanged_ingredients]
    todelete_ingredients_ids = [get_ingredient_id(item) for item in todelete_ingredients]
    insert_ingredients = [item for item in new_ingredients if item not in unchanged_ingredients]

    insert_ingredients_ids = []
    for ingredient in insert_ingredients:
        ingredient_id = get_ingredient_id(ingredient)
        if ingredient_id:
            insert_ingredients_ids.append(ingredient_id)
        else:
            ingredient_id = insert_new_ingredients(ingredient)
            insert_ingredients_ids.append(ingredient_id)

    if todelete_ingredients_ids:
        delete_ingredients(todelete_ingredients_ids, recipe_id)
    if insert_ingredients_ids:
        insert_ingredients_for_recipe(insert_ingredients_ids, recipe_id)


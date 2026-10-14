import streamlit as st
import pandas as pd
from utils import get_all_ingredients, get_ingredienttype, get_all_types
from form_snippets import fill_in_recipe
from loguru import logger

all_ingredients = get_all_ingredients()
all_ingredients_az = sorted(all_ingredients, key=lambda x: x["ingredient"])
all_types = get_all_types()
data = []

for i in all_ingredients_az:
    if i["type_id"]:
        type_naam = [x["type"] for x in all_types if x["type_id"] == i["type_id"]][0]
    else:
        type_naam =""
    data.append(
        {"Naam": i["ingredient"],
         "Type": type_naam
        }
    )

df = pd.DataFrame(data)
st.write(df)
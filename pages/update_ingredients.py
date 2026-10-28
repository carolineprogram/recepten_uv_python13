import streamlit as st
import pandas as pd
from utils import get_all_ingredients, get_ingredienttype, get_all_types, get_ingredientmonths, get_all_ingredienttypes
from loguru import logger

st.title("Ingredienten")

maandnamen = ["jan", "feb", "maa", "apr", "mei", "jun", "jul", "aug", "sep", "okt", "nov", "dec"]

# ---------- Build the dataframe (only once, then keep in session_state) ----------
def build_dataframe():
    all_ingredients_az = sorted(get_all_ingredients(), key=lambda x: x["ingredient"])
    type_naam_map = {x["type_id"]: x["type"] for x in get_all_ingredienttypes()}
    data = []

    for i in all_ingredients_az:
        type_naam = type_naam_map.get(i["type_id"], "")
        #if i["type_id"]:
        #    type_naam = [x["type"] for x in get_all_ingredienttypes() if x["type_id"] == i["type_id"]][0]
        #else:
        #    type_naam =""
        ingr_months = get_ingredientmonths(i["ingredient_id"]).data # dataoutput:[{maand: 4}, {maand:5}]
        maand_nrs = [m["maand"] for m in ingr_months]

        if 99 in maand_nrs:
            maand_cols = {m:"x" for m in maandnamen}
        else:
            maand_cols = {maandnamen[nr - 1]: "x" for nr in maand_nrs if 1 <= nr <= 12}

        data.append(            {
            "ingredient_id": i["ingredient_id"],
            "Naam": i["ingredient"],
            "Type": type_naam,
            **maand_cols,
            "Steringr": i["steringredient"],
            "Alternatief": i["alternatief"],
            }

    )

    df = pd.DataFrame(data)


    for col in maandnamen:
        if col not in df.columns:
            df[col] = ""

    return df[["ingredient_id", "Naam", "Type"] + maandnamen + ["Steringr", "Alternatief"]].fillna("")


if "df_ingredients" not in st.session_state:
    st.session_state.df_ingredients = build_dataframe()

# ---------- Editable table ----------
edited_df = st.data_editor(
    st.session_state.df_ingredients,
    column_config={
        "ingredient_id": st.column_config.Column(disabled=True),  # id not editable
    },
    hide_index=True,
    key="ingredient_editor",
)

# ---------- Update button ----------
if st.button("Update", type="primary"):
    changes_detected = not edited_df.equals(st.session_state.df_ingredients)
    if changes_detected:
        st.session_state.df_ingredients = edited_df

        # Find and show what changed
        old = st.session_state.df_ingredients  # note: already updated — see remark below
        for _, row in edited_df.iterrows():
            st.write(f"Bijgewerkt: {row['Naam']}")

        # Here you would write changes back to your database, e.g.:
        # for record in edited_df.to_dict("records"):
        #     update_ingredient(record["ingredient_id"], ...)
        st.success("Wijzigingen opgeslagen!")
    else:
        st.info("Geen wijzigingen gevonden.")
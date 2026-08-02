import streamlit as st

#sidebar navigations

pages = {
    "Zoek recept": [
        st.Page("pages/info_recipe_form.py", title="Zoek op titel"),
        st.Page("pages/ingredient_form.py", title="Zoek op ingredient"),
        st.Page("pages/type_form.py", title="Zoek op type recept"),
        st.Page("pages/kookboek_form.py", title="Zoek op kookboek"),
    ],
    "Doe-pagina's": [
        st.Page("pages/add_recipe_form.py", title="Voeg recept toe"),
    ],
    "Nog opkuisen": [
        st.Page("pages/availability_form.py", title="Availability form"),
        st.Page("pages/maak_weekmenu.py", title="Maak weekmenu"),
        st.Page("pages/test_supabase.py", title="Test Supabase"),
        st.Page("pages/update_recipe_form.py")
    ]
}

pg = st.navigation(pages)
pg.run()


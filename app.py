import streamlit as st
from supabase import Client
from db import get_connection

supabase: Client = get_connection()

#login: Supabase zal enkel SMTP (mails verzenden) voorzien voor wie in het team zit: supabase.com/dashboard/org
# zit je niet in het team dan krijg je de error Email address not authorized.


def sign_up(email, password):
    try:
        user = supabase.auth.sign_up({"email": email, "password": password})
        return user
    except Exception as e:
        st.error(f"Registration failed: {e}")

def sign_in(email, password, client: supabase.Client):
    try:
        user = client.auth.sign_in_with_password({'email': email, 'password': password})
        return user
    except Exception as e:
        st.error(f"Login failed: {e}")

def sign_out():
    try:
        supabase.auth.sign_out()
        st.session_state.user_email = None
        st.rerun()
    except Exception as e:
        st.error(f"Logout failed= {e}")

def main_app(user_email):
    st.title("Welkom!")
    st.success(f"Welkom {user_email}")
    if st.button("Logout"):
        sign_out()

def auth_screen():
    st.title("Receptendatabank")
    option = st.selectbox("Kies: ", ["Login", "Sign Up"])
    email = st.text_input("Email: ")
    password = st.text_input("Password: ", type="password")

    if option == "Sign Up" and st.button("Register"):
        user = sign_up(email, password)
        if user and user.user:
            st.success("Registratie succesvol, please sign in.")

    if option == "Login" and st.button("Login"):
        user = sign_in(email, password, supabase)
        if user and user.user:
            st.session_state.user_email = user.user.email
            st.success(f"Welcome back!")
            st.rerun()


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
        st.Page("pages/maak_weekmenu.py", title="Maak weekmenu"),
    ],
    "Nog opkuisen": [
        st.Page("pages/availability_form.py", title="Availability form"),
        st.Page("test_supabase.py", title="Test Supabase"),
        st.Page("pages/update_recipe_form.py")
    ]
}


if "user_email" not in st.session_state:
    st.session_state.user_email = None
if st.session_state.user_email:
    main_app(st.session_state.user_email)
    pg = st.navigation(pages)
    pg.run()
else:
    auth_screen()


import streamlit as st

from supabase import create_client, Client
from db import get_connection

# Supabase client
supabase_url = st.secrets['supabase']["SUPABASE_URL"]
supabase_key = st.secrets['supabase']["SUPABASE_KEY"]
supabase = create_client(supabase_url, supabase_key)

# psycopg2 connection
# zie db.py

conn = get_connection()  # Get connection

# Fetch data using Supabase client
data = conn.table("recepten_Recepten").insert({"Naam": 'Artisjokken'}).execute()

st.write("Data from Supabase client:", data)

# Fetch data using psycopg2
cursor.execute('SELECT * FROM "recepten_Recepten";')
rows = cursor.fetchall()
st.write("Data from psycopg2:", rows)

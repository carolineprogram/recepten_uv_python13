import streamlit as st
import psycopg2
from supabase import create_client, Client

# Supabase client
supabase_url = st.secrets['supabase']["SUPABASE_URL"]
supabase_key = st.secrets['supabase']["SUPABASE_KEY"]
supabase = create_client(supabase_url, supabase_key)

# psycopg2 connection
conn = psycopg2.connect(
    dbname=st.secrets['supabase']["DB_NAME"],
    user=st.secrets['supabase']["DB_USER"],
    password=st.secrets['supabase']["DB_PASSWORD"],
    host=st.secrets['supabase']["DB_HOST"],
    port=st.secrets['supabase']["DB_PORT"],
    sslmode = 'require'
)
cursor = conn.cursor()

# Fetch data using Supabase client
data = supabase.table("recepten_Recepten").select("*").execute()
st.write("Data from Supabase client:", data)

# Fetch data using psycopg2
cursor.execute('SELECT * FROM "recepten_Recepten";')
rows = cursor.fetchall()
st.write("Data from psycopg2:", rows)

#This file will handle database connections.
import streamlit as st
import psycopg2
from supabase import create_client, Client

# Supabase client
def get_connection():
    supabase_url = st.secrets['supabase']["SUPABASE_URL"]
    supabase_key = st.secrets['supabase']["SUPABASE_KEY"]
    return create_client(supabase_url, supabase_key)

# psycopg2 connection
def get_psycopg2_connection():
    conn = psycopg2.connect(
        dbname=st.secrets['supabase']["DB_NAME"],
        user=st.secrets['supabase']["DB_USER"],
        password=st.secrets['supabase']["DB_PASSWORD"],
        host=st.secrets['supabase']["DB_HOST"],
        port=st.secrets['supabase']["DB_PORT"],
        sslmode = 'require'
    )
    return conn.cursor()

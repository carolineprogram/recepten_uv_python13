#This file will handle database connections.
import os
import streamlit as st
import psycopg2
from dotenv import load_dotenv
from supabase import create_client, Client

# zorg dat credentials in .env gelezen kunnen worden
load_dotenv()

# Supabase client
def get_connection():
    #eerst proberen om Streamlit secrets te gebruiken
    try:
        supabase_url = st.secrets['supabase']["SUPABASE_URL"]
        supabase_key = st.secrets['supabase']["SUPABASE_KEY"]
    except Exception: # terugvallen op environment variables (handig voor local development)
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        raise RuntimeError(
            "Supabase URL of key zijn niet beschikbaar via .env of via Streamlit sectrets"
        )

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

def close_psycopg2_connection():
    if conn:
        cursor.close()
        conn.close()


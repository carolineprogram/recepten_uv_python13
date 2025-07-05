#This file will handle database connections and queries.

import streamlit as st
import mysql.connector
from st_supabase_connection import SupabaseConnection

# Initialize connection.
def get_connection():
    # op tommy-server
    # return mysql.connector.connect(**st.secrets["mysql_recepten"])
    # hier op de pc
    # return mysql.connector.connect(**st.secrets["mysql_recepten_lokaal"])
    # op Supabase
    return st.connection("supabase", type=SupabaseConnection)

# Perform query.
# def run_query(query, params=None):
#     try:
#         with get_connection() as conn:
#             with conn.cursor(buffered=True) as cur:
#                 cur.execute(query, params or ())
#                 if query.strip().lower().startswith(('insert', 'update', 'delete')):
#                     conn.commit()
#                     return cur.lastrowid
#                 else:
#                     return cur.fetchall()
#     except Exception as e:
#         print(f"An error occurred: {e}")
def run_query(query, table, data=None, where=None, order=None):
    """
       Executes a query on the Supabase database.

       :param query: Type of query ("select", "insert", "update", "delete").
       :param table: Table name.
       :param data: Data for insertion, update, or selected columns (list or dict).
       :param where: Dictionary of column-value pairs for filtering.
       :param order: Column name for ordering (optional).
       :return: Query result or None if an error occurs.
       """
    #SupabaseConnection does not support the context manager protocol
    # (i.e., it does not have __enter__ and __exit__ methods).
    # This means you cannot use it with a with statement.

    try:
        conn = get_connection()  # Get connection

        q = conn.table(table)  # Initialize table

        if query == "select":
            if isinstance(data, list):
                q = q.select(",".join(data))  # Convert list to string
            else:
                q = q.select("*")  # Default: Select all

            if where:
                for col, val in where.items():
                    q = q.eq(col, val)  # Apply where conditions
            if order:
                q = q.order(order)

            result = q.execute()

        elif query == "insert":
            result = q.insert(data).execute()

        elif query == "update":
            rows = conn.table(tabel).update(dict).eq().execute()
            if not where:
                raise ValueError("Update queries require a 'where' condition.")
            for col, val in where.items():
                q = q.eq(col, val)
            result = q.update(data).execute()

        elif query == "delete":
            if not where:
                raise ValueError("Delete queries require a 'where' condition.")
            for col, val in where.items():
                q = q.eq(col, val)
            result = q.delete().execute()

        else:
            raise ValueError(f"Invalid query type: {query}")

        return result

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

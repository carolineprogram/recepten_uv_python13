
import streamlit as st
from st_supabase_connection import SupabaseConnection

# Initialize connection.
#conn = st.connection("supabase",type=SupabaseConnection)

# Perform query.
#rows = conn.table("recepten_ingredient").select("*").execute()

#Om te kunnen werken op Supabase RLS Row Level Security op de tabel afzetten
# Print results.
#for row in rows.data:
#    st.write(f"{row['ingredient']} has a :{row['type']}:")

def get_connection():
    # op tommy-server
    # return mysql.connector.connect(**st.secrets["mysql_recepten"])
    # hier op de pc
    # return mysql.connector.connect(**st.secrets["mysql_recepten_lokaal"])
    # op Supabase
    return st.connection("supabase", type=SupabaseConnection)

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

def add_recipe():
    added_recipe = fill_in_recipe(form_key="Add Recipe", button_label="Voeg recept toe", recipe_id='', recipe_name='', beschrijving='', bron='', locatie='', gemaakt='')
    st.success(added_recipe)


if __name__ == "__main__":
    result = run_query("select", "recepten_Recepttype", ["type_id", "type"], order="type")
    st.write(result)
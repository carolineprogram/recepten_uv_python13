#This file will handle de hoofdquery run_query.

from db import get_connection

def run_query(query, table, data=None, where=None, order=None, in_table_in_record = None, in_=None):
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
            if in_:
                q = q.in_(in_table_in_record, in_)
            result = q.execute()

        elif query == "insert":
            result = q.insert(data).execute()

        elif query == "update":
            q = q.update(data)
            if not where:
                raise ValueError("Update queries require a 'where' condition.")
            else:
                for col, val in where.items():
                    q = q.eq(col, val)
            result = q.execute()

        elif query == "delete":
            q = q.delete()
            if not where:
                raise ValueError("Delete queries require a 'where' condition.")
            else:
                for col, val in where.items():
                    q = q.eq(col, val)
            result = q.execute()

        else:
            raise ValueError(f"Invalid query type: {query}")

        return result

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
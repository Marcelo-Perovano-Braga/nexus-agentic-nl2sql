import os
import sqlite3
from langchain_core.tools import BaseTool
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from langchain.tools import tool

DB_PATH = 'demodb.db'

@tool("Schema Inspector Tool")
def schema_inspector_tool(table_name: str = '') -> str:
    """
    Inspects the database schema. Provide a table name 
    to see its columns and types, or leave blank to list all tables.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        if not table_name:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            return f"Tables in the database: {[table[0] for table in tables]}"
        else:
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            return f"Columns in table '{table_name}': {[f'{col[1]} ({col[2]})' for col in columns]}"
    finally:
        conn.close()

# Tool for executing SQL queries
@tool("SQL Query Executor Tool")
def sql_query_tool(query: str) -> str:
    """Executes an SQL query on the database and returns the result. Only SELECT queries are permitted."""
    if not query.strip().upper().startswith("SELECT"):
        return "Security Error: This tool only allows read operations (SELECT). For edits, use the appropriate tools."
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return f"Query result: {results}"
    except sqlite3.Error as e:
        return f"Error executing SQL query: {e}"
    finally:
        conn.close()

# Tool for plotting tools
@tool("Data Plotting Tool")
def data_plotting_tool(query: str) -> str:
    """
    Creates a bar chart from database data. The input must be an 
    SQL query that returns exactly two columns: one for labels (X-axis) 
    and one for values (Y-axis).
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(query, conn)
        conn.close()
        if df.shape[1] != 2:
            return "Error: The SQL query must return exactly two columns."
        
        plt.figure(figsize=(10, 6))
        sns.barplot(x=df.columns[0], y=df.columns[1], data=df)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        chart_path = "chart.png"
        plt.savefig(chart_path)
        plt.close()
        return f"Chart successfully created and saved at: {os.path.abspath(chart_path)}"
    except Exception as e:
        return f"Error creating chart: {e}"

# Tool for editing the database
@tool("Database Editor Tool")
def data_editor_tool(table_name: str, column_to_update: str, new_value: str, record_id: int) -> str:
    """
    Updates a specific record in a table. Requires four arguments: 
    table_name, column_to_update, new_value, and record_id.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query = f"UPDATE {table_name} SET {column_to_update} = ? WHERE id = ?"
        cursor.execute(query, (new_value, record_id))
        conn.commit()
        if cursor.rowcount == 0:
            return f"Error: No record found with id={record_id} in table '{table_name}'."
        return f"Success: Record with id={record_id} in table '{table_name}' was successfully updated."
    except sqlite3.Error as e:
        return f"Error updating record: {e}"
    finally:
        conn.close()

# Tool for inserting Data
@tool("Data Inserter Tool")
def data_inserter_tool(file_name: str, type: str, creation_date: str, summary: str) -> str:
    """
    Adds a new record to the 'documents' table. Requires four arguments: 
    file_name, type, creation_date (in YYYY-MM-DD format), and summary.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query = "INSERT INTO documents (file_name, type, creation_date, summary) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (file_name, type, creation_date, summary))
        conn.commit()
        return f"Success: A new record was added to the 'documents' table with ID {cursor.lastrowid}."
    except sqlite3.Error as e:
        return f"Error inserting record: {e}"
    finally:
        conn.close()

# Tool for deleting Data
@tool("Data Deleter Tool")
def data_deleter_tool(record_id: int) -> str:
    """
    Deletes a specific record from the 'documents' table using its ID. 
    The input must be the ID (integer) of the record to be deleted.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query = "DELETE FROM documents WHERE id = ?"
        cursor.execute(query, (record_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return f"Error: No record found with ID={record_id}."
        return f"Success: The record with ID={record_id} was deleted."
    except sqlite3.Error as e:
        return f"Error deleting record: {e}"
    finally:
        conn.close()
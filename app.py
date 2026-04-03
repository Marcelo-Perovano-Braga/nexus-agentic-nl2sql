from dotenv import load_dotenv
load_dotenv()

from faker import Faker
import random
import streamlit as st
import pandas as pd
import sqlite3
import os
from crewai import Crew, Process
from tasks import (
    edit_database_task, verify_edit_task, data_extraction_task,
    data_visualization_task, insert_data_task, delete_data_task,
)
from agents import (
    database_editor_agent, data_verifier_agent, database_specialist_agent,
    data_visualization_agent, data_inserter_agent, data_deleter_agent,
)
DB_PATH = 'demodb.db'

# --- BOOTSTRAP ROUTINE ---
@st.cache_resource
def init_db():
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 1. Ensure the schema exists (English schema)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_name TEXT NOT NULL,
                type TEXT NOT NULL,
                creation_date TEXT NOT NULL,
                summary TEXT
            )
        ''')
        
        # 2. Check if the table is empty
        cursor.execute("SELECT COUNT(*) FROM documents")
        count = cursor.fetchone()[0]
        
        # 3. Seed data ONLY if the database is empty.
        if count == 0:
            st.sidebar.info("System Initializing: Provisioning 50 synthetic records...")
            fake = Faker('en_US')
            example_documents = []
            document_types = ['Report', 'Presentation', 'Feedback', 'Contract', 'Spreadsheet', 'Manual']

            for _ in range(50):
                file_name = f"{fake.word()}_{fake.word()}_{random.randint(2022, 2025)}.{fake.random_element(elements=('pdf', 'docx', 'txt', 'xlsx'))}"
                doc_type = fake.random_element(elements=document_types)
                creation_date = fake.date_between(start_date='-3y', end_date='today').strftime('%Y-%m-%d')
                summary = fake.paragraph(nb_sentences=3)
                example_documents.append((file_name, doc_type, creation_date, summary))

            cursor.executemany(
                'INSERT INTO documents (file_name, type, creation_date, summary) VALUES (?,?,?,?)',
                example_documents
            )
            conn.commit()
            
    except Exception as e:
        st.sidebar.error(f"System Warning: Database initialization failed - {e}")
    finally:
        if conn:
            conn.close()

# Execute the bootstrap routine
init_db()

def get_database_schema(db_path='demodb.db'):
    """Extracts the exact database structure (DDL) for the LLM."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    schemas = cursor.fetchall()
    conn.close()
    return "\n\n".join([schema[0] for schema in schemas if schema[0]])

# Dashboard
def show_dashboard():
    st.subheader("📊 Database Dashboard")
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM documents", conn)
        conn.close()

        total_records = len(df)
        doc_types = df['type'].value_counts()

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Documents", total_records)
        with col2:
            st.metric("Distinct Document Types", len(doc_types))

        st.write("#### Count by Document Type")
        st.bar_chart(doc_types)

        st.write("#### Data Sample")
        st.dataframe(df.head(10))

    except Exception as e:
        st.error(f"Could not load the dashboard: {e}")

# Running Function
def run_crew_and_display_results(crew, inputs):
    with st.spinner("Agents are working... This may take a moment."):
        result = crew.kickoff(inputs=inputs)

    st.divider()
    st.subheader("✅ Final Crew Response:")
    st.markdown(result)

    if "chart.png" in str(result) and os.path.exists("chart.png"):
        st.image("chart.png")

# Page Layout
st.set_page_config(page_title="CrewAI Database Manager", page_icon="🤖", layout="wide")

# Sidebar
with st.sidebar:
    st.title("🤖 N.E.X.U.S")
    st.markdown(
        "Welcome to NEXUS! An AI crew capable of interacting "
        "with a database using natural language."
    )
    st.divider()
    app_mode = st.radio(
        "Choose an Action:",
        ["Dashboard", "Smart Search", "Manage Records"]
    )
    st.divider()
    st.markdown("### Developed by Marcelo P. Braga")

# Web Navigation
if app_mode == "Dashboard":
    show_dashboard()

elif app_mode == "Smart Search":
    st.header("❓ Smart Search & Data Visualization")

    question = st.text_input(
        "Describe the information or chart you are looking for:",
        placeholder="Ex: 'List the 5 most recent reports' or 'create a bar chart of counts by type'"
    )

    if st.button("Execute Search"):
        if not question:
            st.warning("Please enter a question.")
        else:
            schema_string = get_database_schema(DB_PATH)
            
            if "chart" in question.lower() or "plot" in question.lower() or "graph" in question.lower():
                st.write("Initializing data visualization crew...")
                crew = Crew(
                    agents=[database_specialist_agent, data_visualization_agent],
                    tasks=[data_extraction_task, data_visualization_task],
                    process=Process.sequential,
                    verbose=2,
                    telemetry=False
                )
            else:
                st.write("Initializing N.E.X.U.S processing...")
                crew = Crew(
                    agents=[database_specialist_agent],
                    tasks=[data_extraction_task],
                    verbose=2,
                    telemetry=False
                )

            inputs = {
                'question': question,
                'schema_context': schema_string
            }

            run_crew_and_display_results(crew, inputs)

elif app_mode == "Manage Records":
    st.header("✍️ Add, Edit, or Delete Records")

    tab1, tab2, tab3 = st.tabs(["Add Record", "Edit Record", "Delete Record"])

    with tab1:
        st.subheader("Add New Document")
        with st.form("add_form"):
            file_name = st.text_input("File Name")
            doc_type = st.text_input("Document Type")
            creation_date = st.date_input("Creation Date")
            summary = st.text_area("Content Summary")
            submitted_add = st.form_submit_button("Add Record")

            if submitted_add:
                inputs = {'file_name': file_name, 'type': doc_type, 'creation_date': creation_date.strftime('%Y-%m-%d'), 'summary': summary}
                crew = Crew(
                    agents=[data_inserter_agent],
                    tasks=[insert_data_task],
                    verbose=2,
                    telemetry=False
                )
                run_crew_and_display_results(crew, inputs)

    with tab2:
        st.subheader("Edit an Existing Record")
        st.info("Tip: Use the 'Smart Search' to find the ID and column name of the record you want to change.")
        with st.form("edit_form"):
            record_id = st.number_input("ID of the record to change", min_value=1, step=1)
            column = st.text_input("Column name to change")
            new_value = st.text_input("New value for the column")
            submitted_edit = st.form_submit_button("Edit Record")

            if submitted_edit:
                edit_inputs = {'table_name': 'documents', 'record_id': int(record_id), 'column_to_update': column, 'new_value': new_value}
                edit_crew = Crew(
                    agents=[database_editor_agent, data_verifier_agent],
                    tasks=[edit_database_task, verify_edit_task],
                    process=Process.sequential,
                    verbose=2,
                    telemetry=False
                )
                run_crew_and_display_results(edit_crew, edit_inputs)

    with tab3:
        st.subheader("Delete a Record")
        st.warning("WARNING: This action is irreversible.")
        with st.form("delete_form"):
            record_id_del = st.number_input("ID of the record to delete", min_value=1, step=1)
            
            confirm_delete = st.checkbox("I understand the consequences and confirm the deletion of this record.")
            
            submitted_del = st.form_submit_button("Delete Record")

            if submitted_del:
                if confirm_delete:
                    crew = Crew(
                        agents=[data_deleter_agent],
                        tasks=[delete_data_task],
                        verbose=2,
                        telemetry=False
                    )
                    run_crew_and_display_results(crew, {'record_id': int(record_id_del)})
                else:
                    st.error("You must check the confirmation box to delete a record.")
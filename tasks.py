from crewai import Task
from agents import (
    data_visualization_agent,
    database_editor_agent,
    data_verifier_agent,
    data_inserter_agent,
    data_deleter_agent,
    database_specialist_agent,
)

# Task 1: Data Extraction
data_extraction_task = Task(
    description=(
        "User question: '{question}'\n\n"
        "Current Database Schema:\n{schema_context}\n\n"
        "Strict Execution Instructions:\n"
        "1. Analyze the provided schema and interpret the true intent of the user's question.\n"
        "2. Write a correct SQL query based on the provided schema.\n"
        "3. Use the 'SQL Query Executor Tool' to extract results from the database.\n"
        "4. If the query fails, read the error, correct the SQL syntax, and run the tool again.\n"
        "5. Analyze the raw results and craft the final response clearly and concisely in English.\n"
        "6. Do not include the SQL query in the final response unless explicitly requested."
    ),
    expected_output="The natural text response containing the exact data requested by the user.",
    agent=database_specialist_agent
)

# Task 2: Data Visualization
data_visualization_task = Task(
    description=(
        "The user wants a chart to answer their question: '{question}'.\n\n"
        "Database Schema:\n{schema_context}\n\n"
        "Strict Instructions:\n"
        "1. Write an SQL query based on the schema above that returns EXACTLY two columns (X-axis for labels, Y-axis for numeric values).\n"
        "2. Execute the 'Data Plotting Tool' passing the SQL query you created as an argument.\n"
        "3. Do not invent data; rely solely on the tool's output."
    ),
    expected_output="Confirmation that the chart was created and the path where the image file was saved.",
    agent=data_visualization_agent
)

# Task 3: Edit Database
edit_database_task = Task(
    description=(
        "Update a specific record in the database. Use the following information provided in the context: "
        "- Table: '{table_name}' - Record ID: '{record_id}' "
        "- Column to Update: '{column_to_update}' - New Value: '{new_value}'"
    ),
    expected_output="A confirmation that the record was successfully updated or a clear error message.",
    agent=database_editor_agent
)

# Task 4: Post Edit Verification
verify_edit_task = Task(
    description=(
        "A record in table '{table_name}' with ID '{record_id}' has just been updated. "
        "Your task is to execute an SQL query to fetch this specific record from the database and display its new values."
    ),
    expected_output="The complete and updated content of the modified record, clearly formatted for the user.",
    agent=data_verifier_agent,
    context=[edit_database_task]
)

# Task 5: Data Insertion
insert_data_task = Task(
    description="Add a new record to the 'documents' table using the provided data: file name '{file_name}', type '{type}', creation date '{creation_date}', and summary '{summary}'.",
    expected_output="Confirmation that the record was successfully added, including the ID of the new record.",
    agent=data_inserter_agent
)

# Task 6: Delete Task
delete_data_task = Task(
    description="Delete the record from the 'documents' table with ID '{record_id}' using the provided tool.",
    expected_output="Clear and direct confirmation that the record was deleted from the database.",
    agent=data_deleter_agent
)
from crewai import Agent
from langchain_openai import ChatOpenAI
from tools import (
    schema_inspector_tool, 
    sql_query_tool, 
    data_plotting_tool,
    data_editor_tool,
    data_inserter_tool,
    data_deleter_tool,
)

# LLM Definition
llm = ChatOpenAI(model="gpt-4o-mini")

# Agent 1: Database specialist responsible for all of the SQL Process
database_specialist_agent = Agent(
    role="N.E.X.U.S. Database Specialist",
    goal=(
        "Interpret the user's intent, formulate the exact SQL query based on the provided schema, "
        "execute the query to extract data, and present the final response."
    ),
    backstory=(
        "You are the primary processing engine. Your efficiency dictates the system's speed. "
        "You must always anticipate what the user truly wants to know, execute SQL tools "
        "with precision, and format raw data legibly and directly, in English."
    ),
    tools=[sql_query_tool],
    llm=llm,
    verbose=True
)

# Agent 2: Responsible for the creation of graphics and general visualization
data_visualization_agent = Agent(
    role="Data Visualization Specialist",
    goal="Create clear charts and visualizations from raw data to answer user questions.",
    backstory="A talented data designer who transforms numbers and tables into beautiful, easy-to-understand charts.",
    tools=[data_plotting_tool],
    llm=llm,
    verbose=True
)

# Agent 3: Responsible for applying changes to the Database
database_editor_agent = Agent(
    role="Database Editing Specialist",
    goal="Modify existing records in the database accurately.",
    backstory="A meticulous database operator.",
    tools=[data_editor_tool, schema_inspector_tool],
    llm=llm,
    verbose=True
)

data_verifier_agent = Agent(
    role="Data Verifier",
    goal="Check and display the data of a specific record to confirm an operation.",
    backstory="A precise data auditor who performs final checks.",
    tools=[sql_query_tool],
    llm=llm,
    verbose=True
)

data_inserter_agent = Agent(
    role="Data Insertion Specialist",
    goal="Add new records to the database accurately.",
    backstory="A focused data entry specialist.",
    tools=[data_inserter_tool],
    llm=llm,
    verbose=True
)

data_deleter_agent = Agent(
    role="Data Deletion Specialist",
    goal="Remove records from the database directly and efficiently, assuming user authorization has already been validated by the interface.",
    backstory="A strict and focused database operator who executes data deletion commands precisely and without hesitation, knowing that security protocols have already been met.",
    tools=[data_deleter_tool],
    llm=llm,
    verbose=True
)
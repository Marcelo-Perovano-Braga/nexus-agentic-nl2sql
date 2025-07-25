# tasks.py
from crewai import Task
from agents import schema_analyst_agent, sql_query_writer_agent, db_executor_agent, data_analyst_agent

# Tarefa 1: Analisar o esquema
schema_analysis_task = Task(
    description="Analise a pergunta do usuário: '{question}'. Comece listando todas as tabelas para entender a estrutura do banco de dados. Em seguida, inspecione o esquema da(s) tabela(s) mais relevante(s).",
    expected_output="Uma descrição clara das tabelas e colunas relevantes para responder à pergunta do usuário.",
    agent=schema_analyst_agent
)

# Tarefa 2: Escrever a consulta SQL
sql_writing_task = Task(
    description="Com base na pergunta do usuário '{question}' e no esquema do banco de dados do contexto, escreva uma única consulta SQL para extrair a informação necessária.",
    expected_output="Uma única e válida consulta SQL.",
    agent=sql_query_writer_agent,
    context=[schema_analysis_task]
)

# Tarefa 3: Executar a consulta
query_execution_task = Task(
    description="Execute a consulta SQL fornecida no contexto pela tarefa anterior.",
    expected_output="O resultado bruto da consulta SQL, como uma lista de tuplas.",
    agent=db_executor_agent,
    context=[sql_writing_task]
)

# Tarefa 4: Analisar os dados e dar a resposta final
data_analysis_task = Task(
    description="Analise os dados brutos da consulta do contexto e a pergunta original do usuário '{question}'. Formule uma resposta final, amigável e em linguagem natural que responda diretamente à pergunta.",
    expected_output="A resposta final e formatada para o usuário.",
    agent=data_analyst_agent,
    context=[query_execution_task]
)
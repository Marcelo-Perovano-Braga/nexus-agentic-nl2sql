from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import pandas as pd
import sqlite3
import os
from crewai import Crew, Process
from tasks import (
    schema_analysis_task, sql_writing_task, query_execution_task,
    data_analysis_task, edit_database_task, verify_edit_task,
    data_visualization_task, insert_data_task, delete_data_task,
    query_optimization_task, translation_task
)
from agents import (
    schema_analyst_agent, sql_query_writer_agent, db_executor_agent,
    data_analyst_agent, database_editor_agent, data_verifier_agent,
    data_visualization_agent, data_inserter_agent, data_deleter_agent,
    query_optimizer_agent, translator_agent
)

DB_PATH = 'demodb.db'

#Dashboard
def show_dashboard():
    st.subheader("📊 Dashboard do Banco de Dados")
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM documentos", conn)
        conn.close()

        total_records = len(df)
        doc_types = df['tipo'].value_counts()

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total de Documentos", total_records)
        with col2:
            st.metric("Tipos de Documentos Diferentes", len(doc_types))

        st.write("#### Contagem por Tipo de Documento")
        st.bar_chart(doc_types)

        st.write("#### Amostra dos Dados")
        st.dataframe(df.head(10))

    except Exception as e:
        st.error(f"Não foi possível carregar o dashboard: {e}")

#Função de Execução
def run_crew_and_display_results(crew, inputs):
    with st.spinner("Agentes trabalhando... Isso pode levar um momento."):
        result = crew.kickoff(inputs=inputs)

    st.divider()
    st.subheader("✅ Resposta Final da Equipe:")
    st.markdown(result)

    if "chart.png" in str(result) and os.path.exists("chart.png"):
        st.image("chart.png")

#Layout da página
st.set_page_config(page_title="CrewAI Database Manager", page_icon="🤖", layout="wide")

#Barra lateral
with st.sidebar:
    st.title("🤖 N.E.X.U.S")
    st.markdown(
        "Bem vindo ao NEXUS! Uma tripulação de I.A que é "
        "capaz de interagir com um banco de dados usando linguagem natural."
    )
    st.divider()
    app_mode = st.radio(
        "Escolha uma Ação:",
        ["Dashboard", "Busca Inteligente", "Gerenciar Registros"]
    )
    st.divider()
    st.markdown("### Desenvolvido por Marcelo P. Braga")


#Navegação

if app_mode == "Dashboard":
    show_dashboard()

elif app_mode == "Busca Inteligente":
    st.header("❓ Busca Inteligente e Visualização de Dados")

    question = st.text_input(
        "Descreva a informação ou o gráfico que você procura:",
        placeholder="Ex: 'Liste os 5 relatórios mais recentes' ou 'crie um gráfico de barras da contagem por tipo'"
    )

    if st.button("Executar Busca"):
        if not question:
            st.warning("Por favor, digite uma pergunta.")
        else:
            optimizer_crew = Crew(
                agents=[query_optimizer_agent],
                tasks=[query_optimization_task],
                verbose=1,
                telemetry=False
            )
            st.write("Otimizando sua pergunta...")
            with st.spinner("Agente otimizador pensando..."):
                optimized_question = optimizer_crew.kickoff(inputs={'question': question})
            st.success(f"Pergunta Otimizada: {optimized_question}")

            if "gráfico" in optimized_question.lower() or "visualização" in optimized_question.lower():
                st.write("Iniciando equipe de visualização de dados...")
                crew = Crew(
                    agents=[schema_analyst_agent, sql_query_writer_agent, data_visualization_agent],
                    tasks=[schema_analysis_task, sql_writing_task, data_visualization_task],
                    process=Process.sequential,
                    verbose=2,
                    telemetry=False
                )
            else:
                st.write("Iniciando equipe de busca de dados...")
                crew = Crew(
                    agents=[schema_analyst_agent, sql_query_writer_agent, db_executor_agent, data_analyst_agent, translator_agent],
                    tasks=[schema_analysis_task, sql_writing_task, query_execution_task, data_analysis_task, translation_task],
                    process=Process.sequential,
                    verbose=2,
                    telemetry=False
                )

            run_crew_and_display_results(crew, {'question': optimized_question})


elif app_mode == "Gerenciar Registros":
    st.header("✍️ Adicionar, Editar ou Deletar Registros")

    tab1, tab2, tab3 = st.tabs(["Adicionar Registro", "Editar Registro", "Deletar Registro"])

    with tab1:
        st.subheader("Adicionar Novo Documento")
        with st.form("add_form"):
            nome = st.text_input("Nome do arquivo")
            tipo = st.text_input("Tipo de documento")
            data = st.date_input("Data de criação")
            resumo = st.text_area("Resumo do conteúdo")
            submitted_add = st.form_submit_button("Adicionar Registro")

            if submitted_add:
                inputs = {'nome_arquivo': nome, 'tipo': tipo, 'data_criacao': data.strftime('%Y-%m-%d'), 'resumo': resumo}
                crew = Crew(
                    agents=[data_inserter_agent],
                    tasks=[insert_data_task],
                    verbose=2,
                    telemetry=False
                )
                run_crew_and_display_results(crew, inputs)

    with tab2:
        st.subheader("Editar um Registro Existente")
        st.info("Dica: Use a 'Busca Inteligente' para encontrar o ID e o nome da coluna do registro que deseja alterar.")
        with st.form("edit_form"):
            record_id = st.number_input("ID do registro a ser alterado", min_value=1, step=1)
            column = st.text_input("Nome da coluna a ser alterada")
            new_value = st.text_input("Novo valor para a coluna")
            submitted_edit = st.form_submit_button("Editar Registro")

            if submitted_edit:
                edit_inputs = {'table_name': 'documentos', 'record_id': int(record_id), 'column_to_update': column, 'new_value': new_value}
                edit_crew = Crew(
                    agents=[database_editor_agent, data_verifier_agent],
                    tasks=[edit_database_task, verify_edit_task],
                    process=Process.sequential,
                    verbose=2,
                    telemetry=False
                )
                run_crew_and_display_results(edit_crew, edit_inputs)

    with tab3:
        st.subheader("Deletar um Registro")
        st.warning("CUIDADO: Esta ação é irreversível.")
        with st.form("delete_form"):
            record_id_del = st.number_input("ID do registro a ser deletado", min_value=1, step=1)
            submitted_del = st.form_submit_button("Deletar Registro")

            if submitted_del:
                crew = Crew(
                    agents=[data_deleter_agent],
                    tasks=[delete_data_task],
                    verbose=2,
                    telemetry=False
                )
                run_crew_and_display_results(crew, {'record_id': int(record_id_del)})
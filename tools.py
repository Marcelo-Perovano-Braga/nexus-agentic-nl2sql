# tools.py (Corrected and Simplified)

import os
import sqlite3
from langchain_core.tools import BaseTool
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from langchain.tools import tool
from langchain_community.tools import HumanInputRun

DB_PATH = 'demodb.db'

# --- Ferramenta para Inspecionar o Esquema do Banco de Dados ---
# This is the only version you need. It's simple and correct.
@tool("Schema Inspector Tool")
def schema_inspector_tool(table_name: str = '') -> str:
    """
    Inspeciona o esquema do banco de dados. Forneça o nome de uma tabela 
    para ver suas colunas e tipos, ou deixe em branco para listar todas as tabelas.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        if not table_name:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            return f"Tabelas no banco de dados: {[table[0] for table in tables]}"
        else:
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            return f"Colunas na tabela '{table_name}': {[f'{col[1]} ({col[2]})' for col in columns]}"
    finally:
        conn.close()

# --- Ferramenta para Executar Consultas SQL ---
@tool("SQL Query Executor Tool")
def sql_query_tool(query: str) -> str:
    """Executa uma consulta SQL no banco de dados e retorna o resultado."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return f"Resultado da consulta: {results}"
    except sqlite3.Error as e:
        return f"Erro ao executar a consulta SQL: {e}"
    finally:
        conn.close()

# --- Ferramenta para Plotar Gráficos ---
@tool("Data Plotting Tool")
def data_plotting_tool(query: str) -> str:
    """
    Cria um gráfico de barras a partir de dados do banco de dados. A entrada deve ser uma 
    consulta SQL que retorne exatamente duas colunas: uma para os rótulos (eixo X) 
    e uma para os valores (eixo Y).
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(query, conn)
        conn.close()
        if df.shape[1] != 2:
            return "Erro: A consulta SQL deve retornar exatamente duas colunas."
        
        plt.figure(figsize=(10, 6))
        sns.barplot(x=df.columns[0], y=df.columns[1], data=df)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        chart_path = "chart.png"
        plt.savefig(chart_path)
        plt.close()
        return f"Gráfico criado com sucesso e salvo em: {os.path.abspath(chart_path)}"
    except Exception as e:
        return f"Erro ao criar o gráfico: {e}"

# --- Ferramenta para Editar o Banco de Dados ---
@tool("Database Editor Tool")
def data_editor_tool(table_name: str, column_to_update: str, new_value: str, record_id: int) -> str:
    """
    Atualiza um registro específico em uma tabela. Requer quatro argumentos: 
    table_name, column_to_update, new_value, e record_id.
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

# --- Ferramenta para Inserir Dados ---
@tool("Data Inserter Tool")
def data_inserter_tool(nome_arquivo: str, tipo: str, data_criacao: str, resumo: str) -> str:
    """
    Adiciona um novo registro na tabela 'documentos'. Requer quatro argumentos: 
    nome_arquivo, tipo, data_criacao (no formato YYYY-MM-DD), e resumo.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query = "INSERT INTO documentos (nome_arquivo, tipo, data_criacao, resumo) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (nome_arquivo, tipo, data_criacao, resumo))
        conn.commit()
        return f"Sucesso: Um novo registro foi adicionado à tabela 'documentos' com o ID {cursor.lastrowid}."
    except sqlite3.Error as e:
        return f"Erro ao inserir o registro: {e}"
    finally:
        conn.close()

# --- Ferramenta para Deletar Dados ---
@tool("Data Deleter Tool")
def data_deleter_tool(record_id: int) -> str:
    """
    Deleta um registro específico da tabela 'documentos' usando seu ID. 
    A entrada deve ser o ID (inteiro) do registro a ser deletado.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query = "DELETE FROM documentos WHERE id = ?"
        cursor.execute(query, (record_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return f"Erro: Nenhum registro encontrado com o ID={record_id}."
        return f"Sucesso: O registro com ID={record_id} foi deletado."
    except sqlite3.Error as e:
        return f"Erro ao deletar o registro: {e}"
    finally:
        conn.close()

# --- Ferramenta para Interação Humana ---        
human_tool = HumanInputRun()
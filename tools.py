# tools.py
import os
import sqlite3
from typing import Type, Optional
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

DB_PATH = 'demodb.db'

# --- Ferramenta para Inspecionar o Esquema do Banco de Dados (VERSÃO CORRIGIDA) ---

# 1. Crie a classe de Input para definir os argumentos
class SchemaInspectorInput(BaseModel):
    table_name: Optional[str] = Field(None, description="O nome da tabela para ver suas colunas. Deixe em branco para listar todas as tabelas.")

class SchemaInspectorTool(BaseTool):
    name: str = "Schema Inspector Tool"
    description: str = "Use esta ferramenta para inspecionar o esquema. Para listar tabelas, não passe argumentos. Para ver as colunas de uma tabela, passe o nome dela como 'table_name'."
    args_schema: Type[BaseModel] = SchemaInspectorInput

    def _run(self, table_name: Optional[str] = None) -> str:
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            if not table_name:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                return f"Tabelas no banco de dados: {[table[0] for table in tables]}"
            else:
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = cursor.fetchall()
                
                # MUDANÇA: Agora formatamos o nome da coluna E o tipo de dado
                # O resultado de PRAGMA table_info é (id, nome, tipo, ...)
                # Nós pegamos o item 1 (nome) e o item 2 (tipo)
                formatted_columns = [f"{col[1]} ({col[2]})" for col in columns]
                
                return f"Colunas na tabela '{table_name}': {formatted_columns}"
        except sqlite3.Error as e:
            return f"Erro ao inspecionar o esquema: {e}"
        finally:
            conn.close()

# --- Ferramenta para Executar Consultas SQL ---
class SQLQueryExecutorTool(BaseTool):
    name: str = "SQL Query Executor Tool"
    description: str = "Use esta ferramenta para executar uma consulta SQL no banco de dados e retornar o resultado."

    def _run(self, query: str) -> str:
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

class SQLQueryInput(BaseModel):
    query: str = Field(description="A consulta SQL completa a ser executada.")

class DataPlottingTool(BaseTool):
    name: str = "Data Plotting Tool"
    description: str = "Use esta ferramenta para criar um gráfico de barras a partir de dados do banco de dados. A entrada deve ser uma consulta SQL que retorne exatamente duas colunas: uma para os rótulos (eixo X) e uma para os valores (eixo Y)."
    args_schema: Type[BaseModel] = SQLQueryInput # Reutilizando o Input da SQLQueryTool

    def _run(self, query: str) -> str:
        try:
            conn = sqlite3.connect(DB_PATH)
            df = pd.read_sql_query(query, conn)
            conn.close()

            if df.shape[1] != 2:
                return "Erro: A consulta SQL deve retornar exatamente duas colunas."
            
            # Renomeia as colunas para clareza no gráfico
            df.columns = ['rótulos', 'valores']

            plt.figure(figsize=(10, 6))
            plot = sns.barplot(x='rótulos', y='valores', data=df)
            plt.xticks(rotation=45, ha='right')
            plt.title("Visualização dos Dados")
            plt.xlabel(df.columns[0].replace('_', ' ').title())
            plt.ylabel(df.columns[1].replace('_', ' ').title())
            plt.tight_layout()

            chart_path = "chart.png"
            plt.savefig(chart_path)
            plt.close() # Fecha a figura para liberar memória
            
            # Usa os.path.abspath que agora funcionará
            return f"Gráfico criado com sucesso e salvo em: {os.path.abspath(chart_path)}"
        except Exception as e:
            return f"Erro ao criar o gráfico: {e}"


# --- Instanciando as ferramentas ---
schema_inspector_tool = SchemaInspectorTool()
sql_query_tool = SQLQueryExecutorTool()
data_plotting_tool = DataPlottingTool()
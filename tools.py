# tools.py
import sqlite3
from typing import Type, Optional
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

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

# --- Instanciando as ferramentas ---
schema_inspector_tool = SchemaInspectorTool()
sql_query_tool = SQLQueryExecutorTool()
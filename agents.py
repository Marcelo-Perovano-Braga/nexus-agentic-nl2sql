# agents.py
from crewai import Agent
from langchain_openai import ChatOpenAI
from tools import schema_inspector_tool, sql_query_tool
from tools import data_plotting_tool

# Definindo o LLM para todos os agentes
llm = ChatOpenAI(model="gpt-4o-mini")

# Agente 1: Analista de Esquema
schema_analyst_agent = Agent(
    role="Analista de Esquema de Banco de Dados",
    goal="Entender a estrutura do banco de dados, identificando tabelas e colunas relevantes para a pergunta do usuário.",
    backstory="Um especialista em engenharia de dados que consegue mapear qualquer banco de dados e entender como as informações estão organizadas.",
    tools=[schema_inspector_tool],
    llm=llm,
    verbose=True
)

# Agente 2: Engenheiro de Queries SQL
sql_query_writer_agent = Agent(
    role="Engenheiro de Queries SQL",
    goal="Escrever consultas SQL perfeitas e otimizadas com base em uma pergunta em linguagem natural e no esquema do banco de dados.",
    backstory="Um mestre em SQL que transforma qualquer pergunta em uma consulta precisa para extrair os dados corretos.",
    llm=llm,
    verbose=True
)

# Agente 3: Executor de Banco de Dados
db_executor_agent = Agent(
    role="Executor de Banco de Dados",
    goal="Executar consultas SQL no banco de dados de forma segura e eficiente.",
    backstory="Um executor robótico que pega uma consulta SQL e a executa sem questionar, retornando os dados brutos.",
    tools=[sql_query_tool],
    llm=llm,
    verbose=True
)

# Agente 4: Analista de Dados
data_analyst_agent = Agent(
    role="Analista de Dados",
    goal="Analisar os dados brutos retornados pelo banco de dados e transformá-los em uma resposta clara e compreensível para o usuário.",
    backstory="Um analista de dados e comunicador que transforma tabelas e números em insights e respostas em linguagem natural.",
    llm=llm,
    verbose=True
)

data_visualization_agent = Agent(
    role="Especialista em Visualização de Dados",
    goal="Criar gráficos e visualizações claras a partir de dados brutos para responder a perguntas do usuário.",
    backstory="Um designer de dados talentoso que transforma números e tabelas em gráficos bonitos e fáceis de entender.",
    tools=[data_plotting_tool],
    llm=llm,
    verbose=True
)
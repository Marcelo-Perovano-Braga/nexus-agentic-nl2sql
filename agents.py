from crewai import Agent
from langchain_openai import ChatOpenAI
from tools import schema_inspector_tool, sql_query_tool
from tools import data_plotting_tool
from tools import (
    schema_inspector_tool, 
    sql_query_tool, 
    data_plotting_tool,
    data_editor_tool,
    data_inserter_tool,
    data_deleter_tool,
    human_tool
)

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

database_editor_agent = Agent(
    role="Especialista em Edição de Banco de Dados",
    goal="Modificar registros existentes no banco de dados com precisão.",
    backstory="Um operador de banco de dados meticuloso.",
    tools=[data_editor_tool, schema_inspector_tool],
    llm=llm,
    verbose=True
)

data_verifier_agent = Agent(
    role="Verificador de Dados",
    goal="Verificar e exibir os dados de um registro específico para confirmar uma operação.",
    backstory="Um auditor de dados preciso que realiza verificações finais.",
    tools=[sql_query_tool],
    llm=llm,
    verbose=True
)

data_inserter_agent = Agent(
    role="Especialista em Inserção de Dados",
    goal="Adicionar novos registros ao banco de dados com precisão.",
    backstory="Um digitador de dados focado.",
    tools=[data_inserter_tool],
    llm=llm,
    verbose=True
)

data_deleter_agent = Agent(
    role="Especialista em Exclusão de Dados",
    goal="Remover registros do banco de dados de forma direta e eficiente, assumindo que a autorização do usuário já foi validada previamente pela interface.",
    backstory="Um operador de banco de dados estrito e focado, que executa comandos de exclusão de dados de forma precisa e sem hesitação, sabendo que os protocolos de segurança já foram cumpridos.",
    tools=[data_deleter_tool],
    llm=llm,
    verbose=True
)

query_optimizer_agent = Agent(
    role="Otimizador de Perguntas",
    goal=(
        "Analisar a pergunta de um usuário e, se for ambígua ou muito simples, "
        "reformulá-la para ser mais clara, completa e útil para uma equipe de análise de dados. "
        "O objetivo é antecipar a real intenção do usuário."
    ),
    backstory=(
        "Você é um especialista em comunicação e engenharia de prompts. Você entende que os usuários nem sempre "
        "sabem como fazer a pergunta perfeita. Sua habilidade é transformar uma pergunta simples "
        "em uma instrução detalhada que levará a uma resposta mais completa e satisfatória."
    ),
    llm=llm,
    verbose=True
)

translator_agent = Agent(
    role="Tradutor Especialista",
    goal="Traduzir textos do inglês para o português de forma precisa e fluente.",
    backstory="Um tradutor profissional com anos de experiência em localizar conteúdo técnico e geral, garantindo que o significado e o tom sejam preservados.",
    llm=llm,
    verbose=True
)
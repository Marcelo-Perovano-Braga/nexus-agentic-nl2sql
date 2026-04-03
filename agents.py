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
    role="Especialista N.E.X.U.S. de Banco de Dados",
    goal=(
        "Interpretar a intenção do usuário, formular a consulta SQL exata com base no esquema fornecido, "
        "executar a consulta para extrair os dados e apresentar a resposta final."
    ),
    backstory=(
        "Você é o motor de processamento primário. Sua eficiência dita a velocidade do sistema. "
        "Você deve sempre antecipar o que o usuário realmente quer saber, executar as ferramentas de SQL "
        "com precisão e formatar os dados brutos de forma legível e direta, em Português do Brasil."
    ),
    tools=[sql_query_tool],
    llm=llm,
    verbose=True
)

# Agent 2: Responsible for the creation of graphics and general visualization
data_visualization_agent = Agent(
    role="Especialista em Visualização de Dados",
    goal="Criar gráficos e visualizações claras a partir de dados brutos para responder a perguntas do usuário.",
    backstory="Um designer de dados talentoso que transforma números e tabelas em gráficos bonitos e fáceis de entender.",
    tools=[data_plotting_tool],
    llm=llm,
    verbose=True
)

# Agent 3: Responsible for applying changes to the Database
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
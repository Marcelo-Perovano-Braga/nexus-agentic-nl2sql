# tasks.py
from crewai import Task
from agents import schema_analyst_agent, sql_query_writer_agent, db_executor_agent, data_analyst_agent, data_visualization_agent
from agents import (
    schema_analyst_agent, 
    sql_query_writer_agent, 
    db_executor_agent, 
    data_analyst_agent,
    data_visualization_agent,
    database_editor_agent,
    data_verifier_agent,
    data_inserter_agent,
    data_deleter_agent,
    query_optimizer_agent,
    translator_agent
)

# Tarefa 1: Analisar o esquema
schema_analysis_task = Task(
    description=(
        "Analise a pergunta do usuário: '{question}'. Sua única função é identificar e descrever a estrutura "
        "das tabelas relevantes para a pergunta. Use a 'Schema Inspector Tool' para listar as tabelas e depois "
        "inspecionar as colunas da tabela principal. Não tente analisar os dados ou valores dentro das colunas."
    ),
    expected_output="Uma descrição clara das tabelas e colunas (com seus tipos de dados) relevantes para responder à pergunta do usuário.",
    agent=schema_analyst_agent
)

# Tarefa 2: Escrever a consulta SQL
sql_writing_task = Task(
    description=(
        "Com base na pergunta do usuário '{question}' e no esquema do banco de dados do contexto, "
        "escreva uma única e precisa consulta SQL para extrair a informação necessária. "
        "Depois de formular a consulta, forneça-a como sua 'Final Answer' imediatamente."
    ),
    expected_output="Uma única e válida consulta SQL formatada como um bloco de código.",
    agent=sql_query_writer_agent,
    context=[schema_analysis_task]
)

# Tarefa 3: Executar a consulta
query_execution_task = Task(
    description=(
        "Sua única função é executar a consulta SQL que foi fornecida no contexto. "
        "Você não deve analisar, interpretar ou modificar a consulta. "
        "Apenas execute-a usando a ferramenta 'SQL Query Executor Tool'."
    ),
    expected_output=(
        "O resultado bruto e exato da consulta SQL. "
        "Se a consulta retornar dados, a saída deve ser a lista de tuplas (ex: [(1, 'dado'), (2, 'outro dado')]). "
        "Se a consulta retornar uma lista vazia ([]), a saída deve ser a frase exata: 'Nenhum registro foi encontrado'. "
        "Não adicione nenhuma outra explicação ou texto."
    ),
    agent=db_executor_agent,
    context=[sql_writing_task]
)

# Tarefa 4: Analisar os dados e dar a resposta final
data_analysis_task = Task(
    description=(
        "Analise os dados brutos da consulta do contexto e a pergunta original do usuário '{question}'. "
        "Sua principal responsabilidade é responder DIRETAMENTE à pergunta do usuário. "
        "Se o usuário perguntar 'quantos', sua resposta final DEVE ser um número. "
        "Se a consulta inicial não fornecer a resposta final, você DEVE delegar para o 'Engenheiro de Queries SQL' "
        "para escrever uma nova consulta que responda à pergunta (ex: usando COUNT)."
    ),
    expected_output=(
        "A resposta final e formatada para o usuário. "
        "Esta DEVE ser uma lista numerada de cada manual, com seu nome, data e um resumo do seu conteúdo. "
        "Não inclua nenhuma conversa ou introdução, apenas a lista."
        "A resposta final e formatada para o usuário. Se a pergunta for sobre contagem, "
        "a resposta deve começar com o número total."
    ),
    agent=data_analyst_agent,
    context=[query_execution_task]
)

# Tarefa 5: Visualização de Dados
data_visualization_task = Task(
    description=(
        "O usuário quer um gráfico para responder à sua pergunta: '{question}'. "
    ),
    expected_output="A confirmação de que o gráfico foi criado e o caminho onde o arquivo de imagem foi salvo.",
    agent=data_visualization_agent,
    context=[sql_writing_task] # Depends on the SQL writer
)

# Tarefa 6: Edição de Registro
edit_database_task = Task(
    description=(
        "Atualize um registro específico no banco de dados. Use as seguintes informações fornecidas no contexto: "
        "- Tabela: '{table_name}' - ID do Registro: '{record_id}' "
        "- Coluna para Atualizar: '{column_to_update}' - Novo Valor: '{new_value}'"
    ),
    expected_output="Uma confirmação de que o registro foi atualizado com sucesso ou uma mensagem de erro clara.",
    agent=database_editor_agent
)

# Tarefa 7: Verificação Pós-Edição
verify_edit_task = Task(
    description=(
        "Um registro na tabela '{table_name}' com o ID '{record_id}' acabou de ser atualizado. "
        "Sua tarefa é executar uma consulta SQL para buscar este registro específico no banco de dados e exibir seus novos valores."
    ),
    expected_output="O conteúdo completo e atualizado do registro que foi modificado, formatado de forma clara para o usuário.",
    agent=data_verifier_agent,
    context=[edit_database_task]
)

# Tarefa 8: Inserção de Registro
insert_data_task = Task(
    description="Adicione um novo registro na tabela 'documentos' usando os dados fornecidos: nome do arquivo '{nome_arquivo}', tipo '{tipo}', data de criação '{data_criacao}', e resumo '{resumo}'.",
    expected_output="A confirmação de que o registro foi adicionado com sucesso, incluindo o ID do novo registro.",
    agent=data_inserter_agent
)

# Tarefa 9: Exclusão de Registro
delete_data_task = Task(
    description=(
        "Delete o registro da tabela 'documentos' com o ID '{record_id}'. "
        "IMPORTANTE: Antes de usar a 'Data Deleter Tool', você DEVE usar a ferramenta 'human_tool' para pedir confirmação ao usuário, "
        "fazendo a pergunta: 'Você tem certeza que deseja deletar o registro com ID {record_id}? Esta ação é irreversível. (sim/não)'"
    ),
    expected_output="A confirmação de que o registro foi ou não deletado, com base na resposta do usuário.",
    agent=data_deleter_agent
)

query_optimization_task = Task(
    description=(
        "Analise a pergunta do usuário: '{question}'. "
        "Se a pergunta for simples (ex: 'quantos manuais existem?'), reformule-a para ser mais útil "
        "(ex: 'faça uma contagem de quantos documentos existem para cada tipo diferente e me mostre os resultados'). "
        "IMPORTANTE: Ao enriquecer a pergunta, você NUNCA deve remover ou ignorar um filtro "
        "explícito que o usuário forneceu (como um tipo de documento específico, uma data ou um ID). "
        "Mantenha o filtro original e, se possível, adicione mais detalhes a ele."

        "Sua resposta final deve ser APENAS a pergunta otimizada, e nada mais."
    ),
    expected_output="A pergunta do usuário, otimizada para obter a resposta mais completa e útil possível, respeitando as restrições explícitas.",
    agent=query_optimizer_agent
)

translation_task = Task(
    description="Pegue a resposta final da tarefa de análise de dados e traduza todo o seu conteúdo para o português. Mantenha a formatação original.",
    expected_output="O texto completo da tarefa anterior, traduzido para o português.",
    agent=translator_agent,
    context=[data_analysis_task] # Depende da tarefa de análise de dados
)
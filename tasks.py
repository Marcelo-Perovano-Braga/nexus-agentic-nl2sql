from crewai import Task
from agents import (
    data_visualization_agent,
    database_editor_agent,
    data_verifier_agent,
    data_inserter_agent,
    data_deleter_agent,
    database_specialist_agent,
)

# Task 1: Data Extraction
data_extraction_task = Task(
    description=(
        "Pergunta do usuário: '{question}'\n\n"
        "Esquema do Banco de Dados Atual:\n{schema_context}\n\n"
        "Instruções de Execução Estritas:\n"
        "1. Analise o esquema fornecido e interprete a verdadeira intenção da pergunta do usuário.\n"
        "2. Escreva uma query SQL correta baseada no esquema fornecido.\n"
        "3. Use a ferramenta 'SQL Query Executor Tool' para extrair os resultados do banco de dados.\n"
        "4. Se a query falhar, leia o erro, corrija a sintaxe SQL e execute a ferramenta novamente.\n"
        "5. Analise os resultados brutos e elabore a resposta final em Português do Brasil de forma clara e concisa.\n"
        "6. Não inclua a query SQL na resposta final a menos que explicitamente solicitado."
    ),
    expected_output="A resposta em texto natural contendo os dados exatos solicitados pelo usuário.",
    agent=database_specialist_agent
)

# Task 2: Data Visualization
data_visualization_task = Task(
    description=(
        "O usuário quer um gráfico para responder à sua pergunta: '{question}'.\n\n"
        "Esquema do Banco de Dados:\n{schema_context}\n\n"
        "Instruções Estritas:\n"
        "1. Escreva uma query SQL baseada no esquema acima que retorne EXATAMENTE duas colunas (Eixo X para rótulos, Eixo Y para valores numéricos).\n"
        "2. Execute a 'Data Plotting Tool' passando a query SQL que você criou como argumento.\n"
        "3. Não invente dados; confie apenas no retorno da ferramenta."
    ),
    expected_output="A confirmação de que o gráfico foi criado e o caminho onde o arquivo de imagem foi salvo.",
    agent=data_visualization_agent
)

# Task 3: Edit Database
edit_database_task = Task(
    description=(
        "Atualize um registro específico no banco de dados. Use as seguintes informações fornecidas no contexto: "
        "- Tabela: '{table_name}' - ID do Registro: '{record_id}' "
        "- Coluna para Atualizar: '{column_to_update}' - Novo Valor: '{new_value}'"
    ),
    expected_output="Uma confirmação de que o registro foi atualizado com sucesso ou uma mensagem de erro clara.",
    agent=database_editor_agent
)

# Task 4: Post Edit Verification
verify_edit_task = Task(
    description=(
        "Um registro na tabela '{table_name}' com o ID '{record_id}' acabou de ser atualizado. "
        "Sua tarefa é executar uma consulta SQL para buscar este registro específico no banco de dados e exibir seus novos valores."
    ),
    expected_output="O conteúdo completo e atualizado do registro que foi modificado, formatado de forma clara para o usuário.",
    agent=data_verifier_agent,
    context=[edit_database_task]
)

# Task 5: Data Insertion
insert_data_task = Task(
    description="Adicione um novo registro na tabela 'documentos' usando os dados fornecidos: nome do arquivo '{nome_arquivo}', tipo '{tipo}', data de criação '{data_criacao}', e resumo '{resumo}'.",
    expected_output="A confirmação de que o registro foi adicionado com sucesso, incluindo o ID do novo registro.",
    agent=data_inserter_agent
)

# Task 6: Delete Task
delete_data_task = Task(
    description="Delete o registro da tabela 'documentos' com o ID '{record_id}' usando a ferramenta fornecida.",
    expected_output="A confirmação clara e direta de que o registro foi deletado do banco de dados.",
    agent=data_deleter_agent
)
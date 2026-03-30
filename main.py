from crewai import Crew, Process
from agents import (
    schema_analyst_agent, sql_query_writer_agent, db_executor_agent,
    data_analyst_agent, database_editor_agent, data_verifier_agent,
    data_visualization_agent, data_inserter_agent, data_deleter_agent,
    query_optimizer_agent, translator_agent
)
from tasks import (
    schema_analysis_task, sql_writing_task, query_execution_task,
    data_analysis_task, edit_database_task, verify_edit_task,
    data_visualization_task, insert_data_task, delete_data_task,
    query_optimization_task, translation_task
)
from dotenv import load_dotenv

load_dotenv()

def run_crew():
    print("## Bem-vindo à Equipe de Gerenciamento de Banco de Dados! ##")
    print("-----------------------------------------------------------")

    print("Escolha uma ação:")
    print("1: Buscar e/ou Editar um registro")
    print("2: Criar um gráfico a partir dos dados")
    print("3: Adicionar um novo registro")
    print("4: Deletar um registro")
    choice = input("Digite 1, 2, 3 ou 4: ")

    # Busca e edição:
    if choice == '1':
        initial_question = input("\nQual informação você gostaria de obter do banco de dados?\n")

        # Primeiro, otimiza a pergunta:
        optimizer_crew = Crew(
            agents=[query_optimizer_agent],
            tasks=[query_optimization_task],
            verbose=1,
            telemetry=False
        )
        
        optimized_question = optimizer_crew.kickoff(inputs={'question': initial_question})
        print(f"\nPergunta Otimizada: {optimized_question}")

        # Em seguida, executa a busca:
        search_crew = Crew(
            agents=[schema_analyst_agent, sql_query_writer_agent, db_executor_agent, data_analyst_agent, translator_agent],
            tasks=[schema_analysis_task, sql_writing_task, query_execution_task, data_analysis_task, translation_task],
            process=Process.sequential, 
            verbose=2,
            telemetry=False
        )
        result = search_crew.kickoff(inputs={'question': optimized_question})
        print("\n\n########################\n## Resposta Final da Equipe:\n########################\n")
        print(result)

        # Pergunta se o usuário quer editar:
        should_edit = input("\nGostaria de editar um registro com base nesta busca? (s/n) ").lower()
        if should_edit == 's':
            record_id = input("Qual o ID do registro que você quer editar? ")
            column = input("Qual o nome da coluna que você quer alterar? ")
            new_value = input("Qual o novo valor? ")
            edit_crew = Crew(
                agents=[database_editor_agent, data_verifier_agent],
                tasks=[edit_database_task, verify_edit_task],
                process=Process.sequential, 
                verbose=2,
                telemetry=False
            )
            edit_inputs = {'table_name': 'documentos', 'record_id': record_id, 'column_to_update': column, 'new_value': new_value}
            edit_result = edit_crew.kickoff(inputs=edit_inputs)
            print("\n\n########################\n## Resultado da Edição:\n########################\n")
            print(edit_result)

    # Criação de Gráfico:
    elif choice == '2':
        question = input("\nDescreva o gráfico que você gostaria de criar:\n")

        optimizer_crew = Crew(
            agents=[query_optimizer_agent],
            tasks=[query_optimization_task],
            verbose=1,
            telemetry=False
        )
        optimized_question = optimizer_crew.kickoff(inputs={'question': question})
        print(f"\nPergunta Otimizada: {optimized_question}")

        crew = Crew(
            agents=[schema_analyst_agent, sql_query_writer_agent, data_visualization_agent],
            tasks=[schema_analysis_task, sql_writing_task, data_visualization_task],
            process=Process.sequential, 
            verbose=2,
            telemetry=False
        )
        
        result = crew.kickoff(inputs={'question': optimized_question})
        print("\n\n########################\n## Resposta Final da Equipe:\n########################\n")
        print(result)

    # Adicionar um Registro:
    elif choice == '3':
        print("\nPara adicionar um novo registro, por favor, forneça:")
        nome = input("Nome do arquivo: ")
        tipo = input("Tipo de documento: ")
        data = input("Data de criação (YYYY-MM-DD): ")
        resumo = input("Resumo do conteúdo: ")

        inputs = {'nome_arquivo': nome, 'tipo': tipo, 'data_criacao': data, 'resumo': resumo}
        
        crew = Crew(
            agents=[data_inserter_agent],
            tasks=[insert_data_task],
            verbose=2,
            telemetry=False
        )
        result = crew.kickoff(inputs=inputs)
        print("\n\n########################\n## Resultado da Operação:\n########################\n")
        print(result)

    # Deletar um Registro:
    elif choice == '4':
        record_id = input("\nQual o ID do registro que você deseja deletar? (Primeiro, use a opção 1 para encontrar o ID)\n")
        crew = Crew(
            agents=[data_deleter_agent],
            tasks=[delete_data_task],
            verbose=2,
            telemetry=False
        )
        result = crew.kickoff(inputs={'record_id': record_id})
        print("\n\n########################\n## Resultado da Operação:\n########################\n")
        print(result)

    else:
        print("Opção inválida. Por favor, reinicie o programa.")
        return

if __name__ == '__main__':
    run_crew()
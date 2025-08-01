# main.py
from crewai import Crew, Process
# MUDANÇA 1: Importar o novo agente e tarefa de visualização
from agents import (
    schema_analyst_agent, 
    sql_query_writer_agent, 
    db_executor_agent, 
    data_analyst_agent,
    data_visualization_agent
)
from tasks import (
    schema_analysis_task, 
    sql_writing_task, 
    query_execution_task, 
    data_analysis_task,
    data_visualization_task
)
from dotenv import load_dotenv

load_dotenv()

def run_crew():
    print("## Bem-vindo à Equipe de Análise de Banco de Dados! ##")
    print("-----------------------------------------------------")
    
    # MUDANÇA 2: Adicionar a nova opção ao menu
    print("Escolha uma ação:")
    print("1: Fazer uma pergunta em linguagem natural sobre os dados")
    print("2: Criar um gráfico a partir de uma pergunta sobre os dados")
    choice = input("Digite 1 ou 2: ")

    # --- FLUXO DE TRABALHO 1: PERGUNTA E RESPOSTA ---
    if choice == '1':
        question = input("Qual informação você gostaria de obter do banco de dados?\n")
        
        crew = Crew(
            agents=[schema_analyst_agent, sql_query_writer_agent, db_executor_agent, data_analyst_agent],
            tasks=[schema_analysis_task, sql_writing_task, query_execution_task, data_analysis_task],
            process=Process.sequential,
            verbose=2
        )
        
        result = crew.kickoff(inputs={'question': question})

    # --- MUDANÇA 3: NOVO FLUXO DE TRABALHO PARA VISUALIZAÇÃO ---
    elif choice == '2':
        question = input("Qual gráfico você gostaria de criar? (ex: um gráfico de barras mostrando a contagem de documentos por tipo)\n")
        
        # Esta equipe precisa do Analista de Esquema, do Escritor de SQL e do novo Agente de Visualização
        crew = Crew(
            agents=[schema_analyst_agent, sql_query_writer_agent, data_visualization_agent],
            tasks=[schema_analysis_task, sql_writing_task, data_visualization_task],
            process=Process.sequential,
            verbose=2
        )
        
        result = crew.kickoff(inputs={'question': question})
        
    else:
        print("Opção inválida. Por favor, reinicie o programa.")
        return

    print("\n\n########################")
    print("## Resposta Final da Equipe:")
    print("########################\n")
    print(result)

if __name__ == '__main__':
    run_crew()
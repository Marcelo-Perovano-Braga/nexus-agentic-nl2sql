# main.py
from crewai import Crew, Process
from agents import schema_analyst_agent, sql_query_writer_agent, db_executor_agent, data_analyst_agent
from tasks import schema_analysis_task, sql_writing_task, query_execution_task, data_analysis_task
from dotenv import load_dotenv

load_dotenv()

def run_crew():
    print("## Bem-vindo à Equipe de Análise de Banco de Dados! ##")
    print("-----------------------------------------------------")
    
    question = input("Qual informação você gostaria de obter do banco de dados? (ex: 'Quais são todos os documentos do tipo Relatório?')\n")
    
    crew = Crew(
        agents=[schema_analyst_agent, sql_query_writer_agent, db_executor_agent, data_analyst_agent],
        tasks=[schema_analysis_task, sql_writing_task, query_execution_task, data_analysis_task],
        process=Process.sequential,
        verbose=2
    )
    
    result = crew.kickoff(inputs={'question': question})
    
    print("\n\n########################")
    print("## Resposta Final da Equipe:")
    print("########################\n")
    print(result)

if __name__ == '__main__':
    run_crew()
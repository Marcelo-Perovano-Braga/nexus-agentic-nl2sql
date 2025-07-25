# populate_database.py
import sqlite3
from faker import Faker
import random

# Initialize Faker to generate data in Brazilian Portuguese for more realism
fake = Faker('pt_BR')
DB_PATH = 'demodb.db'

def populate_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # (Opcional) Limpa a tabela para evitar dados duplicados ao rodar de novo
    print("Limpando dados antigos da tabela 'documentos'...")
    cursor.execute("DELETE FROM documentos;")

    print("Gerando e inserindo 50 novos registros...")
    documentos_exemplo = []
    tipos_de_documento = ['Relatório', 'Apresentação', 'Feedback', 'Contrato', 'Planilha', 'Manual']

    for _ in range(50):
        nome_arquivo = f"{fake.word()}_{fake.word()}_{random.randint(2022, 2025)}.{fake.random_element(elements=('pdf', 'docx', 'txt', 'xlsx'))}"
        tipo = fake.random_element(elements=tipos_de_documento)
        data_criacao = fake.date_between(start_date='-3y', end_date='today').strftime('%Y-%m-%d')
        resumo = fake.paragraph(nb_sentences=3)
        documentos_exemplo.append((nome_arquivo, tipo, data_criacao, resumo))

    cursor.executemany(
        'INSERT INTO documentos (nome_arquivo, tipo, data_criacao, resumo) VALUES (?,?,?,?)',
        documentos_exemplo
    )

    # Salva as mudanças e fecha a conexão
    conn.commit()
    conn.close()
    
    print(f"Sucesso! O banco de dados '{DB_PATH}' foi populado com 50 registros.")

if __name__ == '__main__':
    populate_db()
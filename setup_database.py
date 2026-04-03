import sqlite3

# Establishes connection to the Database
conn = sqlite3.connect('demodb.db')
cursor = conn.cursor()

# Creates an "Documents" section if there is no one present 
cursor.execute('''
    CREATE TABLE IF NOT EXISTS documentos (
        id INTEGER PRIMARY KEY,
        nome_arquivo TEXT NOT NULL,
        tipo TEXT,
        data_criacao TEXT,
        resumo TEXT
    )
''')

# Fills the test Database with a few examples
documentos_exemplo = [
    ('relatorio_vendas_q1.pdf', 'Relatório', '2025-04-15', 'Relatório trimestral sobre o desempenho de vendas no primeiro trimestre.'),
    ('apresentacao_marketing.pptx', 'Apresentação', '2025-05-20', 'Slides da nova campanha de marketing para o produto X.'),
    ('feedback_clientes.txt', 'Feedback', '2025-06-01', 'Notas brutas com o feedback dos clientes coletado em maio.')
]

cursor.executemany('INSERT INTO documentos (nome_arquivo, tipo, data_criacao, resumo) VALUES (?,?,?,?)', documentos_exemplo)

print("Banco de dados 'demodb.db' e tabela 'documentos' criados com sucesso!")

# Saves all changes and closes connections
conn.commit()
conn.close()
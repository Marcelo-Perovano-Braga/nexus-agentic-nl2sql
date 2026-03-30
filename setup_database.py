import sqlite3

# Conecta ao banco de dados (o arquivo será criado se não existir)
conn = sqlite3.connect('demodb.db')
cursor = conn.cursor()

# Cria uma tabela de "documentos"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS documentos (
        id INTEGER PRIMARY KEY,
        nome_arquivo TEXT NOT NULL,
        tipo TEXT,
        data_criacao TEXT,
        resumo TEXT
    )
''')

# Insere alguns dados de exemplo
documentos_exemplo = [
    ('relatorio_vendas_q1.pdf', 'Relatório', '2025-04-15', 'Relatório trimestral sobre o desempenho de vendas no primeiro trimestre.'),
    ('apresentacao_marketing.pptx', 'Apresentação', '2025-05-20', 'Slides da nova campanha de marketing para o produto X.'),
    ('feedback_clientes.txt', 'Feedback', '2025-06-01', 'Notas brutas com o feedback dos clientes coletado em maio.')
]

cursor.executemany('INSERT INTO documentos (nome_arquivo, tipo, data_criacao, resumo) VALUES (?,?,?,?)', documentos_exemplo)

print("Banco de dados 'demodb.db' e tabela 'documentos' criados com sucesso!")

# Salva as mudanças e fecha a conexão
conn.commit()
conn.close()
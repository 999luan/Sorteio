from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Pega a URL do banco de dados
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Cria a conexão com o banco
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    # Busca todos os pedidos
    result = conn.execute(text("SELECT * FROM orders;"))
    
    # Imprime cada linha
    for row in result:
        print("\n=== PEDIDO ===")
        for key, value in row._mapping.items():
            print(f"{key}: {value}") 
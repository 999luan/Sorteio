from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import logging
from tabulate import tabulate
from datetime import datetime

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Carrega variáveis de ambiente
load_dotenv()

# Pega a URL do banco de dados
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

if not DATABASE_URL:
    raise ValueError("DATABASE_URL não está configurada nas variáveis de ambiente!")

# Cria a conexão com o banco
engine = create_engine(DATABASE_URL)

def check_tokens():
    """Verifica os tokens vendidos e seus compradores"""
    try:
        with engine.connect() as conn:
            # Busca tokens vendidos com dados dos compradores
            result = conn.execute(text("""
                SELECT 
                    t.number as token,
                    o.customer_name as nome,
                    o.customer_email as email,
                    o.customer_phone as telefone,
                    o.payment_status as status,
                    o.purchase_date as data_compra
                FROM tokens t
                JOIN orders o ON t.order_id = o.id
                WHERE t.is_used = true
                ORDER BY o.purchase_date DESC;
            """))
            
            # Converte resultado em lista de dicionários
            tokens = []
            for row in result:
                token_dict = {
                    'Token': row.token,
                    'Nome': row.nome,
                    'Email': row.email,
                    'Telefone': row.telefone,
                    'Status': row.status,
                    'Data': row.data_compra.strftime('%d/%m/%Y %H:%M') if row.data_compra else '-'
                }
                tokens.append(token_dict)
            
            if tokens:
                print("\n🎫 TOKENS VENDIDOS:")
                print(tabulate(tokens, headers="keys", tablefmt="grid"))
                print(f"\nTotal de tokens vendidos: {len(tokens)}")
            else:
                print("\n❌ Nenhum token vendido ainda!")
            
            # Busca tokens disponíveis
            result = conn.execute(text("""
                SELECT COUNT(*) as total
                FROM tokens
                WHERE is_used = false;
            """))
            available = result.scalar()
            print(f"\n✨ Tokens disponíveis para venda: {available}")

    except Exception as e:
        logging.error(f"❌ Erro ao verificar tokens: {str(e)}")
        raise

if __name__ == "__main__":
    check_tokens() 
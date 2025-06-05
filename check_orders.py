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

def check_orders():
    """Verifica os pedidos na tabela orders"""
    try:
        with engine.connect() as conn:
            # Busca todos os pedidos
            result = conn.execute(text("""
                SELECT 
                    id,
                    external_reference,
                    customer_name,
                    customer_email,
                    customer_phone,
                    payment_status,
                    purchase_date,
                    (
                        SELECT COUNT(*)
                        FROM tokens t
                        WHERE t.order_id = orders.id
                    ) as total_tokens
                FROM orders
                ORDER BY purchase_date DESC;
            """))
            
            # Converte resultado em lista de dicionários
            orders = []
            for row in result:
                order_dict = {
                    'ID': row.id,
                    'Ref': row.external_reference,
                    'Nome': row.customer_name or '-',
                    'Email': row.customer_email or '-',
                    'Telefone': row.customer_phone or '-',
                    'Status': row.payment_status,
                    'Tokens': row.total_tokens,
                    'Data': row.purchase_date.strftime('%d/%m/%Y %H:%M') if row.purchase_date else '-'
                }
                orders.append(order_dict)
            
            if orders:
                print("\n📦 PEDIDOS REGISTRADOS:")
                print(tabulate(orders, headers="keys", tablefmt="grid"))
                print(f"\nTotal de pedidos: {len(orders)}")
            else:
                print("\n❌ Nenhum pedido registrado na tabela orders!")

    except Exception as e:
        logging.error(f"❌ Erro ao verificar pedidos: {str(e)}")
        raise

if __name__ == "__main__":
    check_orders() 
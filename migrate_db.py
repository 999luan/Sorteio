from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import logging

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

def migrate_database():
    """
    Executa a migração do banco de dados:
    1. Cria a nova tabela orders
    2. Migra os dados existentes
    3. Atualiza a estrutura da tabela tokens
    """
    try:
        with engine.connect() as conn:
            # Inicia uma transação
            with conn.begin():
                logging.info("🚀 Iniciando migração do banco de dados...")

                # 1. Verifica se a tabela orders já existe
                logging.info("Verificando se a tabela orders existe...")
                result = conn.execute(text("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'orders'
                    );
                """))
                table_exists = result.scalar()

                if not table_exists:
                    logging.info("Criando tabela orders...")
                    conn.execute(text("""
                        CREATE TABLE orders (
                            id SERIAL PRIMARY KEY,
                            external_reference VARCHAR UNIQUE,
                            payment_id VARCHAR UNIQUE,
                            payment_status VARCHAR,
                            total_amount FLOAT,
                            purchase_date TIMESTAMP,
                            customer_name VARCHAR,
                            customer_email VARCHAR,
                            customer_cpf VARCHAR,
                            customer_phone VARCHAR
                        );
                    """))
                    logging.info("✅ Tabela orders criada com sucesso!")
                else:
                    logging.info("Tabela orders já existe, pulando criação...")

                # 2. Migra dados existentes dos tokens para orders
                logging.info("Migrando dados existentes...")
                conn.execute(text("""
                    INSERT INTO orders (
                        external_reference,
                        payment_id,
                        payment_status,
                        total_amount,
                        purchase_date,
                        customer_name,
                        customer_email,
                        customer_cpf,
                        customer_phone
                    )
                    SELECT DISTINCT ON (external_reference)
                        external_reference,
                        payment_id,
                        payment_status,
                        total_amount,
                        purchase_date,
                        owner_name as customer_name,
                        owner_email as customer_email,
                        owner_cpf as customer_cpf,
                        owner_phone as customer_phone
                    FROM tokens
                    WHERE external_reference IS NOT NULL
                    AND NOT EXISTS (
                        SELECT 1 FROM orders o 
                        WHERE o.external_reference = tokens.external_reference
                    );
                """))
                logging.info("✅ Dados migrados com sucesso!")

                # 3. Adiciona coluna order_id na tabela tokens se não existir
                logging.info("Verificando coluna order_id na tabela tokens...")
                result = conn.execute(text("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.columns 
                        WHERE table_name = 'tokens' AND column_name = 'order_id'
                    );
                """))
                column_exists = result.scalar()

                if not column_exists:
                    logging.info("Adicionando coluna order_id na tabela tokens...")
                    conn.execute(text("""
                        ALTER TABLE tokens 
                        ADD COLUMN order_id INTEGER REFERENCES orders(id);
                    """))
                    logging.info("✅ Coluna order_id adicionada com sucesso!")
                else:
                    logging.info("Coluna order_id já existe, pulando criação...")

                # 4. Atualiza os order_id nos tokens existentes
                logging.info("Atualizando order_id nos tokens...")
                conn.execute(text("""
                    UPDATE tokens t
                    SET order_id = o.id
                    FROM orders o
                    WHERE t.external_reference = o.external_reference
                    AND t.external_reference IS NOT NULL;
                """))
                logging.info("✅ Order IDs atualizados com sucesso!")

                # 5. Remove colunas antigas da tabela tokens
                logging.info("Removendo colunas antigas da tabela tokens...")
                old_columns = [
                    'owner_name', 'owner_email', 'owner_cpf', 'owner_phone',
                    'payment_id', 'payment_status', 'external_reference',
                    'purchase_date', 'total_amount'
                ]
                
                for column in old_columns:
                    result = conn.execute(text(f"""
                        SELECT EXISTS (
                            SELECT FROM information_schema.columns 
                            WHERE table_name = 'tokens' AND column_name = '{column}'
                        );
                    """))
                    if result.scalar():
                        logging.info(f"Removendo coluna {column}...")
                        conn.execute(text(f"ALTER TABLE tokens DROP COLUMN {column};"))

                logging.info("✅ Colunas antigas removidas com sucesso!")
                
                logging.info("🎉 Migração concluída com sucesso!")

    except Exception as e:
        logging.error(f"❌ Erro durante a migração: {str(e)}")
        raise

if __name__ == "__main__":
    migrate_database() 
import os
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Token, Order

# Configuração do banco de dados
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///sorteio.db')
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Criar engine do SQLAlchemy
engine = create_engine(DATABASE_URL)

def reset_database():
    print("🗑️ Removendo tabelas existentes...")
    Base.metadata.drop_all(engine)
    
    print("🏗️ Criando novas tabelas...")
    Base.metadata.create_all(engine)
    
    # Criar sessão
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        print("📝 Lendo tokens do arquivo CSV...")
        with open('tokens.csv', 'r') as file:
            csv_reader = csv.DictReader(file)
            tokens_count = 0
            
            print("💾 Inserindo tokens no banco de dados...")
            for row in csv_reader:
                token = Token(
                    number=row['Token'],
                    is_used=False
                )
                session.add(token)
                tokens_count += 1
                
                # Commit a cada 100 tokens para não sobrecarregar a memória
                if tokens_count % 100 == 0:
                    session.commit()
                    print(f"✅ {tokens_count} tokens inseridos...")
            
            # Commit final para os tokens restantes
            session.commit()
            print(f"🎉 Total de {tokens_count} tokens inseridos com sucesso!")
            
    except Exception as e:
        print(f"❌ Erro durante a inserção dos tokens: {str(e)}")
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == "__main__":
    print("🚀 Iniciando reset do banco de dados...")
    reset_database()
    print("✨ Banco de dados resetado e populado com sucesso!") 
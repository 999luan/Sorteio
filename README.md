# 🎰 Sistema de Sorteio de Carro

Sistema web para venda de números da sorte para sorteio de carro, com integração ao Mercado Pago para pagamentos.

## 🚀 Funcionalidades

- ✨ Interface moderna e responsiva com efeitos visuais dinâmicos.
- 🚗 **Carrossel de Imagens:** Exibição interativa de fotos do carro do sorteio.
- ✍️ **Efeito Typewriter:** Título dinâmico na página inicial para engajamento.
- 💳 Integração com Mercado Pago para processamento de pagamentos.
- 📧 Notificações por e-mail automáticas para confirmação de compra.
- 🔔 Notificações no Discord para acompanhamento de vendas em tempo real.
- 🎫 Gerenciamento de números da sorte, com reserva e liberação.
-  Layout adaptativo para mobile, garantindo ótima experiência em qualquer dispositivo.
- 🖨️ Opção de impressão dos números da sorte para registro físico.
- 📄 **Ficha Técnica Detalhada:** Modal com informações completas sobre o veículo.

## 🛠️ Tecnologias Utilizadas

- Python 3.x
- Flask (Framework Web)
- Gunicorn (WSGI Server)
- SQLAlchemy (ORM)
- PostgreSQL (Banco de Dados)
- Mercado Pago SDK
- Flask-Mail
- Python-Jose (JWT for security)
- HTML/CSS/JavaScript
- Vercel (Deploy)
- Railway (Deploy)

## ⚙️ Configuração do Ambiente

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/Sorteio.git
cd Sorteio
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente (.env):
```env
# Banco de Dados
DATABASE_URL=postgresql://user:password@localhost:5432/sorteio

# Mercado Pago
MP_ACCESS_TOKEN=seu_token_aqui

# Email
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=seu_email@gmail.com
MAIL_PASSWORD=sua_senha_app
MAIL_DEFAULT_SENDER=seu_email@gmail.com

# Discord
DISCORD_WEBHOOK_URL=sua_url_webhook

# Aplicação
BASE_URL=https://seu-dominio.com
```

## 🗃️ Estrutura do Banco de Dados

O sistema utiliza uma tabela principal para gerenciar os tokens de sorteio e as informações dos compradores:

### Tabela: `tokens`
- `id`: ID único do token (Integer, Primary Key, Index)
- `number`: Número da sorte (String, Unique, Index, Not Null)
- `is_used`: Status de uso do token (Boolean, Default: False)
- `owner_name`: Nome completo do comprador (String)
- `owner_email`: E-mail do comprador (String)
- `owner_cpf`: CPF do comprador (String)
- `owner_phone`: Telefone do comprador (String)
- `payment_id`: ID do pagamento gerado pelo Mercado Pago (String)
- `payment_status`: Status do pagamento (ex: 'pending', 'approved', 'rejected') (String)
- `external_reference`: Referência externa da transação, usada para agrupar tokens de uma mesma compra (String, Index)
- `purchase_date`: Data e hora da compra (DateTime, Default: UTC Now)
- `total_amount`: Valor total pago por este token (Float)

### Conexão com o Banco de Dados

- O sistema é configurado para se conectar a um banco de dados PostgreSQL, utilizando SQLAlchemy como ORM.
- A URL de conexão é definida pela variável de ambiente `DATABASE_URL`.
- Há uma configuração específica para otimizar a conexão com o **Supabase Transaction Pooler**, incluindo parâmetros como `sslmode=require`, `connect_timeout`, `application_name`, e `statement_timeout`.
- A função `get_db` implementa um mecanismo de retry para garantir a robustez da conexão em caso de falhas temporárias.

## 📋 Scripts de Utilidade

- `reset_db.py`: Reseta o banco de dados e carrega tokens iniciais
- `check_db.py`: Verifica integridade dos dados
- `verify_data_integrity.py`: Validação completa dos dados

## 🔄 Fluxo de Pagamento

1. Cliente seleciona quantidade de números
2. Sistema reserva números disponíveis
3. Integração com Mercado Pago gera pagamento
4. Webhook recebe confirmação de pagamento
5. Sistema envia emails e notificações
6. Números são marcados como vendidos

## 📱 Endpoints da API

- `GET /`: Página inicial
- `POST /create_preference`: Cria preferência de pagamento
- `POST /mercadopago_webhook`: Webhook do Mercado Pago
- `GET /payment_status`: Status do pagamento
- `GET /test_notifications`: Teste de notificações

## 🔍 Monitoramento

O sistema inclui logs detalhados para:
- Transações de pagamento
- Envio de emails
- Notificações Discord
- Operações no banco de dados
- Webhooks recebidos

## 🚨 Tratamento de Erros

- Validação de dados de entrada
- Tratamento de falhas de pagamento
- Backup de dados importantes
- Logs de erros detalhados
- Notificações de falhas

## 🔐 Segurança

- Validação de webhooks
- Proteção contra duplicidade
- Sanitização de inputs
- Controle de acesso
- Backup automático

## 📦 Deploy

### Deploy na Vercel

O sistema está configurado para deploy na Vercel:
- Arquivo `vercel.json` com configurações
- Suporte a serverless functions
- Configuração de rotas
- Variáveis de ambiente

### Deploy na Railway

O sistema também está configurado para deploy na Railway:
- Arquivo `Procfile` para definir o comando de inicialização do Gunicorn.
- Arquivo `railway.json` com configurações de build e deploy, incluindo healthcheck.
- A Railway detectará automaticamente o `Procfile` e o `railway.json` para configurar o deploy.
- Certifique-se de configurar as mesmas variáveis de ambiente (`.env`) na Railway.

## 🤝 Contribuição

1. Faça o fork do projeto
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add: nova funcionalidade'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

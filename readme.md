# Product Microservice API 🚀

Uma API de microserviço desenvolvida com **FastAPI** para gerenciar produtos de uma empresa. O projeto segue boas práticas como **TDD**, autenticação com **JWT**, **paginação** e integração com **PostgreSQL**.

## 📌 Tecnologias Utilizadas

- **FastAPI** - Framework rápido e moderno para APIs  
- **PostgreSQL** - Banco de dados relacional  
- **SQLAlchemy** - ORM para manipulação do banco de dados  
- **Alembic** - Controle de versões do banco de dados (migrations)  
- **Docker & Docker Compose** - Containerização do ambiente  
- **JWT (JSON Web Token)** - Autenticação segura  
- **TDD (Test-Driven Development)** - Desenvolvimento orientado a testes  

## 📦 Funcionalidades

✅ CRUD completo de **produtos**  
✅ Listagem de produtos com **filtro por nome**  
✅ Listagem, criação e deleção de **categorias**  
✅ Autenticação de usuários com **JWT**  
✅ **Paginação** na listagem de produtos  

## 🚀 Como Executar o Projeto

1. Clone este repositório:  
   ```bash
   git clone https://github.com/AfonsoDolmen/product-microservice-api.git
   cd product-microservice-api
   ```

2. Crie um arquivo .env na raiz do projeto e defina as variáveis de ambiente necessárias:
    ```ini
    POSTGRES_USER=SEU_USUARIO_POSTGRES
    POSTGRES_PASSWORD=SUA_SENHA_POSTGRES
    POSTGRES_DB=NOME_DO_BANCO
    PGADMIN_DEFAULT_EMAIL=EMAIL_DO_PGADMIN
    PGADMIN_DEFAULT_PASSWORD=SENHA_DO_PGADMIN
    DB_URL=URL_DO_BANCO_DE_DADOS
    DB_TEST_URL=URL_DO_BANCO_DE_TESTE
    TEST_MODE=1
    SECRET_KEY=CHAVE_SECRETA_PARA_JWT
    ALGORITHM=ALGORITMO_JWT
    ```

3. Configure o ambiente com **Docker**:
    ```bash
    docker-compose up --build
    ```

4. Acesse a documentação interativa com seu navegador
    ```
    http://localhost:8000/api/docs
    ```

## 📄 Licença
Este projeto é open-source e está sob a licença **MIT**.
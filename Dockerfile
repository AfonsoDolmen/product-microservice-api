FROM python:3.13.2-slim-bullseye

# Variáveis de ambiente
ENV PYTHONUNBUFFERED 1
ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONPATH="/"

# Copiando arquivos do poetry para a imagem
COPY ./poetry.lock ./pyproject.toml /app/
WORKDIR /app

# Instalação do Poetry e dependências
RUN apt-get update -y && \
    apt-get install curl -y && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# Copiando o restante do projeto
COPY . .

EXPOSE 8000

# Comando padrão
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

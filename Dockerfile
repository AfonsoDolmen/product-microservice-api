FROM python:3.11-slim-buster

# Variáveis de ambiente
ENV PYTHONUNBUFFERED 1
ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONPATH="/"

# Copiando arquivos do poetry para a imagem
COPY ./poetry.lock /
COPY ./pyproject.toml /

# Instalação e configuração do Poetry
RUN apt-get update -y && apt-get install curl -y \
&& curl -sSL https://install.python-poetry.org | python3 - \
&& poetry config virtualenvs.create false \
&& poetry install \
&& apt-get remove curl -y

# Copiando o projeto para a imagem
COPY ./app /app
WORKDIR /app
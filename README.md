# EventReady - Backend 🚀

API desenvolvida para o gerenciamento e organização de eventos, construída com **FastAPI** e **PostgreSQL**, totalmente conteinerizada com **Docker**.

## 🛠 Tecnologias Utilizadas

- **[FastAPI](https://fastapi.tiangolo.com/)** - Framework web moderno e de alta performance para construção de APIs em Python.
- **[PostgreSQL](https://www.postgresql.org/)** - Banco de dados relacional robusto.
- **[Docker](https://www.docker.com/)** & **[Docker Compose](https://docs.docker.com/compose/)** - Para isolamento de ambiente e orquestração dos containers.
- **Uvicorn** - Servidor ASGI para FastAPI.

---

## 📋 Pré-requisitos

Certifique-se de ter as seguintes ferramentas instaladas na sua máquina:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## 🚀 Como Rodar o Projeto (Com Docker)

Esta é a forma mais fácil e recomendada de rodar a aplicação, pois o banco de dados e a API sobem automaticamente configurados.

1. Clone o repositório para a sua máquina:
   ```bash
   git clone [https://github.com/pedrovitorino07/eventready-backend.git](https://github.com/pedrovitorino07/eventready-backend.git)
   cd eventready-backend

# EventReady - Backend 

API para gerenciamento e organização de eventos, com foco em ajudar organizadores a decidir se as condições climáticas previstas são favoráveis para o dia do evento. Construída com **FastAPI** e **PostgreSQL**, totalmente conteinerizada com **Docker**.

##  Funcionalidades

- **CRUD de eventos** — criação, listagem, atualização e remoção de eventos.
- **Geocodificação automática** — ao criar/atualizar um evento, se latitude e longitude não forem informadas, elas são obtidas automaticamente a partir do nome do local (via [Open-Meteo Geocoding API](https://open-meteo.com/en/docs/geocoding-api)).
- **Previsão do tempo por evento** — busca a previsão climática para a data e local do evento (via [Open-Meteo Forecast API](https://open-meteo.com/en/docs)).
- **Análise climática** — classifica o clima previsto (ex: `IDEAL`, `REGULAR`, `ALERTA`) com motivos e recomendações práticas (ex: "prefira um local coberto", "reforce a hidratação").
- **Event Score** — nota de 0 a 100 calculada a partir da chance de chuva, temperatura, condição do céu e horário do evento, classificando o evento como `EXCELENTE`, `BOM`, `REGULAR` ou `RUIM`.
- **Favoritos** — usuários podem favoritar/desfavoritar eventos e listar seus favoritos.

##  Tecnologias Utilizadas

- **[FastAPI](https://fastapi.tiangolo.com/)** — Framework web moderno e de alta performance para construção de APIs em Python.
- **[PostgreSQL](https://www.postgresql.org/)** — Banco de dados relacional.
- **[SQLAlchemy](https://www.sqlalchemy.org/)** — ORM para modelagem e acesso ao banco de dados.
- **[Pydantic](https://docs.pydantic.dev/)** — Validação de dados e schemas.
- **[httpx](https://www.python-httpx.org/)** — Cliente HTTP para consumo das APIs externas de clima.
- **[Open-Meteo](https://open-meteo.com/)** — APIs gratuitas de geocodificação e previsão do tempo.
- **[Docker](https://www.docker.com/)** & **[Docker Compose](https://docs.docker.com/compose/)** — Isolamento de ambiente e orquestração dos containers.
- **Uvicorn** — Servidor ASGI para a aplicação FastAPI.

##  Estrutura do Projeto

```
eventready-backend/
├── app/
│   ├── main.py                       # Ponto de entrada da aplicação FastAPI
│   ├── database.py                   # Configuração da conexão com o banco (SQLAlchemy)
│   ├── models/
│   │   ├── event.py                  # Modelo Evento
│   │   └── favorite.py               # Modelo Favorite
│   ├── schemas/
│   │   └── event.py                  # Schemas Pydantic (request/response)
│   ├── routers/
│   │   ├── event.py                  # Rotas de eventos e clima
│   │   └── favorites.py              # Rotas de favoritos
│   ├── services/
│   │   ├── weather.py                # Integração com Open-Meteo (geocoding e previsão)
│   │   ├── climate_analysis_service.py  # Classificação do clima e recomendações
│   │   ├── event_score_service.py    # Cálculo do Event Score
│   │   └── favorite_service.py       # Regras de negócio de favoritos
│   └── tests/
│       └── test_features.py          # Testes de clima e event score
├── dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

##  Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

Para rodar sem Docker, você também vai precisar de:
- [Python 3.11+](https://www.python.org/downloads/)
- Uma instância do [PostgreSQL](https://www.postgresql.org/download/) em execução

##  Como Rodar o Projeto (com Docker)

Esta é a forma mais fácil e recomendada, já que o banco de dados e a API sobem automaticamente configurados.

1. Clone o repositório:
   ```bash
   git clone https://github.com/pedrovitorino07/eventready-backend.git
   cd eventready-backend
   ```

2. Suba os containers:
   ```bash
   docker-compose up --build
   ```

3. A API estará disponível em `http://localhost:8000` e a documentação interativa (Swagger) em `http://localhost:8000/docs`.

O `docker-compose.yml` já sobe dois serviços:
- **db** — PostgreSQL 15, exposto na porta `5432`.
- **web** — API FastAPI, exposta na porta `8000`, conectada automaticamente ao banco.

##  Como Rodar Localmente (sem Docker)

1. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/Mac
   venv\Scripts\activate         # Windows
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure a variável de ambiente `DATABASE_URL` apontando para o seu PostgreSQL (veja a seção abaixo) e garanta que o banco `eventready` (ou o nome configurado) exista.

4. Rode a aplicação:
   ```bash
   uvicorn app.main:app --reload
   ```

##  Variáveis de Ambiente

| Variável       | Descrição                                   | Padrão (local)                                            |
| -------------- | -------------------------------------------- | ----------------------------------------------------------- |
| `DATABASE_URL` | String de conexão do PostgreSQL              | `postgresql://postgres:123@localhost:5432/eventready`       |

No `docker-compose.yml`, essa variável já é definida automaticamente para apontar para o container `db`.

>  **Nota:** as credenciais do banco no `docker-compose.yml` são apenas para ambiente de desenvolvimento local. Não as utilize em produção — use variáveis de ambiente/secrets adequados.

##  Endpoints da API

### Eventos

| Método   | Rota                     | Descrição                                                                 |
| -------- | ------------------------ | --------------------------------------------------------------------------- |
| `POST`   | `/eventos/`               | Cria um novo evento (geocodifica o local automaticamente, se necessário). |
| `GET`    | `/eventos/`               | Lista todos os eventos cadastrados.                                       |
| `GET`    | `/eventos/{evento_id}/clima` | Retorna o evento com previsão do tempo, análise climática, event score e status de favorito. |
| `PUT`    | `/eventos/{evento_id}`    | Atualiza um evento existente.                                             |
| `DELETE` | `/eventos/{evento_id}`    | Remove um evento.                                                         |

### Favoritos

| Método   | Rota                              | Descrição                                  |
| -------- | ---------------------------------- | -------------------------------------------- |
| `POST`   | `/eventos/{event_id}/favoritar`    | Favorita um evento.                        |
| `DELETE` | `/eventos/{event_id}/favoritar`    | Remove um evento dos favoritos.            |
| `GET`    | `/eventos/favoritos`               | Lista os eventos favoritados pelo usuário. |

> A documentação completa e interativa de todos os endpoints (com exemplos de request/response) fica disponível automaticamente em `/docs` (Swagger UI) e `/redoc` assim que a API estiver rodando.

### Exemplo de resposta — `GET /eventos/{evento_id}/clima`

```json
{
  "evento": {
    "id": 1,
    "nome": "Festival de Verão",
    "data": "2026-12-20",
    "horario": "18:00",
    "local": "Recife, PE",
    "latitude": -8.0476,
    "longitude": -34.877
  },
  "clima": {
    "condicao": "Céu limpo",
    "temperatura_max": 29.5,
    "sensacao_max": 31.0,
    "chance_chuva": 10,
    "vento_max": 14.2,
    "indice_uv_max": 9.0,
    "sol": { "nascer": "05:12", "por": "17:34" }
  },
  "analise_climatica": {
    "nivel": "REGULAR",
    "motivos": ["Índice UV muito alto"],
    "recomendacoes": ["Utilize protetor solar e busque áreas de sombra"]
  },
  "event_score": {
    "score": 88,
    "nivel": "EXCELENTE",
    "fatores": {
      "clima": 25,
      "chuva": 23,
      "temperatura": 25,
      "horario": 25
    }
  },
  "favoritado": false
}
```

##  Testes

O projeto conta com testes unitários para os serviços de análise climática e cálculo de event score, em `app/tests/test_features.py`.

Para rodar (é necessário ter o `pytest` instalado):

```bash
pip install pytest
pytest
```

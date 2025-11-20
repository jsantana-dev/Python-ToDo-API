# 📝 Python-ToDo-API

API REST para gerenciamento de tarefas (To-Do List) desenvolvida em Python puro, sem uso de frameworks externos. Implementa operações CRUD completas com persistência em SQLite.

## 📋 Sobre o Projeto

Este projeto foi desenvolvido com o objetivo de demonstrar conhecimento em desenvolvimento de APIs REST utilizando apenas bibliotecas nativas do Python. A aplicação implementa um servidor HTTP customizado (`http.server`) integrado com banco de dados SQLite, utilizando SQL puro para manipulação de dados, sem depender de ORMs ou frameworks como Django/Flask.

## ✨ Funcionalidades

### API REST (Back-end)
- ✅ **POST** `/tasks` - Criar nova tarefa
- ✅ **GET** `/tasks` - Listar todas as tarefas
- ✅ **GET** `/tasks/<id>` - Buscar tarefa específica por ID
- ✅ **PUT** `/tasks/<id>` - Atualizar tarefa existente
- ✅ **DELETE** `/tasks/<id>` - Remover tarefa

### Cliente CLI
- Interface de linha de comando para interação com a API
- Operações CRUD completas via terminal
- Tratamento de códigos HTTP e respostas da API
- Comandos intuitivos e feedback visual

### Recursos Técnicos
- 🗄️ Persistência de dados em SQLite
- 🔒 SQL puro (sem ORM)
- 📡 Protocolo HTTP/REST
- 🔄 Criação automática do banco de dados
- ⚡ Servidor HTTP nativo do Python
- 🎯 Arquitetura cliente-servidor

## 🏗️ Arquitetura do Projeto

O projeto foi estruturado seguindo o padrão de **arquitetura em camadas**, aplicando os princípios SOLID e separação de responsabilidades:

```
Python-ToDo-API/
├── app/                          # Aplicação principal
│   ├── __init__.py              # Inicialização do módulo
│   ├── server.py                # Servidor HTTP
│   ├── routes.py                # Definição de rotas
│   ├── controllers/             # Camada de controle (lógica de negócio)
│   │   ├── __init__.py
│   │   └── task_controller.py
│   ├── models/                  # Camada de modelo (entidades)
│   │   ├── __init__.py
│   │   └── task.py
│   ├── database/                # Camada de persistência
│   │   ├── __init__.py
│   │   ├── connection.py        # Gerenciamento de conexões
│   │   └── task_repository.py  # Queries e acesso aos dados
│   ├── validators/              # Validações de entrada
│   │   ├── __init__.py
│   │   └── task_validator.py
│   └── utils/                   # Utilitários
│       ├── __init__.py
│       └── response.py          # Helpers de resposta HTTP
├── client/                      # Cliente CLI
│   └── client.py
├── create_db.sql                # Script SQL de criação
├── tasks.db                     # Banco de dados (gerado automaticamente)
├── requirements.txt             # Dependências
└── README.md                    # Documentação
```

### Responsabilidades por Camada

- **Models:** Representação das entidades de negócio (Task)
- **Controllers:** Lógica de negócio e orquestração
- **Database:** Acesso aos dados e persistência (Repository Pattern)
- **Validators:** Validação e sanitização de dados
- **Utils:** Funções auxiliares e helpers
- **Routes:** Mapeamento de endpoints para controllers

## 🛠️ Tecnologias Utilizadas

- **Python 3** - Linguagem principal
- **http.server** - Servidor HTTP nativo
- **sqlite3** - Banco de dados embutido
- **SQL** - Queries puras para manipulação de dados
- **requests** - Biblioteca para cliente HTTP (CLI)
- **json** - Serialização de dados
- **argparse** - Parser de argumentos CLI

## 🚀 Como Executar

### Pré-requisitos

- Python 3.7 ou superior instalado
- pip (gerenciador de pacotes Python)

### Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/jsantana-dev/Python-ToDo-API.git
cd Python-ToDo-API
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **(Opcional) Criar banco manualmente:**
```bash
sqlite3 tasks.db < create_db.sql
```
> **Nota:** O servidor cria o banco automaticamente na primeira execução.

### Executando o Servidor

```bash
python server.py 8000
```

O servidor estará rodando em `http://localhost:8000`

### Usando o Cliente CLI

#### Listar todas as tarefas:
```bash
python client.py list
```

#### Criar nova tarefa:
```bash
python client.py create "Estudar Python" --d "Revisar conceitos de OOP"
```

#### Buscar tarefa específica:
```bash
python client.py get 1
```

#### Atualizar tarefa:
```bash
python client.py update 1 --status completo
```

#### Deletar tarefa:
```bash
python client.py delete 1
```

## 📡 Documentação da API

### Endpoints

#### `POST /tasks`
Cria uma nova tarefa.

**Request Body:**
```json
{
  "title": "Título da tarefa",
  "description": "Descrição detalhada",
  "status": "pendente"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "title": "Título da tarefa",
  "description": "Descrição detalhada",
  "status": "pendente"
}
```

---

#### `GET /tasks`
Lista todas as tarefas cadastradas.

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "title": "Tarefa 1",
    "description": "Descrição",
    "status": "pendente"
  },
  {
    "id": 2,
    "title": "Tarefa 2",
    "description": "Descrição",
    "status": "completo"
  }
]
```

---

#### `GET /tasks/<id>`
Busca uma tarefa específica por ID.

**Response:** `200 OK`
```json
{
  "id": 1,
  "title": "Tarefa 1",
  "description": "Descrição",
  "status": "pendente"
}
```

**Erro:** `404 Not Found` - Tarefa não encontrada

---

#### `PUT /tasks/<id>`
Atualiza uma tarefa existente.

**Request Body:**
```json
{
  "title": "Novo título",
  "description": "Nova descrição",
  "status": "completo"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "title": "Novo título",
  "description": "Nova descrição",
  "status": "completo"
}
```

---

#### `DELETE /tasks/<id>`
Remove uma tarefa do sistema.

**Response:** `204 No Content`

**Erro:** `404 Not Found` - Tarefa não encontrada

## 🗄️ Estrutura do Banco de Dados

### Tabela: `tasks`

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id | INTEGER | Chave primária (autoincremento) |
| title | TEXT | Título da tarefa (obrigatório) |
| description | TEXT | Descrição detalhada (opcional) |
| status | TEXT | Status: "pendente" ou "completo" |

## 🎯 Conceitos Aplicados

- ✅ API RESTful
- ✅ Arquitetura Cliente-Servidor
- ✅ Protocolo HTTP (métodos, códigos de status)
- ✅ Persistência de dados (SQLite)
- ✅ SQL puro (queries, transactions)
- ✅ Serialização JSON
- ✅ Interface de linha de comando (CLI)
- ✅ Tratamento de exceções
- ✅ Validação de entrada

## 🔄 Melhorias Futuras

- [ ] Adicionar autenticação (JWT)
- [ ] Implementar validações robustas
- [ ] Adicionar filtros e paginação
- [ ] Testes unitários e de integração
- [ ] Logging estruturado
- [ ] Documentação OpenAPI/Swagger
- [ ] Suporte a CORS
- [ ] Docker/docker-compose
- [ ] Migração para framework (FastAPI/Flask)
- [ ] Front-end web

## 📚 Aprendizados

Este projeto me permitiu desenvolver e aprimorar:

- ✅ Desenvolvimento de APIs REST do zero
- ✅ Manipulação de banco de dados com SQL puro
- ✅ Trabalho com protocolo HTTP em baixo nível
- ✅ Criação de CLIs interativos
- ✅ Arquitetura cliente-servidor
- ✅ Boas práticas de versionamento (Git)

## 👨‍💻 Autor

**Jamylle Santana**
- LinkedIn: https://www.linkedin.com/in/jamylle-santana

## 📄 Licença

Este projeto é de código aberto e pode ser usado para aprendizado e melhorias. 🚀

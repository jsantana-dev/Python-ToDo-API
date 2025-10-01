# Sistema de Gestão de Tarefas (To-Do)

Arquivos entregues:
- server.py       -> Servidor em Python (http.server + sqlite3)
- client.py       -> Cliente CLI em Python (usa requests)
- create_db.sql   -> Script SQL para criar a tabela `tasks`
- tasks.db        -> (opcional) banco SQLite criado ao iniciar o servidor
- requirements.txt -> requests
- README.md       -> Descrição de funcionamento do projeto

Requisitos implementados:
- Rotas:
  * POST   /tasks
  * GET    /tasks
  * GET    /tasks/<id>
  * PUT    /tasks/<id>
  * DELETE /tasks/<id>

- Persistência em SQLite via SQL puro.
- Cliente CLI com operações CRUD e tratamento básico de códigos HTTP.

Como usar:
1. Criar banco manualmente (opcional):
   sqlite3 tasks.db < create_db.sql

2. Rodar o servidor:
   py server.py 8000

   O servidor cria tasks.db automaticamente se não existir.

3. Usar o cliente:
   py client.py list
   py client.py create "Tarefa exemplo" --d "..." 
   py client.py get 1
   py client.py update 1 --status completo
   py client.py delete 1

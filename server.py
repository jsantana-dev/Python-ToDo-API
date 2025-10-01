import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import sqlite3
import sys
from urllib.parse import urlparse
import re

DB_PATH = "tasks.db"

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL DEFAULT 'pendente',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript(CREATE_TABLE_SQL)
    conn.commit()
    conn.close()

class TaskHandler(BaseHTTPRequestHandler):
    def _send(self, code=200, data=None):
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        if data is not None:
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def _read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return None
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode("utf-8"))
        except Exception:
            return None

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/tasks":
            body = self._read_json()
            if not body or "title" not in body or not body["title"]:
                return self._send(400, {"error": "campo 'title' é obrigatório"})
            title = body["title"]
            description = body.get("description")
            status = body.get("status", "pendente")
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)",
                        (title, description, status))
            conn.commit()
            task_id = cur.lastrowid
            cur.execute("SELECT id, title, description, status, created_at FROM tasks WHERE id = ?", (task_id,))
            row = cur.fetchone()
            conn.close()
            task = dict(zip(["id","title","description","status","created_at"], row))
            return self._send(201, task)
        else:
            return self._send(404, {"error": "rota não encontrada"})

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/tasks":
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT id, title, description, status, created_at FROM tasks ORDER BY id")
            rows = cur.fetchall()
            conn.close()
            tasks = [dict(zip(["id","title","description","status","created_at"], r)) for r in rows]
            return self._send(200, {"tasks": tasks})
        m = re.match(r"^/tasks/(\d+)$", parsed.path)
        if m:
            task_id = int(m.group(1))
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT id, title, description, status, created_at FROM tasks WHERE id = ?", (task_id,))
            row = cur.fetchone()
            conn.close()
            if not row:
                return self._send(404, {"error": "tarefa não encontrada"})
            task = dict(zip(["id","title","description","status","created_at"], row))
            return self._send(200, task)
        return self._send(404, {"error": "rota não encontrada"})

    def do_PUT(self):
        m = re.match(r"^/tasks/(\d+)$", self.path)
        if not m:
            return self._send(404, {"error": "rota não encontrada"})
        task_id = int(m.group(1))
        body = self._read_json()
        if body is None:
            return self._send(400, {"error": "corpo JSON inválido ou ausente"})
        fields = {}
        allowed = {"title","description","status"}
        for k in allowed:
            if k in body:
                fields[k] = body[k]
        if not fields:
            return self._send(400, {"error": "nenhum campo para atualizar"})
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
        if not cur.fetchone():
            conn.close()
            return self._send(404, {"error": "tarefa não encontrada"})
        sets = ", ".join([f"{k} = ?" for k in fields.keys()])
        params = list(fields.values()) + [task_id]
        cur.execute(f"UPDATE tasks SET {sets} WHERE id = ?", params)
        conn.commit()
        cur.execute("SELECT id, title, description, status, created_at FROM tasks WHERE id = ?", (task_id,))
        row = cur.fetchone()
        conn.close()
        task = dict(zip(["id","title","description","status","created_at"], row))
        return self._send(200, task)

    def do_DELETE(self):
        m = re.match(r"^/tasks/(\d+)$", self.path)
        if not m:
            return self._send(404, {"error": "rota não encontrada"})
        task_id = int(m.group(1))
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
        if not cur.fetchone():
            conn.close()
            return self._send(404, {"error": "tarefa não encontrada"})
        cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        return self._send(204, None)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self._send(204, None)

if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except:
            pass
    init_db()
    server = HTTPServer(("", port), TaskHandler)
    print(f"Servidor rodando em http://localhost:{port} (DB: {DB_PATH})")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Encerrando servidor...")
        server.server_close()
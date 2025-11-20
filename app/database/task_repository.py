from app.database.connection import get_connection
from app.models.task import Task

class TaskRepository:
    """Responsável por todas as operações de banco de dados relacionadas a tarefas"""
    
    @staticmethod
    def create(task):
        """
        Cria uma nova tarefa no banco de dados
        Retorna: Task com ID preenchido
        """
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)",
                (task.title, task.description, task.status)
            )
            task_id = cur.lastrowid
            
            # Buscar tarefa criada
            cur.execute(
                "SELECT id, title, description, status, created_at FROM tasks WHERE id = ?",
                (task_id,)
            )
            row = cur.fetchone()
            
            return Task.from_db_row(row)
    
    @staticmethod
    def find_all():
        """
        Retorna todas as tarefas
        Retorna: Lista de Task
        """
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, title, description, status, created_at FROM tasks ORDER BY id"
            )
            rows = cur.fetchall()
            
            return [Task.from_db_row(row) for row in rows]
    
    @staticmethod
    def find_by_id(task_id):
        """
        Busca uma tarefa por ID
        Retorna: Task ou None se não encontrado
        """
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, title, description, status, created_at FROM tasks WHERE id = ?",
                (task_id,)
            )
            row = cur.fetchone()
            
            return Task.from_db_row(row)
    
    @staticmethod
    def update(task_id, updates):
        """
        Atualiza uma tarefa
        Args:
            task_id: ID da tarefa
            updates: dict com campos a atualizar (title, description, status)
        Retorna: Task atualizado ou None se não encontrado
        """
        # Verificar se tarefa existe
        if not TaskRepository.find_by_id(task_id):
            return None
        
        with get_connection() as conn:
            cur = conn.cursor()
            
            # Construir query dinâmica
            allowed_fields = {"title", "description", "status"}
            fields_to_update = {k: v for k, v in updates.items() if k in allowed_fields}
            
            if not fields_to_update:
                return TaskRepository.find_by_id(task_id)
            
            set_clause = ", ".join([f"{field} = ?" for field in fields_to_update.keys()])
            values = list(fields_to_update.values()) + [task_id]
            
            cur.execute(
                f"UPDATE tasks SET {set_clause} WHERE id = ?",
                values
            )
            
            # Retornar tarefa atualizada
            return TaskRepository.find_by_id(task_id)
    
    @staticmethod
    def delete(task_id):
        """
        Deleta uma tarefa
        Retorna: True se deletado, False se não encontrado
        """
        # Verificar se tarefa existe
        if not TaskRepository.find_by_id(task_id):
            return False
        
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            
            return True
    
    @staticmethod
    def exists(task_id):
        """
        Verifica se uma tarefa existe
        Retorna: bool
        """
        return TaskRepository.find_by_id(task_id) is not None
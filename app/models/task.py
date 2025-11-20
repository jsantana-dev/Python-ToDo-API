class Task:
    """Representa uma tarefa no sistema"""
    
    def __init__(self, id=None, title=None, description=None, status="pendente", created_at=None):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.created_at = created_at
    
    def to_dict(self):
        """Converte a tarefa para dicionário"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at
        }
    
    @staticmethod
    def from_dict(data):
        """Cria uma tarefa a partir de um dicionário"""
        return Task(
            id=data.get("id"),
            title=data.get("title"),
            description=data.get("description"),
            status=data.get("status", "pendente"),
            created_at=data.get("created_at")
        )
    
    @staticmethod
    def from_db_row(row):
        """Cria uma tarefa a partir de uma linha do banco"""
        if not row:
            return None
        return Task(
            id=row[0],
            title=row[1],
            description=row[2],
            status=row[3],
            created_at=row[4]
        )
    
    def __repr__(self):
        return f"Task(id={self.id}, title='{self.title}', status='{self.status}')"
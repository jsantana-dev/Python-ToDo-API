VALID_STATUSES = ["pendente", "em_andamento", "completo", "cancelado"]

class TaskValidator:
    """Validador de dados de tarefas"""
    
    @staticmethod
    def validate_create(data):
        """
        Valida dados para criação de tarefa
        Retorna: (bool, str) - (válido, mensagem_erro)
        """
        if not data:
            return False, "Corpo da requisição vazio"
        
        # Validar título
        if "title" not in data:
            return False, "Campo 'title' é obrigatório"
        
        if not data["title"] or not data["title"].strip():
            return False, "Campo 'title' não pode estar vazio"
        
        if len(data["title"]) > 200:
            return False, "Campo 'title' deve ter no máximo 200 caracteres"
        
        # Validar descrição (opcional)
        if "description" in data and data["description"]:
            if len(data["description"]) > 1000:
                return False, "Campo 'description' deve ter no máximo 1000 caracteres"
        
        # Validar status (opcional)
        if "status" in data and data["status"]:
            if data["status"] not in VALID_STATUSES:
                return False, f"Status inválido. Use: {', '.join(VALID_STATUSES)}"
        
        return True, None
    
    @staticmethod
    def validate_update(data):
        """
        Valida dados para atualização de tarefa
        Retorna: (bool, str) - (válido, mensagem_erro)
        """
        if not data:
            return False, "Corpo da requisição vazio"
        
        # Pelo menos um campo deve ser fornecido
        allowed_fields = {"title", "description", "status"}
        has_field = any(field in data for field in allowed_fields)
        
        if not has_field:
            return False, "Nenhum campo válido para atualizar (title, description, status)"
        
        # Validar título (se fornecido)
        if "title" in data:
            if not data["title"] or not data["title"].strip():
                return False, "Campo 'title' não pode estar vazio"
            
            if len(data["title"]) > 200:
                return False, "Campo 'title' deve ter no máximo 200 caracteres"
        
        # Validar descrição (se fornecido)
        if "description" in data and data["description"]:
            if len(data["description"]) > 1000:
                return False, "Campo 'description' deve ter no máximo 1000 caracteres"
        
        # Validar status (se fornecido)
        if "status" in data:
            if data["status"] not in VALID_STATUSES:
                return False, f"Status inválido. Use: {', '.join(VALID_STATUSES)}"
        
        return True, None
    
    @staticmethod
    def validate_id(task_id):
        """
        Valida ID da tarefa
        Retorna: (bool, str) - (válido, mensagem_erro)
        """
        if not isinstance(task_id, int) or task_id <= 0:
            return False, "ID inválido"
        
        return True, None
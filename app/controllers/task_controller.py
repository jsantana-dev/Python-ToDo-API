from app.models.task import Task
from app.database.task_repository import TaskRepository
from app.validators.task_validator import TaskValidator
from app.utils.response import ResponseBuilder

class TaskController:
    """Controlador de tarefas - gerencia lógica de negócio"""
    
    @staticmethod
    def create(handler, body):
        """
        Cria uma nova tarefa
        Args:
            handler: HTTPRequestHandler
            body: dict com dados da tarefa
        """
        try:
            # Validar dados
            is_valid, error_msg = TaskValidator.validate_create(body)
            if not is_valid:
                return ResponseBuilder.bad_request(handler, error_msg)
            
            # Criar tarefa
            task = Task.from_dict(body)
            created_task = TaskRepository.create(task)
            
            # Retornar sucesso
            return ResponseBuilder.created(handler, created_task.to_dict())
        
        except Exception as e:
            print(f"Erro ao criar tarefa: {e}")
            return ResponseBuilder.internal_error(handler)
    
    @staticmethod
    def list_all(handler):
        """
        Lista todas as tarefas
        Args:
            handler: HTTPRequestHandler
        """
        try:
            tasks = TaskRepository.find_all()
            tasks_data = [task.to_dict() for task in tasks]
            
            return ResponseBuilder.success(handler, {"tasks": tasks_data})
        
        except Exception as e:
            print(f"Erro ao listar tarefas: {e}")
            return ResponseBuilder.internal_error(handler)
    
    @staticmethod
    def get_by_id(handler, task_id):
        """
        Busca uma tarefa por ID
        Args:
            handler: HTTPRequestHandler
            task_id: ID da tarefa
        """
        try:
            # Validar ID
            is_valid, error_msg = TaskValidator.validate_id(task_id)
            if not is_valid:
                return ResponseBuilder.bad_request(handler, error_msg)
            
            # Buscar tarefa
            task = TaskRepository.find_by_id(task_id)
            
            if not task:
                return ResponseBuilder.not_found(handler, "Tarefa não encontrada")
            
            return ResponseBuilder.success(handler, task.to_dict())
        
        except Exception as e:
            print(f"Erro ao buscar tarefa: {e}")
            return ResponseBuilder.internal_error(handler)
    
    @staticmethod
    def update(handler, task_id, body):
        """
        Atualiza uma tarefa
        Args:
            handler: HTTPRequestHandler
            task_id: ID da tarefa
            body: dict com campos a atualizar
        """
        try:
            # Validar ID
            is_valid, error_msg = TaskValidator.validate_id(task_id)
            if not is_valid:
                return ResponseBuilder.bad_request(handler, error_msg)
            
            # Validar dados de atualização
            is_valid, error_msg = TaskValidator.validate_update(body)
            if not is_valid:
                return ResponseBuilder.bad_request(handler, error_msg)
            
            # Atualizar tarefa
            updated_task = TaskRepository.update(task_id, body)
            
            if not updated_task:
                return ResponseBuilder.not_found(handler, "Tarefa não encontrada")
            
            return ResponseBuilder.success(handler, updated_task.to_dict())
        
        except Exception as e:
            print(f"Erro ao atualizar tarefa: {e}")
            return ResponseBuilder.internal_error(handler)
    
    @staticmethod
    def delete(handler, task_id):
        """
        Deleta uma tarefa
        Args:
            handler: HTTPRequestHandler
            task_id: ID da tarefa
        """
        try:
            # Validar ID
            is_valid, error_msg = TaskValidator.validate_id(task_id)
            if not is_valid:
                return ResponseBuilder.bad_request(handler, error_msg)
            
            # Deletar tarefa
            deleted = TaskRepository.delete(task_id)
            
            if not deleted:
                return ResponseBuilder.not_found(handler, "Tarefa não encontrada")
            
            return ResponseBuilder.no_content(handler)
        
        except Exception as e:
            print(f"Erro ao deletar tarefa: {e}")
            return ResponseBuilder.internal_error(handler)
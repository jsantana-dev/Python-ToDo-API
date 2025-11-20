import re
from app.controllers.task_controller import TaskController
from app.utils.response import ResponseBuilder

class Router:
    """Gerenciador de rotas da API"""
    
    @staticmethod
    def route_post(handler, path, body):
        """Roteia requisições POST"""
        if path == "/tasks":
            return TaskController.create(handler, body)
        else:
            return ResponseBuilder.not_found(handler, "Rota não encontrada")
    
    @staticmethod
    def route_get(handler, path):
        """Roteia requisições GET"""
        # GET /tasks - listar todas
        if path == "/tasks":
            return TaskController.list_all(handler)
        
        # GET /tasks/<id> - buscar por ID
        match = re.match(r"^/tasks/(\d+)$", path)
        if match:
            task_id = int(match.group(1))
            return TaskController.get_by_id(handler, task_id)
        
        return ResponseBuilder.not_found(handler, "Rota não encontrada")
    
    @staticmethod
    def route_put(handler, path, body):
        """Roteia requisições PUT"""
        # PUT /tasks/<id> - atualizar
        match = re.match(r"^/tasks/(\d+)$", path)
        if match:
            task_id = int(match.group(1))
            return TaskController.update(handler, task_id, body)
        
        return ResponseBuilder.not_found(handler, "Rota não encontrada")
    
    @staticmethod
    def route_delete(handler, path):
        """Roteia requisições DELETE"""
        # DELETE /tasks/<id> - deletar
        match = re.match(r"^/tasks/(\d+)$", path)
        if match:
            task_id = int(match.group(1))
            return TaskController.delete(handler, task_id)
        
        return ResponseBuilder.not_found(handler, "Rota não encontrada")
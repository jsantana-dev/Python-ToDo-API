import json

class ResponseBuilder:
    """Construtor de respostas HTTP padronizadas"""
    
    @staticmethod
    def success(handler, data, status_code=200):
        """
        Envia resposta de sucesso
        Args:
            handler: HTTPRequestHandler
            data: dados a retornar (dict, list ou None)
            status_code: código HTTP (200, 201, 204, etc)
        """
        handler.send_response(status_code)
        handler.send_header("Content-Type", "application/json; charset=utf-8")
        handler.end_headers()
        
        if data is not None and status_code != 204:
            response_body = json.dumps(data, ensure_ascii=False)
            handler.wfile.write(response_body.encode("utf-8"))
    
    @staticmethod
    def error(handler, message, status_code=400):
        """
        Envia resposta de erro
        Args:
            handler: HTTPRequestHandler
            message: mensagem de erro
            status_code: código HTTP (400, 404, 500, etc)
        """
        handler.send_response(status_code)
        handler.send_header("Content-Type", "application/json; charset=utf-8")
        handler.end_headers()
        
        error_data = {"error": message}
        response_body = json.dumps(error_data, ensure_ascii=False)
        handler.wfile.write(response_body.encode("utf-8"))
    
    @staticmethod
    def not_found(handler, message="Recurso não encontrado"):
        """Envia resposta 404"""
        ResponseBuilder.error(handler, message, 404)
    
    @staticmethod
    def bad_request(handler, message="Requisição inválida"):
        """Envia resposta 400"""
        ResponseBuilder.error(handler, message, 400)
    
    @staticmethod
    def created(handler, data):
        """Envia resposta 201 (Created)"""
        ResponseBuilder.success(handler, data, 201)
    
    @staticmethod
    def no_content(handler):
        """Envia resposta 204 (No Content)"""
        ResponseBuilder.success(handler, None, 204)
    
    @staticmethod
    def internal_error(handler, message="Erro interno do servidor"):
        """Envia resposta 500"""
        ResponseBuilder.error(handler, message, 500)
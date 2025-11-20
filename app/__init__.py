__version__ = "2.0.0"
__author__ = "Jamylle Santana"

# app/models/__init__.py
"""
Models da aplicação
"""
from app.models.task import Task

__all__ = ["Task"]

# app/controllers/__init__.py
"""
Controllers da aplicação
"""
from app.controllers.task_controller import TaskController

__all__ = ["TaskController"]

# app/database/__init__.py
"""
Camada de acesso a dados
"""
from app.database.connection import init_database, get_connection
from app.database.task_repository import TaskRepository

__all__ = ["init_database", "get_connection", "TaskRepository"]

# app/validators/__init__.py
"""
Validadores da aplicação
"""
from app.validators.task_validator import TaskValidator

__all__ = ["TaskValidator"]

# app/utils/__init__.py
"""
Utilitários da aplicação
"""
from app.utils.response import ResponseBuilder

__all__ = ["ResponseBuilder"]
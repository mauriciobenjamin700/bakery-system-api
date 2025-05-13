import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = os.getenv("LOG_DIR", "app/logs")
INFO_LOG_FILE = os.path.join(LOG_DIR, "info.log")
ERROR_LOG_FILE = os.path.join(LOG_DIR, "error.log")

os.makedirs(LOG_DIR, exist_ok=True)
open(INFO_LOG_FILE, "a").close()
open(ERROR_LOG_FILE, "a").close()
os.chmod(LOG_DIR, 0o755)  # Permissões para o diretório
os.chmod(INFO_LOG_FILE, 0o644)  # Permissões para o arquivo info.log
os.chmod(ERROR_LOG_FILE, 0o644)  # Permissões para o arquivo error.log


class LogManager:
    """
    A class to manage logging in the application.
    Provides methods to log messages at different levels (INFO, ERROR, etc.)
    to separate log files.

    - Attributes:
        - _loggers:: dict: A dictionary to store logger instances.

    - Methods:
        - _get_logger(level: str, file_path: str):
            Returns a logger instance for the specified level and file path.
        - create_info_log(action: str, local: str, agente: str, agente_role: str, request_time: float):
            Logs an INFO message to the info log file.
        - create_error_log(action: str, agente: str, agente_role: str, status: int, detail: str):
            Logs an ERROR message to the error log file.
    """

    _loggers = {}

    @classmethod
    def _get_logger(cls, level: str, file_path: str):
        if level not in cls._loggers:
            logger = logging.getLogger(level)
            logger.setLevel(getattr(logging, level))

            # Configuração do handler com rotação de arquivos
            handler = RotatingFileHandler(
                file_path, maxBytes=5_000_000, backupCount=5
            )
            formatter = logging.Formatter(
                "%(asctime)s---%(levelname)s---%(message)s"
            )
            handler.setFormatter(formatter)

            logger.addHandler(handler)
            cls._loggers[level] = logger

        return cls._loggers[level]

    @classmethod
    def create_info_log(
        cls,
        action: str,
        local: str,
        agente: str,
        agente_role: str,
        request_time: float,
    ):
        """
        Log an INFO message.

        - Args:
            - action:: str: The action being logged.
            - local:: str: The local context of the action.
            - agente:: str: The agent involved in the action.
            - agente_role:: str: The role of the agent.
            - request_time:: float: The time taken for the request.
        - Returns:
            - None
        """
        log_message = (
            f"{action}---{local}---{agente}---{agente_role}---{request_time}"
        )
        logger = cls._get_logger("INFO", "app/logs/info.log")
        logger.info(log_message)

    @classmethod
    def create_error_log(
        cls,
        action: str,
        agente: str,
        agente_role: str,
        status: int,
        detail: str,
    ):
        """
        Log an ERROR message.

        - Args:
            - action:: str: The action being logged.
            - agente:: str: The agent involved in the action.
            - agente_role:: str: The role of the agent.
            - status:: int: The HTTP status code.
            - detail:: str: Additional details about the error.
        - Returns:
            - None
        """
        log_message = (
            f"{action}---{agente}---{agente_role}---{status}---{detail}"
        )
        logger = cls._get_logger("ERROR", "app/logs/error.log")
        logger.error(log_message)

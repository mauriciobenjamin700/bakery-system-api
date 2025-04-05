import asyncio
import uvicorn
from app.db.configs.connection import db
from app.main import app

async def create_tables():
    max_retries = 5
    for attempt in range(max_retries):
        try:
            await db.create_tables()
            print("Tabelas criadas com sucesso!")
            break
        except Exception as e:
            print(f"Tentativa {attempt + 1} falhou: {str(e)}")
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 * (attempt + 1))

async def main():
    # Inicializa o banco de dados
    await create_tables()

    # Configura o servidor UVicorn para rodar em um event loop separado
    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        log_config="logging_config.yaml"  # Apontar para o arquivo de configuração de log
    )

    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())

    """
    log_level pode ter os seguintes valores:
        "critical": Registra apenas mensagens críticas.
        "error": Registra mensagens de erro e mensagens mais graves.
        "warning": Registra mensagens de aviso, erro e mensagens mais graves.
        "info": Registra mensagens informativas, de aviso, erro e mensagens mais graves.
        "debug": Registra mensagens de depuração, informativas, de aviso, erro e mensagens mais graves.
        "trace": Registra todas as mensagens, incluindo mensagens de rastreamento detalhadas.
    """

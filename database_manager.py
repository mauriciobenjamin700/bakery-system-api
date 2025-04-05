from asyncio import run

from app.db.configs.connection import db


run(db.create_tables())

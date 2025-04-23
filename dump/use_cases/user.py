from src.models.database.models import User
from src.controllers.services.check_fields import check_fields_formated
from src.models.schemas.user import *

class UseCaseUser():
    def __init__(self,db_session) -> None:
        self.db_session = db_session
        if len(self.db_session.query(User).all()) == 0:
            data_insert = User(login="Jasson", password="admin", level=1)
            data_insert_b = User(login="Funcionario",password="func",level=2)
            self.db_session.add_all([data_insert,data_insert_b])
            self.db_session.commit()

    def add_user(self,UserRequest:UserRequest):
        try:
            check_fields_formated(
            UserRequest,
            ["login", "password", "level"],
            {"login":"Login invalido", "password":"Password invalido", "level":"Level invalido"})
            data_insert = User(**UserRequest.__dict__   )
            self.db_session.add(data_insert)
            self.db_session.commit()   
            
            return {"msg":"Usuario criado com sucesso"}         
            
        except Exception as e:
            self.db_session.rollback()
            raise e


    def get_user(self,login: str):
        try:
            return self.db_session.query(User).filter_by(login=login).first()
        except Exception as e:
            raise e

    def delete_user(self,login: str):
        try:

            self.db_session.query(User).filter_by(login=login).delete()
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            raise e


    def login(self, UserLogin:UserLogin)->User:
        try:
            check_fields_formated(UserLogin,["login","password"],{"login":"Login invalido","password":"Password invalido"})
            return self.db_session.query(User).filter_by(login=UserLogin.login, password=UserLogin.password).first()
        except Exception as e:
            raise e
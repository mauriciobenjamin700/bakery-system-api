"""
Esse pacote contem todos as funções do objeto Ingredient

classes:
    UseCaseIngredient

"""

from sqlalchemy import func 

from src.models.database.models import (
    Ingredient as IngredientModel, 
    LoteIngredient as LoteIngredientModel)
from src.models.schemas.ingredient import (
    IngredientRequest,
    IngredientUpdate,
    IngredientResponse,
    LoteIngredientRequest,
    LoteIngredientUpdate,
    LoteIngredientResponse,
)
from datetime import datetime

class UseCaseIngredient():
    """
    Essa classe contém os casos de uso do objeto Ingredient

    functions:
        - ingredient_add(IngredientRequest)
        - ingredient_delete(IngredientDelete)
        - ingredient_update(IngredientUpdate)
        - lote_add(LoteIngredientRequest)
        - lote_delete(LoteIngredientDelete)
        - lote_update(LoteIngredientUpdate)
        - ingredient_get(IngredientOut)
        - ingredient_get_all()
    """
    DEFAULT_MARK = "-"

    def __init__(self,db_session):
        self.db_session = db_session

    def ingredient_add(self,ingredient_request:IngredientRequest) -> dict:
        """
        A função serve para adicionar um ingrediente ao banco de dados, recebendo um IngredientRequest
        com todos os dados necessarios. A função cadastra automaticamente um lote inicial para aquele produto
        e caso o produto já exista no banco é criado um lote daquele produto. \n Para ser considerado o mesmo
        produto é necessario ter os seguintes campos iguais:\n
        \t Name\n\t Mark\n\t Measure


        - Parameter:
            - ingredient_request: IngredientRequest

        - Returns:
            - {msg:response}: Dict (Um dicionario com uma mensagem de sucesso)
            - Exceptions:
                - Algum campo obrigatorio faltando ou invalido
        
        """
        try:
           
            if not ingredient_request.mark:
                ingredient_request.mark = UseCaseIngredient.DEFAULT_MARK

            ingredient_on_db = self.db_session.query(IngredientModel).filter_by(
                name=ingredient_request.name,
                mark=ingredient_request.mark,
                measure=ingredient_request.measure
            ).first()

            data_insert_ingredient = ingredient_request.dict_nofilter()
            data_insert_lote = ingredient_request.dict_nofilter()

            for _ in range(7):
                data_insert_lote.pop(next(iter(data_insert_lote)))

            if ingredient_on_db:
                
                self.db_session.add(LoteIngredientModel(**data_insert_lote,id_ingredient=ingredient_on_db.id,register_date=datetime.now()))
                
                self.db_session.commit()
                
                return {"msg":"Ingrediente já existe, então o ingrediente foi salvo como lote"}

            for _ in range(2):
                data_insert_ingredient.popitem()
                
            ingredient_model = IngredientModel(**data_insert_ingredient)

            self.db_session.add(ingredient_model)
            self.db_session.flush()

            self.db_session.add(LoteIngredientModel(**data_insert_lote,id_ingredient=ingredient_model.id,register_date=datetime.now()))

            self.db_session.commit()
            return {"msg": "Ingrediente cadastrado com sucesso"}

        except Exception as e:
            self.db_session.rollback()
            raise e
        

    def ingredient_delete(self, ingredient_id:int) -> dict:
        """
        A função serve para remover um ingrediente do banco de dados, recebendo um 
        IngredientDelete com o id do ingrediente a ser deletado.

        - Parameter:
            - ingredient_delete: IngredientDelete (Contém o ID do ingrediente que será deletado)
        
        - Returns:
            - {msg:response}: Dict (Um dicionário com uma mensagem de sucesso)

        - Exceptions:
            - ID inválido ou faltando
            - Ingrediente não encontrado
        """
        try:
            # Verifica se o atributo 'id' está presente, se não é None e se é do tipo inteiro.

            
            # Busca o ingrediente no banco de dados usando o id fornecido.
            ingredient = self.db_session.query(IngredientModel).filter_by(id=ingredient_id).first()
            
            # Caso o ingrediente não seja encontrado, uma exceção é levantada.
            if not ingredient:
                raise Exception("Ingrediente não encontrado")
            
            # Remove o ingrediente do banco de dados.
            self.db_session.delete(ingredient)
            self.db_session.commit()

            # Retorna uma mensagem de sucesso.
            return {"msg":"Ingrediente removido com sucesso"}
        
        except Exception as e:
            # Faz o rollback no banco de dados em caso de erro e levanta a exceção.
            self.db_session.rollback()
            raise e

        
    
    def ingredient_update(self, ingredient_update:IngredientUpdate) -> dict:
        """
        A função serve para atualizar os dados de um ingrediente no banco de dados, 
        recebendo um IngredientUpdate com os novos valores. 

        - Parameter:
            - ingredient_update: IngredientUpdate (Contém o ID do ingrediente a ser atualizado e os novos valores)

        - Returns:
            - {msg:response}: Dict (Um dicionário com uma mensagem de sucesso)

        - Exceptions:
            - Atributo obrigatório 'id' faltando ou inválido
            - Ingrediente não encontrado
        """
        try:
            # Converte os dados de 'ingredient_update' em um dicionário.
            data_update = ingredient_update.dict()
            
            # Busca o ingrediente no banco de dados pelo id fornecido.
            ingredient = self.db_session.query(IngredientModel).filter_by(id=ingredient_update.id).first()

            # Levanta uma exceção caso o ingrediente não seja encontrado.
            if not ingredient:
                raise Exception("Ingrediente não encontrado")

            # Atualiza os campos do ingrediente com os novos valores fornecidos.
            for field, value in data_update.items():
                setattr(ingredient, field, value)
            
            # Salva as mudanças no banco de dados.
            self.db_session.commit()
            self.db_session.refresh(ingredient)  # Atualiza o objeto com os dados salvos no banco de dados.
            
            # Retorna uma mensagem de sucesso.
            return {"msg": "Ingrediente atualizado com sucesso"}
        
        except Exception as e:
            # Faz rollback no banco de dados em caso de erro e levanta a exceção.
            self.db_session.rollback()
            raise e

    
    def lote_add(self, lote_ingredient_request:LoteIngredientRequest) -> dict:
        """
        A função serve para adicionar um novo lote de um ingrediente existente no banco de dados, 
        recebendo um LoteIngredientRequest com os dados necessários. 

        - Parameter:
            - lote_ingredient_request: LoteIngredientRequest (Contém os valores e a quantidade para o novo lote)

        - Returns:
            - {msg:response}: Dict (Um dicionário com uma mensagem de sucesso)

        - Exceptions:
            - Algum campo obrigatório faltando ou inválido
            - Ingrediente não encontrado
        """
        try:

            # Busca o ingrediente no banco de dados utilizando o id fornecido.
            ingredient_on_db = self.db_session.query(IngredientModel).filter_by(
                id=lote_ingredient_request.id_ingredient).first()

            # Se o ingrediente for encontrado, adiciona o novo lote.
            if ingredient_on_db:
                
                self.db_session.add(
                    
                    LoteIngredientModel(
                        **lote_ingredient_request.dict(), 
                        register_date=datetime.now()
                        )
                    )
                
                self.db_session.commit()
                
                return {"msg": "Lote cadastrado com sucesso"}
            
            # Se o ingrediente não for encontrado, levanta uma exceção.
            raise ValueError("Ingrediente não encontrado")

        except Exception as e:
            # Faz rollback no banco de dados em caso de erro e levanta a exceção.
            self.db_session.rollback()
            raise e


    def lote_delete(self, lote_id: int) -> dict:
        """
        A função serve para remover um lote de ingrediente do banco de dados, 
        recebendo um LoteIngredientDelete com o id do lote a ser deletado.

        - Parameter:
            - lote_delete: LoteIngredientDelete (Contém o ID do lote que será deletado)
        
        - Returns:
            - {msg:response}: Dict (Um dicionário com uma mensagem de sucesso)

        - Exceptions:
            - ID inválido ou faltando
            - Lote não encontrado
        """
        try:

            # Busca o lote no banco de dados usando o id fornecido.
            lote = self.db_session.query(LoteIngredientModel).filter_by(id=lote_id).first()
            
            # Caso o lote não seja encontrado, uma exceção é levantada.
            if not lote:
                raise Exception("Lote não encontrado")
            
            # Remove o lote do banco de dados.
            self.db_session.delete(lote)
            self.db_session.commit()

            # Retorna uma mensagem de sucesso.
            return {"msg":"Lote removido com sucesso"}
        
        except Exception as e:
            # Faz rollback no banco de dados em caso de erro e levanta a exceção.
            self.db_session.rollback()
            raise f"Erro ao deletar lote: {e}"


    def lote_update(self, lote_update:LoteIngredientUpdate) -> dict:
        """
        A função serve para atualizar os dados de um lote de ingrediente no banco de dados, 
        recebendo um LoteIngredientUpdate com os novos valores. 

        - Parameter:
            - lote_update: LoteIngredientUpdate (Contém o ID do lote a ser atualizado e os novos valores)

        - Returns:
            - {msg:response}: Dict (Um dicionário com uma mensagem de sucesso)

        - Exceptions:
            - Atributo obrigatório 'id' faltando ou inválido
            - Lote do ingrediente não encontrado
        """
        try:

            # Converte os dados de 'lote_update' em um dicionário.
            data_update = lote_update.dict()
            
            # Busca o lote no banco de dados pelo id fornecido.
            lote = self.db_session.query(LoteIngredientModel).filter_by(id=lote_update.id).first()

            # Levanta uma exceção caso o lote não seja encontrado.
            if not lote:
                raise Exception("Lote do ingrediente não encontrado")

            # Atualiza os campos do lote com os novos valores fornecidos.
            for field, value in data_update.items():
                setattr(lote, field, value)
            
            # Salva as mudanças no banco de dados.
            self.db_session.commit()
            self.db_session.refresh(lote)  # Atualiza o objeto com os dados salvos no banco de dados.
            
            # Retorna uma mensagem de sucesso.
            return {"msg": "Lote atualizado com sucesso"}

        except Exception as e:
            # Faz rollback no banco de dados em caso de erro e levanta a exceção.
            self.db_session.rollback()
            raise f"Erro ao atualizar lote: {e}"

    def ingredient_get(self, ingredient_id) -> IngredientResponse:
        """
        A função serve para buscar um ingrediente no banco de dados, 
        retornando uma lista de respostas contendo as informações do ingrediente.

        - Parameter:
            - ingredient_out: IngredientOut (Contém o ID do ingrediente que será buscado)
        
        - Returns:
            - list[IngredientResponse]: Lista com as respostas que incluem as informações do ingrediente e seus lotes

        - Exceptions:
            - Atributo obrigatório 'id' faltando ou inválido
            - Ingrediente não encontrado
        """
        try:
            
            # Busca o ingrediente no banco de dados pelo id fornecido.
            ingredient = self.db_session.query(IngredientModel).filter_by(id=ingredient_id).first()
            
            # Levanta uma exceção caso o ingrediente não seja encontrado.
            if not ingredient:
                raise Exception("Ingrediente não encontrado.")
            
            # Busca todos os lotes relacionados ao ingrediente.
            lotes = self.db_session.query(LoteIngredientModel).filter_by(id_ingredient=ingredient_id).all()

            quantity = 0
            
            for lote in lotes:
                quantity += lote.quantity
                
            return IngredientResponse(
                **ingredient.dict(),
                quantity=quantity
            )
            

        except Exception as e:
            # Levanta a exceção em caso de erro.
            raise e
        
    def _get_lote_ingredient(self,  ingredient_id: int) -> list[LoteIngredientResponse]:
        """
        A função serve para buscar um lote de um ingrediente no banco de dados, 
        retornando uma lista de respostas contendo as informações do lote.

        - Parameter:
            - ingredient_id: int (O ID do ingrediente)
        
        - Returns:
            - list[LoteIngredientResponse]: Lista com as respostas que incluem as informações do lote

        - Exceptions:
            - Ingrediente não encontrado
            - Nenhum lote encontrado
        """
        try:
            
            # Busca todos os lotes relacionados ao ingrediente.
            lotes = self.db_session.query(LoteIngredientModel).filter_by(id_ingredient=ingredient_id).all()
            
            # Verifica se há lotes cadastrados para o ingrediente.
            if not lotes:
                raise Exception("Nenhum lote encontrado.")
            
            # Monta a resposta contendo o produto e seus lotes.
            response = []
            for lote in lotes:
                response.append(LoteIngredientResponse(**lote.dict()))
            
            return response

        except Exception as e:
            # Levanta a exceção em caso de erro.
            raise Exception(f"Erro ao buscar lote: {e}")
        
    def get_ingredient_and_lots(self, ingredient_id: int) -> dict:

        """
        
        Busca um ingrediente e seus lotes associados
        
        - Args:
            - ingredient_id: int (O id do ingrediente)
        
        - Returns:
            dict[
                "ingredient": IngredientResponse,
                "lotes": list[LoteIngredientResponse]
            ]
        """

        try:

            # Busca o produto no banco de dados
            ingredient = self.db_session.query(IngredientModel).filter_by(id=ingredient_id).first()

            # Verifica se o produto existe
            if not ingredient:
                raise Exception(f"Ingrediente com id  não encontrado.")

            total_quantity = 0
            lotes = []
            try:
                lotes = self._get_lote_ingredient(ingredient_id)
                for lote in lotes:
                    total_quantity += lote.quantity
            except:
                pass

            ingredient_response = IngredientResponse(**ingredient.dict(),quantity=total_quantity)
            
            return {"ingredient":ingredient_response,"lotes":lotes}

        except Exception as e:
            raise e
        
    def ingredient_get_all(self) -> list[dict]:
        """
        A função serve para buscar todos os ingredientes do banco de dados, 
        junto com seus respectivos lotes, retornando uma lista de respostas.

        - Returns:
            - list[IngredientResponse]: Lista com as respostas que incluem as informações de todos os ingredientes e seus lotes
        
        - Exceptions:
            - Nenhum ingrediente encontrado
            - Ingredientes encontrados, mas nenhum lote foi associado a eles
        """
        try:
            # Busca todos os ingredientes no banco de dados.
            ingredients = self.db_session.query(IngredientModel).all()
            
            # Verifica se há ingredientes cadastrados, caso contrário, levanta uma exceção.
            if not ingredients:
                raise Exception(f"Nenhum ingrediente encontrado") 

            response = []
            
            for ingrendient in ingredients:
                response.append(
                    self.get_ingredient_and_lots(ingrendient.id)
                )
                
            return response

        except Exception as e:
            raise e

    def get_db_all_lote_ingredient(self) -> list[LoteIngredientModel]:
        lotes = self.db_session.query(LoteIngredientModel).all()
        return lotes
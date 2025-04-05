"""
Esse pacote contem todos as funções do objeto Portion

classes:
    UseCasePortion

"""

from src.controllers.services.check_fields import check_fields_formated

from src.models.schemas.portion import *
from src.models.database.models import (
    Ingredient as IngredientModel,
    Recipe as RecipeModel,
    Portion as PortionModel
)
from src.models.schemas.portion import PortionResponse
class UseCasePortion():
    """
    Essa classe contém os casos de uso do objeto Portion

    functions:
        - portion_add(PortionRequest)
        - portion_delete(PortionDelete)
        - portion_update(PortionUpdate)
        - portion_get(PortionOut)
        - portion_get_all(PortionOut)
    """
    def __init__(self,db_session):
        self.db_session = db_session
    
    def portion_add(self, portion_request: PortionRequest):
        """
        A função serve para adicionar uma porção ao banco de dados, verificando se o ingrediente e a receita existem, 
        e certificando-se de que a porção não foi previamente cadastrada.

        - Parameter:
            - portion_request: PortionRequest (Contém os dados necessários para cadastrar uma porção)

        - Returns:
            - {msg: response}: Dict (Uma mensagem de sucesso indicando que a porção foi adicionada)
        
        - Exceptions:
            - Ingrediente não encontrado
            - Receita não encontrada
            - Porção já cadastrada
            - Algum campo obrigatório faltando ou inválido
        """
        try:
            # Verifica se os campos necessários estão preenchidos e formatados corretamente.
            check_fields_formated(portion_request, ['id_ingredient', 'id_recipe', 'quantity'], {
                'id_ingredient': 'O id do ingrediente está faltando',
                'id_recipe': 'O id da receita está faltando',
                'quantity': 'A quantidade utilizada na porção está faltando',
            })
            
            # Busca o ingrediente e a receita no banco de dados.
            ingredient = self.db_session.query(IngredientModel).filter_by(id=portion_request.id_ingredient).first()
            recipe = self.db_session.query(RecipeModel).filter_by(id=portion_request.id_recipe).first()

            # Levanta exceções caso o ingrediente ou a receita não sejam encontrados.
            if ingredient is None: 
                raise Exception("Ingrediente não encontrado")    
            if recipe is None:
                raise Exception("Receita não encontrada")
            
            # Tenta buscar a porção para garantir que ela ainda não foi cadastrada.
            try:
                self.portion_get(id_ingredient=ingredient.id, id_recipe=recipe.id)
            except:
                # Adiciona a porção se ela ainda não existir.
                self.db_session.add(PortionModel(**portion_request.dict(), ingredient_name=ingredient.name))
                self.db_session.commit()
                return {'msg': 'Porção adicionada com sucesso'}
            
            # Levanta exceção se a porção já foi cadastrada anteriormente.
            raise Exception("Porção já cadastrada")
        
        except Exception as e:
            # Levanta a exceção em caso de erro.
            raise e

        
    def portion_delete(self, portion_id):
        """
        A função serve para deletar uma porção do banco de dados, verificando se ela existe 
        e garantindo que o ID fornecido é válido.

        - Parameter:
            - portion_delete: PortionDelete (Contém o ID da porção a ser deletada)

        - Returns:
            - {msg: response}: Dict (Uma mensagem de sucesso indicando que a porção foi deletada)

        - Exceptions:
            - ID inválido ou ausente
            - Porção não encontrada
        """
        try:
            # Verifica se o atributo 'id' está presente, é válido e é um número inteiro.

            # Busca a porção no banco de dados pelo id fornecido.
            portion = self.db_session.query(PortionModel).filter_by(id=portion_id).first()

            # Levanta exceção caso a porção não seja encontrada.
            if portion is None:
                raise Exception("Porção não encontrada")
            
            # Remove a porção do banco de dados.
            self.db_session.delete(portion)

            # Retorna uma mensagem de sucesso.
            return {'msg': 'Porção deletada com sucesso'}
        
        except Exception as e:
            # Levanta a exceção em caso de erro.
            raise e



    def portion_update(self, portion_id: int, portion_quantity: float) -> dict[str, str]:
        """
        A função serve para atualizar a quantidade de uma porção existente no banco de dados, 
        verificando se a porção existe e se os campos obrigatórios foram preenchidos corretamente.

        - Parameter:
            - portion_update: PortionUpdate (Contém os dados necessários para atualizar uma porção)

        - Returns:
            - {msg: response}: Dict (Uma mensagem de sucesso indicando que a porção foi atualizada)

        - Exceptions:
            - Id da porção ausente ou inválido
            - Quantidade da porção ausente
            - Porção não encontrada
        """
        try:
            # Verifica se o id da porção foi fornecido.
            if portion_id is None:
                raise Exception("O id da porção é obrigatório")
            
            # Verifica se a quantidade da porção foi fornecida.
            if portion_quantity is None:
                raise Exception("A quantidade é obrigatória")
            
            
            # Busca a porção no banco de dados pelo id fornecido.
            portion = self.db_session.query(PortionModel).filter_by(id=portion_id).first()

            # Levanta exceção caso a porção não seja encontrada.
            if not portion:
                raise Exception("Porção não encontrada.")
            
            # Atualiza a quantidade da porção.
            portion.quantity = portion_quantity
            self.db_session.commit()
            self.db_session.refresh(portion)

            # Retorna uma mensagem de sucesso.
            return {'msg': 'Porção atualizada com sucesso'}

        except Exception as e:
            # Faz rollback em caso de erro.
            self.db_session.rollback()
            raise e

        
    def portion_get(self, id_ingredient: int, id_recipe: int) -> PortionResponse:
        """
        A função serve para buscar uma porção específica no banco de dados, 
        verificando se o id do ingrediente e da receita foram fornecidos corretamente.

        - Parameter:
            - portion_out: PortionOut (Contém os ids necessários para buscar a porção)

        - Returns:
            - PortionResponse: A resposta contendo os dados da porção encontrada

        - Exceptions:
            - Id do ingrediente ou da receita ausente
            - Porção não encontrada
        """
        try:
            # Verifica se o id do ingrediente foi fornecido.
            if id_ingredient is None:
                raise Exception('O id do ingrediente está faltando')
            
            # Verifica se o id da receita foi fornecido.
            if id_recipe is None:
                raise Exception('O id da receita é obrigatório')
            
            # Busca a porção no banco de dados com base nos ids fornecidos.
            portion = self.db_session.query(PortionModel).filter(
                PortionModel.id_ingredient == id_ingredient,
                PortionModel.id_recipe == id_recipe
            ).first()
            
            # Levanta exceção caso a porção não seja encontrada.
            if portion is None:
                raise Exception('Porção não encontrada')
            
            # Retorna a resposta com os dados da porção encontrada.
            return PortionResponse(**portion.dict())

        except Exception as e:
            # Levanta a exceção em caso de erro.
            raise e

        
    def portion_get_all(self, id_recipe: int) -> list[PortionResponse]:
        """
        A função serve para buscar todas as porções relacionadas a uma receita específica no banco de dados.

        - Parameter:
            - portion_out: PortionOut (Contém o id da receita necessária para buscar todas as porções)

        - Returns:
            - List[PortionResponse]: Uma lista com as porções encontradas para a receita

        - Exceptions:
            - Id da receita ausente
            - Nenhuma porção encontrada
        """
        try:
            # Verifica se o id da receita foi fornecido.
            if id_recipe is None:
                raise Exception("O id da receita é obrigatório")
            
            # Busca todas as porções relacionadas à receita no banco de dados.
            portions = self.db_session.query(PortionModel).filter_by(id_recipe=id_recipe).all()

            # Levanta exceção caso nenhuma porção seja encontrada.
            if not portions:
                raise Exception(f"Nenhuma porção encontrada para a receita")
            
            # Cria uma lista de respostas para cada porção encontrada.
            portions_response = [PortionResponse(**portion.dict()) for portion in portions]
            
            # Retorna a lista de porções encontradas.
            return portions_response

        except Exception as e:
            # Levanta a exceção em caso de erro.
            raise e

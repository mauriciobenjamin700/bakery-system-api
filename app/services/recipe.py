"""
Esse pacote contem todos as funções do objeto Recipe

classes:
    UseCaseRecipe

"""
from src.models.schemas.recipe import *
from src.models.database.models import (
    Recipe as RecipeModel,
    Portion as PortionModel,
    LoteIngredient as LoteIngredientModel,
    Product as ProductModel)

class UseCaseRecipe():
    """
    Essa classe contém os casos de uso do objeto Recipe

    functions:
        - recipe_add(RecipeRequest)
        - recipe_delete(RecipeRequest)
        - recipe_update(RecipeUpdate)
        - recipe_get(RecipeRequest)
        - check_ingredient_quantity(quantity:float,id_recipe:int)
        - check_portion(total_quantity:float,id_ingredient:int,indice:int=0)
        - calculate_recipe_price(product:RecipeRequest)
        - calculate_sale_price(product:RecipeRequest,lucro:float)

    """
    def __init__(self,db_session):
        self.db_session = db_session

    def recipe_add(self, recipe_request: RecipeRequest) -> dict:
        """
        Adiciona uma nova receita associada a um produto.

        - Parameter:
            - recipe_request: RecipeRequest (Objeto contendo as informações da receita e o id do produto)

        - Returns:
            - dict: Mensagem de sucesso e o id da receita criada.

        - Exceptions:
            - Exceção levantada caso o id do produto seja inválido, o produto não seja encontrado, ou a receita já esteja cadastrada.
        """
        try:
            # Verifica se o id do produto foi fornecido corretamente
            if not(hasattr(recipe_request, "id_product")) or recipe_request.id_product is None or type(recipe_request.id_product) != int:
                raise Exception("Id invalido")

            # Busca o produto no banco de dados
            product = self.db_session.query(ProductModel).filter_by(id=recipe_request.id_product).first()

            # Verifica se o produto existe
            if product is None:
                raise Exception("Produto não encontrado")

            # Verifica se já existe uma receita para o produto
            recipe = self.db_session.query(RecipeModel).filter_by(id_product=recipe_request.id_product).first()

            if recipe:
                raise Exception("O produto já possui uma receita cadastrada, utilize a opção de editar")

            # Cria uma nova receita
            new_recipe = RecipeModel(**recipe_request.dict())
            self.db_session.add(new_recipe)
            self.db_session.flush()  # Atualiza o banco com a nova receita sem fazer o commit completo
            self.db_session.commit()  # Confirma a transação no banco de dados

            return {"msg": "Receita cadastrada com sucesso", "id": new_recipe.id}

        except Exception as e:
            # Em caso de erro, desfaz qualquer mudança no banco
            self.db_session.rollback()
            raise e

        
    def recipe_delete(self, recipe_delete: RecipeRequest):
        """
        Remove uma receita associada a um produto.

        - Parameter:
            - recipe_delete: RecipeRequest (Objeto contendo o id do produto cuja receita será removida)

        - Returns:
            - dict: Mensagem de sucesso caso a receita seja deletada com sucesso.

        - Exceptions:
            - Exceção levantada caso o id do produto seja inválido, o produto não seja encontrado, ou a receita não esteja cadastrada.
        """
        try:
            # Verifica se o id do produto foi fornecido corretamente
            if not(hasattr(recipe_delete, "id_product")) or recipe_delete.id_product is None or type(recipe_delete.id_product) != int:
                raise Exception("Id invalido")

            # Busca o produto no banco de dados
            product = self.db_session.query(ProductModel).filter_by(id=recipe_delete.id_product).first()

            # Verifica se o produto existe
            if product is None:
                raise Exception("Produto não encontrado")

            # Busca a receita associada ao produto
            recipe = self.db_session.query(RecipeModel).filter_by(id_product=recipe_delete.id_product).first()

            # Verifica se a receita existe
            if not recipe:
                raise Exception("Receita não encontrada")

            # Remove a receita do banco de dados
            self.db_session.delete(recipe)
            self.db_session.commit()  # Confirma a exclusão no banco de dados

            return {"msg": "Receita deletada com sucesso"}

        except Exception as e:
            # Em caso de erro, desfaz qualquer mudança no banco
            self.db_session.rollback()
            raise e

        
    def recipe_update(self,recipe_id: int , product_id: int):
        try:
            
            product = self.db_session.query(ProductModel).filter_by(id=product_id).first()

            if not product:
                raise Exception("O Produto do novo id não foi encontrado")  

            recipe = self.db_session.query(RecipeModel).filter_by(id=recipe_id).first()

            if not recipe:
                raise Exception("Receita não encontrada")
            
            recipe.id_product = recipe_id

            self.db_session.commit()
            self.db_session.refresh(recipe)
            return {"msg": "Receita atualizada com sucesso"}
        
        except Exception as e:
            self.db_session.rollback()
            raise e
        
    def recipe_get(self,recipe_request:RecipeRequest) -> int:
        try:
            if not(hasattr(recipe_request, "id_product")) or recipe_request.id_product == None or type(recipe_request.id_product) != int:
                    raise Exception("Id invalido")
            
            recipe = self.db_session.query(RecipeModel).filter_by(id_product = recipe_request.id_product).first()
            
            if not recipe:
                raise Exception("Receita não encontrada")

            return RecipeResponse(**recipe.dict())

        except Exception as e:
             raise e
    
    def check_ingredient_quantity(self,quantity:float,id_recipe:int):
        portions = self.db_session.query(PortionModel).filter_by(id_recipe=id_recipe).all()

        for portion in portions:
            self.check_portion(quantity*portion.quantity,portion.id_recipe)

    def check_portion(self,total_quantity:float,id_ingredient:int,indice:int=0):
        lote = self.db_session.query(LoteIngredientModel).filter_by(id_ingredient = id_ingredient).all()

        try:
            if total_quantity <= lote[indice].quantity:
                lote.quantity -= total_quantity 
                return [True]
            else:
                total_quantity -= lote[indice].quantity
                lote[indice].quantity = 0
                self.check_portion(total_quantity,id_ingredient,indice+1)
        except Exception:
            raise id_ingredient
        
    def calculate_recipe_price(self,product:RecipeRequest):
        recipe = self.recipe_get(product)
        recipe_portions = self.db_session.query(PortionModel).filter_by(id_recipe = recipe.id_product).all()
        total_value = 0
        
        for portions in recipe_portions:
            lote_ingredient = self.db_session.query(LoteIngredientModel).filter_by(
                id_ingredient = portions.id_ingredient).first()
            total_value += lote_ingredient.value
        
        return total_value
    
    def calculate_sale_price(self,product:RecipeRequest,lucro:float):
        if not(hasattr(product, "id_product")) or product.id_product == None or type(product.id_product) != int:
            raise Exception("Id invalido")
        
        value = self.calculate_recipe_price(product)
        return value * (lucro/100)
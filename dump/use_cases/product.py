"""
Esse pacote contem todos as funções do objeto Product

classes:
    UseCaseProduct

"""

from sqlalchemy import func
from datetime import datetime
from src.controllers.services.check_fields import check_fields_formated

from src.models.schemas.product import *

from src.models.database.models import (
    Product as ProductModel,
    LoteProduct as LoteProductModel
    )

from src.controllers.use_cases.recipe import UseCaseRecipe
from src.models.schemas.recipe import RecipeRequest, RecipeResponse

class UseCaseProduct():
    """
    Essa classe contém os casos de uso do objeto Product

    functions:
        - product_add(ProductRequest)
        - product_delete(ProductDelete)
        - product_update(ProductUpdate)
        - lote_add(LoteProductRequest)
        - lote_delete(LoteProductDelete)
        - lote_update(LoteProductUpdate)
        - product_get(ProductOut)
        - product_get_all()
        - get_db_product()
        - get_product_by_name(product_name:str)
    """
    DEFAULT_MARK = "-"

    def __init__(self,db_session):
        self.db_session = db_session

    def product_add(self, product_request: ProductRequest):
        """
        A função serve para adicionar um novo produto no banco de dados. Se o produto já existir, 
        ele será adicionado como um novo lote. O produto é validado quanto aos campos obrigatórios 
        antes de ser inserido.

        - Parameter:
            - product_request: ProductRequest (Contém os dados do produto a ser cadastrado)

        - Returns:
            - Dict: Retorna uma mensagem de sucesso e o id do produto cadastrado, ou informa que o produto já existe e foi salvo como lote.

        - Exceptions:
            - Campos obrigatórios não preenchidos (name, measure, quantity)
            - Erros ao adicionar o produto ou lote no banco de dados
        """
        try:

            # Se a marca não for fornecida, usa a marca padrão.
            if not product_request.mark:
                product_request.mark = UseCaseProduct.DEFAULT_MARK

            # Verifica se o produto já existe no banco de dados.
            product_on_db = self.db_session.query(ProductModel).filter_by(
                name=product_request.name,
                mark=product_request.mark,
                measure=product_request.measure
            ).first()

            # Prepara os dados para inserção.
            data_insert_product = product_request.dict_nofilter()
            data_insert_lote = product_request.dict_nofilter()

            # Remove os campos relacionados ao lote do dicionário do produto.
            for _ in range(8):
                data_insert_lote.pop(next(iter(data_insert_lote)))

            # Se o produto já existir, adiciona-o como um novo lote.
            if product_on_db:
                self.db_session.add(LoteProductModel(**data_insert_lote, product_id=product_on_db.id, register_date=datetime.now()))
                self.db_session.commit()
                return {"msg": "Produto já existe, então o produto foi salvo como lote"}
            
            # Remove os últimos três itens do dicionário do produto para preparar a inserção.
            for _ in range(2):
                data_insert_product.popitem()


            product_model = ProductModel(**data_insert_product)
            # Adiciona o produto no banco de dados.
            self.db_session.add(product_model)
            self.db_session.flush()

            # Adiciona o lote referente ao produto cadastrado.
            self.db_session.add(
                
                LoteProductModel(
                    **data_insert_lote, 
                    product_id=product_model.id, 
                    register_date=datetime.now()
                    )
                )

            # Faz o commit da transação.
            self.db_session.commit()
            return {"msg": "Produto cadastrado com sucesso", "id": product_model.id}

        except Exception as e:
            # Faz rollback em caso de erro.
            self.db_session.rollback()
            raise e

    def product_delete(self, product_id: int):
        """
        A função serve para deletar um produto existente no banco de dados, utilizando o id do produto 
        fornecido no `ProductDelete`. Verifica se o id é válido antes de realizar a deleção.

        - Parameter:
            - product_delete: ProductDelete (Contém o id do produto a ser deletado)

        - Returns:
            - Dict: Retorna uma mensagem de sucesso indicando que o produto foi deletado.

        - Exceptions:
            - Id ausente ou inválido
            - Produto não encontrado
            - Erros ao deletar o produto no banco de dados
        """
        try:
            # Busca o produto no banco de dados pelo id.
            product = self.db_session.query(ProductModel).filter_by(id=product_id).first()

            # Levanta exceção se o produto não for encontrado.
            if not product:
                raise Exception("Produto não encontrado")
            
            # Deleta o produto encontrado.
            self.db_session.delete(product)
            self.db_session.commit()

            # Retorna uma mensagem de sucesso.
            return {"msg": "Produto deletado com sucesso"}

        except Exception as e:
            # Faz rollback em caso de erro.
            self.db_session.rollback()
            raise e


    def product_update(self, product_update: ProductUpdate):
        """
        A função atualiza os dados de um produto existente no banco de dados. O `id` do produto 
        é necessário para localizar o produto a ser atualizado. Campos ausentes ou inválidos 
        são tratados antes de aplicar as modificações.

        - Parameter:
            - product_update: ProductUpdate (Contém os dados a serem atualizados)

        - Returns:
            - Dict: Retorna uma mensagem de sucesso informando que o produto foi atualizado.

        - Exceptions:
            - Falta de atributo obrigatório (id)
            - Produto não encontrado
            - Erros ao atualizar o produto no banco de dados
        """
        try:
            # Converte o objeto de entrada em um dicionário para fácil manipulação.
            data_update = product_update.dict()
            # Busca o produto no banco de dados pelo id.
            product = self.db_session.query(ProductModel).filter_by(id=product_update.id).first()

            # Levanta exceção se o produto não for encontrado.
            if not product:
                raise Exception("Produto não encontrado")
                        
            # Atualiza os campos do produto com os valores fornecidos.
            for field, value in data_update.items():
                setattr(product, field, value)
            
            # Faz o commit das mudanças e atualiza a instância do produto.
            self.db_session.commit()
            self.db_session.refresh(product)

            # Retorna uma mensagem de sucesso.
            return {"msg": "Produto atualizado com sucesso"}

        except Exception as e:
            # Faz rollback em caso de erro.
            self.db_session.rollback()
            raise e
    
    def lote_add(self, lote_product_request: LoteProductRequest):
        """
        A função adiciona um novo lote para um produto existente. Valida os campos obrigatórios 
        do lote e verifica se o produto relacionado ao lote existe antes de adicionar o lote.

        - Parameter:
            - lote_product_request: LoteProductRequest (Contém os dados do lote a ser adicionado)

        - Returns:
            - Dict: Retorna uma mensagem de sucesso informando que o lote foi cadastrado.

        - Exceptions:
            - Campos obrigatórios não preenchidos (product_id, quantity)
            - Produto não encontrado
            - Erros ao adicionar o lote no banco de dados
        """
        try:

            # Verifica se o produto relacionado ao lote existe no banco de dados.
            product_on_db = self.db_session.query(ProductModel).filter_by(
                id=lote_product_request.product_id).first()

            # Se o produto for encontrado, adiciona o lote.
            if product_on_db:
                self.db_session.add(LoteProductModel(**lote_product_request.dict(), register_date=datetime.now()))
                self.db_session.commit()
                return {"msg": "Lote cadastrado com sucesso"}
            
            # Levanta exceção se o produto não for encontrado.
            raise Exception("Produto não foi encontrado")

        except Exception as e:
            # Faz rollback em caso de erro.
            self.db_session.rollback()
            raise e

        
    def lote_delete(self, lote_id: int):
        """
        A função deleta um lote existente no banco de dados, utilizando o id do lote fornecido no 
        `LoteProductDelete`. Verifica se o id é válido antes de realizar a deleção.

        - Parameter:
            - lote_delete: LoteProductDelete (Contém o id do lote a ser deletado)

        - Returns:
            - Dict: Retorna uma mensagem de sucesso informando que o lote foi removido.

        - Exceptions:
            - Id ausente ou inválido
            - Lote não encontrado
            - Erros ao deletar o lote no banco de dados
        """
        try:
            
            # Busca o lote no banco de dados pelo id.
            product = self.db_session.query(LoteProductModel).filter_by(id=lote_id).first()

            # Levanta exceção se o lote não for encontrado.
            if not product:
                raise Exception("Lote não encontrado")

            # Deleta o lote encontrado.
            self.db_session.delete(product)
            self.db_session.commit()

            # Retorna uma mensagem de sucesso.
            return {"msg": "Lote removido com sucesso"}

        except Exception as e:
            # Faz rollback em caso de erro.
            self.db_session.rollback()
            raise e


    def lote_update(self, lote_update: LoteProductUpdate) -> dict[str, str]:
        """
        A função atualiza os dados de um lote de produto existente no banco de dados. O `id` do lote 
        é necessário para localizar o lote a ser atualizado. Caso a quantidade do lote seja aumentada,
        é realizada uma verificação da quantidade de produto disponível nas receitas relacionadas.

        - Parameter:
            - lote_update: LoteProductUpdate (Contém os dados a serem atualizados)

        - Returns:
            - Dict: Retorna uma mensagem de sucesso informando que o lote foi atualizado.

        - Exceptions:
            - Falta de atributo obrigatório (id)
            - Lote não encontrado
            - Erros ao atualizar o lote no banco de dados
            - Verificação de quantidade de produto nas receitas
        """
        try:
            # Converte o objeto de entrada em um dicionário para fácil manipulação.
            data_update = lote_update.dict()

            # Busca o lote no banco de dados pelo id.
            lote = self.db_session.query(LoteProductModel).filter_by(id=lote_update.id).first()

            # Levanta exceção se o lote não for encontrado.
            if not lote:
                raise Exception("Lote do produto não encontrado")
            
            # Verifica se há atualização na quantidade e se a nova quantidade é maior que a anterior.
            try:
                if "quantity" in data_update:
                    if data_update["quantity"] > lote.quantity:
                        # Verifica se o produto tem receita associada e valida a quantidade disponível.
                        uc = UseCaseRecipe(self.db_session)
                        recipe = uc.recipe_get(RecipeRequest(id_product=lote.product_id))
                        if recipe:
                            uc.check_product_quantity(data_update["quantity"] - lote.quantity, recipe)
            except:
                pass

            # Atualiza os campos do lote com os valores fornecidos.
            for field, value in data_update.items():
                setattr(lote, field, value)
            
            # Faz o commit das mudanças e atualiza a instância do lote.
            self.db_session.commit()
            self.db_session.refresh(lote)

            # Retorna uma mensagem de sucesso.
            return {"msg": "Lote atualizado com sucesso"}

        except Exception as e:
            # Faz rollback em caso de erro.
            self.db_session.rollback()
            raise e

    def product_get(self, product_id):
        """
        Recupera os lotes de produto pelo id relacionados.
        
        - Parameter:
            - product_out: ProductOut (Objeto contendo o id do produto a ser buscado)
        
        - Returns:
            - dict{"product":ProductResponse,"lotes":[LoteProductResponse]}: Dicionario contendo informações do produto e seus lotes
        
        - Exceptions:
            - Exceção levantada caso o id não seja fornecido ou o produto não seja encontrado.
        """
        try:

            # Busca o produto no banco de dados
            product = self.db_session.query(ProductModel).filter_by(id=product_id).first()

            # Verifica se o produto existe
            if not product:
                raise Exception(f"Produto não encontrado.")

            # Busca os lotes relacionados ao produto
            lotes = self.db_session.query(LoteProductModel).filter_by(product_id=product_id).all()
            
            all_lote = []
            
            total_quantity = 0
            
            # Monta a resposta contendo o produto e seus lotes
            for lote in lotes:
                
                lote_response = LoteProductResponse(lote_id=lote.id, **lote.dict())
                
                total_quantity += lote.quantity
                
                all_lote.append(lote_response)

            product_response = ProductResponse(**product.dict(),quantity=total_quantity)
            
            return {"product":product_response,"lotes":all_lote}

        except Exception as e:
            raise e
       
    def product_get_all(self) -> list[dict]:
        """
        Recupera todos os produtos cadastrados no banco de dados junto com seus lotes relacionados.
        
        - Returns:
            - list[{'product':ProductResponse,'lotes':[LoteProductResponse]}]: Lista contendo dicionarios
            com os produtos e seus lotes
        
        - Exceptions:
            - Exceção levantada caso nenhum produto seja encontrado ou não haja lotes para os produtos.
        """
        try:
            # Busca todos os produtos no banco de dados
            products = self.db_session.query(ProductModel).all()

            # Verifica se existem produtos cadastrados
            if not products:
                raise Exception(f"Nenhum produto encontrado")

            
            all_products = []
            # Itera sobre cada produto encontrado
            for product in products:
                # Busca os lotes associados ao produto
                lotes = self.db_session.query(LoteProductModel).filter_by(product_id=product.id).all()
                all_lote = []
                total_quantity=0
                # Adiciona cada lote e produto à resposta
                for lote in lotes:
                    lote_response = LoteProductResponse(lote_id=lote.id, **lote.dict())
                    total_quantity+=lote_response.quantity
                    all_lote.append(lote_response)
                product_response = ProductResponse(**product.dict(),quantity=total_quantity)
                all_products.append({"product":product_response,"lotes":all_lote}) 
                    
            # Verifica se há lotes e retorna a resposta
            return all_products

        except Exception as e:
            raise e

    def get_db_product(self) -> list[ProductModel]:
        """
        Retorna todos os produtos cadastrados no banco de dados.
        
        - Returns:
            - list[ProductModel]: Lista contendo todos os produtos.
        """
        return self.db_session.query(ProductModel).all()

    def get_product_by_name(self, product_name: str) -> ProductResponse:
        """
        Recupera um produto pelo nome fornecido.
        
        - Parameter:
            - product_name: str (Nome do produto a ser buscado)
        
        - Returns:
            - ProductResponse: Contém as informações do produto encontrado.
        
        - Exceptions:
            - Exceção levantada caso o produto não seja encontrado.
        """
        try:
            # Busca o produto pelo nome
            product = self.db_session.query(ProductModel).filter_by(name=product_name).first()

            # Verifica se o produto foi encontrado
            if not product:
                raise Exception(f"Nenhum produto encontrado com o nome {product_name}")

            # Retorna as informações do produto
            return ProductResponse(**product.dict())

        except Exception as e:
            raise e

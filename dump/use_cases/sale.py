from src.models.schemas.sale import *
from src.models.database.models import (
    ProductSale as ProductSaleModel,
    SaleNote as SaleNoteModel, 
    LoteProduct as LoteProductModel)
from datetime import datetime
class UseCaseSale():
    def __init__(self,db_session):
        self.db_session = db_session

    def create_sale_note(self,sale_list:list[ProductSaleRequest]):
        try:
            if sale_list is None or sale_list == []:
                raise Exception("Lista de vendas esta vazia")
            
            total_value = 0
            for sale in sale_list:

                lotes = self.db_session.query(LoteProductModel).filter_by(product_id = sale.id_product).all()
                sale_quantity = sale.quantity
                try:
                    for lote in lotes:
                        if sale_quantity <= lote.quantity:
                            lote.quantity -= sale_quantity
                            sale_quantity = 0
                            break
                        else:
                            sale_quantity -= lote.quantity
                            lote.quantity = 0
                    if sale_quantity > 0:
                        raise Exception("Não a produtos suficientes no estoque")
                
                except Exception as e:
                    raise e
            total_value += sale.unit_cost * sale.quantity

            sale_note = SaleNoteModel(total_value=total_value, sale_time=datetime.now())

            self.db_session.add(sale_note)
            self.db_session.flush()

            for sale in sale_list:
                sale.id_sale_note = sale_note.id
            
            products_sale_list = [ProductSaleModel(**product.dict()) for product in sale_list]
            self.db_session.add_all(products_sale_list)
            self.db_session.commit()

            for product in products_sale_list:
                self.db_session.refresh(product)

            return {"msg":"Venda realizada com sucesso"}


        except Exception as e:
            self.db_session.rollback()
            raise e
    
    def get_all_sale_note(self):
        try:
            all_sale_note = self.db_session.query(SaleNoteModel).all()
            response_all_sale_note = []
            for sale_note in all_sale_note:
                sale_note_list = SaleNoteResponse(**sale_note.dict(),products=[])
                all_products_sale = self.db_session.query(ProductSaleModel).filter_by(id_sale_note = sale_note_list.id).all()
                list_products_sale = [ProductSaleRequest(**product_sale.dict()) for product_sale in all_products_sale]
                
                for product_sale in list_products_sale:
                    sale_note_list.products.append(product_sale)
                
                response_all_sale_note.append(sale_note_list)
            
            return response_all_sale_note
        
        except Exception as e:
            raise e
        
    def get_db_sale_note(self) -> list[SaleNoteModel]:
        return self.db_session.query(SaleNoteModel).all()
    
    def get_db_product_sale(self) -> list[ProductSaleModel]:
        return self.db_session.query(ProductSaleModel).all()
    

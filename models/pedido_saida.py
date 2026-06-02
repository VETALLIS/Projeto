from core.crud_base import Crud_base
from core.manipular import Manipular 
import datetime
class Pedido_saida(Crud_base):
    tabela = "pedido_saida"
    fields = ["pedido_saida_id", "pedido_saida_nome", "pedido_saida_data", "pedido_saida_status", "animal_animal_id"]

    def __init__(self, pedido_saida_nome, pedido_saida_data, animal_animal_id, pedido_saida_status = "PENDENTE" ):
        self.pedido_saida_nome = pedido_saida_nome
        self.pedido_saida_data = pedido_saida_data 
        self.pedido_saida_status = pedido_saida_status
        self.animal_animal_id = animal_animal_id

    def validar_saida(self):
        erros = [
            Manipular.validar_vazio(self.pedido_saida_nome, "nome"),
            Manipular.validar_vazio(self.pedido_saida_data, "data"),
            Manipular.validar_data(self.pedido_saida_data, "data"),
            Manipular.validar_vazio(self.animal_animal_id, "animal"),     
        ]          
    
        return [ erro for erro in erros if erro]

    def gravar_pedido_saida(self):
        pedido_saida = self.gravar()

        if not pedido_saida:
            raise ValueError("Erro ao criar pedido!")

        return "Pedido criado com sucesso"

    def deletar_pedido_saida(self, id):
        pedido_saida = self.buscar_por_id(id)

        if not pedido_saida:
            raise ValueError("Pedido não encontrado")

        self.deletar()
        return "Pedido deletado com sucesso!"

    def atualizar_pedido_saida(self, id):
        pedido_saida = self.buscar_por_id(id)

        if not pedido_saida:
            raise ValueError("Pedido não encontrado")

        self.atualizar()
        return "Pedido atualizado com sucesso!"

    def buscar_todos_pedidos_saida(cls, order_by="pedido_saida_nome"):
        pedido_saida  = cls.buscar_tudo(order_by)

        if not pedido_saida:
            raise ValueError("Pedido não encontrado!")

        return Pedido_saida(**pedido_saida)
    
from core.crud_base import Crud_base
from core.manipular import Manipular 

class Item_pedido_saida(Crud_base):
    tabela = "item_pedido_saida"
    fields = ["item_pedido_saida_id", "item_pedido_saida_nome", "item_pedido_saida_data_validade", 
    "item_pedido_saida_quantidade","item_pedido_saida_lote", "estoque_estoque_id", "pedido_saida_pedido_saida_id"]

    def __init__(self, item_pedido_saida_nome, item_pedido_saida_data_validade, 
    item_pedido_saida_quantidade, item_pedido_saida_lote, estoque_estoque_id, pedido_saida_pedido_saida_id ):
        self.item_pedido_saida_nome = item_pedido_saida_nome
        self.item_pedido_saida_data_validade = item_pedido_saida_data_validade
        self.item_pedido_saida_lote = item_pedido_saida_lote
        self.item_pedido_saida_quantidade = item_pedido_saida_quantidade
        self.estoque_estoque_id = 1
        self.pedido_saida_pedido_saida_id= 1
    
    def validar_item_pedido_saida(self):
        erros = [
            Manipular.validar_vazio(self.item_pedido_saida_nome, "nome"),
            Manipular.validar_vazio(self.item_pedido_saida_data_validade, "data"),
            Manipular.validar_data(self.item_pedido_saida_data_validade, "data"),
            Manipular.validar_numero_negativo(self.item_pedido_saida_quantidade, "quantidade"),
            Manipular.validar_vazio(self.item_pedido_saida_quantidade, "quantidade"),
            Manipular.validar_vazio(self.item_pedido_saida_lote, "lote"),       
        ]          
    
        return [ erro for erro in erros if erro]

    def gravar_item_pedido_saida(self):
        pedido_saida = self.gravar()
        

        if not pedido_saida:
            raise ValueError("Erro ao criar pedido!")

        return "Pedido criado com sucesso"

    def deletar_item_pedido_saida(self, id):
        pedido_saida = self.buscar_por_id(id)

        if not pedido_saida:
            raise ValueError("Pedido não encontrado")

        self.deletar()
        return "Pedido deletado com sucesso!"

    def atualizar_item_pedido_saida(self, id):
        pedido_saida = self.buscar_por_id(id)

        if not pedido_saida:
            raise ValueError("Pedido não encontrado")

        self.atualizar()
        return "Pedido atualizado com sucesso!"

    def buscar_item_pedido_saida(self):
        pedido_saida  = self.buscar_por_id(id)

        if not pedido_saida:
            raise ValueError("Pedido não encontrado!")


        return Item_pedido_saida(**item_pedido_saida)
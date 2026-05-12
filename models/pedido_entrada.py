from core.crud_base import Crud_base
from core.manipular import Manipular
from core.conectar import Database

class Pedido_entrada(Crud_base):
    tabela = "pedido_entrada"
    pk = "pedido_entrada_id"
    fields = ["pedido_entrada_nome", "pedido_entrada_data", "pedido_entrada_status", "fornecedor_fornecedor_id"]

    def __init__(self, pedido_entrada_nome, pedido_entrada_data, pedido_entrada_status):
        self.pedido_entrada_nome = pedido_entrada_nome
        self.pedido_entrada_data = pedido_entrada_data
        self.pedido_entrada_status = pedido_entrada_status
        self.fornecedor_fornecedor_id = 1
        
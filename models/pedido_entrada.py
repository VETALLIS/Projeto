from core.crud_base import Crud_base
from core.manipular import Manipular
from core.conectar import Database
from datetime import datetime

class Pedido_entrada(Crud_base):
    tabela = "pedido_entrada"
    pk = "pedido_entrada_id"
    fields = ["pedido_entrada_nome", "pedido_entrada_data", "pedido_entrada_status", "fornecedor_fornecedor_id"]

    def __init__(self, pedido_entrada_nome, pedido_entrada_data, pedido_entrada_status, fornecedor_fornecedor_id=None):
        self.pedido_entrada_nome = pedido_entrada_nome
        self.pedido_entrada_data = pedido_entrada_data
        self.pedido_entrada_status = pedido_entrada_status
        self.fornecedor_fornecedor_id = fornecedor_fornecedor_id

    def validar_pedido_entrada (self):
        erros = [
            Manipular.validar_vazio (self.pedido_entrada_nome, "pedido_entrada_nome"),
            #Manipular.validar_vazio (self.pedido_entrada_data, "pedido_entrada_data"),
            Manipular.validar_vazio (self.pedido_entrada_status, "pedido_entrada_status"),
            Manipular.validar_data(self.pedido_entrada_data, "pedido_entrada_data")
        ]
        return [ erro for erro in erros if erro]
    
    @staticmethod
    def converter_data(data_str):
        formatos = ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d']
        for formato in formatos:
            try:
                return datetime.strptime(data_str.strip(), formato).strftime('%Y-%m-%d')
            except ValueError:
                continue
        return None
    
    def gravar_pedido_entrada (self):
        pedido_entrada = self.gravar()

        if not pedido_entrada:
            raise ValueError("Erro ao cadastrar pedido de entrada.")
        
        return "Cadastrado"

    @classmethod
    def relacao_entre_tabelas(cls, id):
        '''
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            queries = [
                "SELECT COUNT(*) FROM item_pedido_entrada WHERE produto_id = %s",
                "SELECT COUNT(*) FROM pedido_entrada WHERE produto_id = %s"
            ]
            total = 0
            for sql in queries:
                cursor.execute(sql, (id,))
                total += cursor.fetchone()[0]
            return total > 0
        finally:
            cursor.close()
            conexao.close()'''
        return False

    def deletar_pedido_entrada(cls, id):
        pedido_entrada = cls.buscar_por_id(id)

        if not pedido_entrada:
            raise ValueError("Pedidode entrada não encontrado.")
        if cls.relacao_entre_tabelas(id):
            raise ValueError("Não é possível excluir o pedido de entrada porque ele possui pedidos ou movimentações vinculadas.")
        cls.deletar(id)

        return "Pedido de entrada deletado com sucesso!"

    def atualizar_pedido_entrada(self, id):
        pedido_entrada = self.buscar_por_id(id)

        if not pedido_entrada:
            raise ValueError("Pedido de entrada não encontrado!")
        if self.relacao_entre_tabelas(id):
            raise ValueError("Não é possível atualizar o pedido de entrada porque ele possui pedidos ou movimentações vinculadas.")
        self.atualizar(id)

        return "Pedido de entrada atualizado com sucesso!"

    def buscar_todo_pedido_entrada(cls, order_by="pedido_entrada_nome"):
        pedido_entrada = cls.buscar_tudo(order_by)

        if not pedido_entrada:
            raise ValueError("Pedidos de entrada não encontrados")

        return f"Pedidos de entrada: "

class item_pedido_entrada(Crud_base): 
    tabela = "item_pedido_entrada"
    pk = "item_pedido_entrada_id"
    fields = ["item_pedido_entrada_nome" ,"item_pedido_entrada_lote", "item_pedido_entrada_quantidade", "item_pedido_entrada_valor_unitario", "pedido_entrada_pedido_entrada_id"]

    def __init__(self, item_pedido_entrada_lote,item_pedido_entrada_quantidade,item_pedido_entrada_valor_unitario, item_pedido_entrada_nome, pedido_entrada_pedido_entrada_id):
        self.item_pedido_entrada_lote = item_pedido_entrada_lote
        self.item_pedido_entrada_quantidade = item_pedido_entrada_quantidade
        self.item_pedido_entrada_valor_unitario = item_pedido_entrada_valor_unitario
        self.item_pedido_entrada_nome = item_pedido_entrada_nome
        self.pedido_entrada_pedido_entrada_id= pedido_entrada_pedido_entrada_id

    def validar_item_pedido_entrada (self):
        erros = [
            Manipular.validar_vazio (self.item_pedido_entrada_nome, "item_pedido_entrada_nome"),
            Manipular.validar_vazio (self.item_pedido_entrada_lote, "item_pedido_entrada_lote"),
            Manipular.validar_vazio (self.item_pedido_entrada_quantidade, "item_pedido_entrada_quantidade"),
            Manipular.validar_vazio (self.item_pedido_entrada_valor_unitario, "item_pedido_entrada_valor_unitario"),
            Manipular.validar_numero_negativo (self.item_pedido_entrada_quantidade, "item_pedido_entrada_quantidade"),
            Manipular.validar_numero_negativo (self.item_pedido_entrada_valor_unitario, "item_pedido_entrada_valor_unitario")
        ]

        return [ erro for erro in erros if erro]
    
    def gravar_item_pedido_entrada (self):
        item_pedido_entrada = self.gravar()

        if not item_pedido_entrada:
            raise ValueError("Erro ao cadastrar item de pedido de entrada.")
        
        return "Cadastrado"

    def deletar_item_pedido_entrada(cls, id):
        item_pedido_entrada = cls.buscar_por_id(id)

        if not item_pedido_entrada:
            raise ValueError("Item de Pedido de entrada não encontrado.")
        if cls.relacao_entre_tabelas(id):
            raise ValueError("Não é possível excluir o item de pedido de entrada porque ele possui pedidos ou movimentações vinculadas.")
        cls.deletar(id)

        return "Item de Pedido de entrada deletado com sucesso!"

    def atualizar_item_pedido_entrada(self, id):
        item_pedido_entrada = self.buscar_por_id(id)

        if not item_pedido_entrada:
            raise ValueError("Item de pedido de entrada não encontrado!")
        self.atualizar(id)
        return "Item de pedido de entrada atualizado com sucesso!"


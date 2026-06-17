from core.crud_base import Crud_base
from core.manipular import Manipular 
import datetime
from core.conectar import Database



class Pedido_saida(Crud_base):
    pk = "pedido_saida_id"
    tabela = "pedido_saida"
    fields = ["pedido_saida_id", "pedido_saida_nome", "pedido_saida_data", "pedido_entrada_status", "animal_animal_id"]

    def __init__(self, pedido_saida_nome, pedido_saida_data, animal_animal_id, pedido_entrada_status = "PENDENTE" ):
        self.pedido_saida_id = None
        self.pedido_saida_nome = pedido_saida_nome
        self.pedido_saida_data = pedido_saida_data 
        self.pedido_entrada_status = pedido_entrada_status
        self.animal_animal_id = animal_animal_id

    def validar_pedido_saida(self):
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

        return pedido_saida

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
    pk = "item_pedido_saida_id"
    tabela = "item_pedido_saida"
    fields = ["item_pedido_saida_id", "item_pedido_saida_nome", "item_pedido_saida_quantidade","item_pedido_saida_lote", "estoque_estoque_id", "pedido_saida_pedido_saida_id"]

    def __init__(self, item_pedido_saida_nome, item_pedido_saida_quantidade, item_pedido_saida_lote, estoque_estoque_id, pedido_saida_pedido_saida_id ):
        self.item_pedido_saida_id = None
        self.item_pedido_saida_nome = item_pedido_saida_nome
        self.item_pedido_saida_lote = item_pedido_saida_lote
        self.item_pedido_saida_quantidade = item_pedido_saida_quantidade
        self.estoque_estoque_id = Item_pedido_saida.buscar_estoque_por_produto(item_pedido_saida_nome)
        self.pedido_saida_pedido_saida_id= pedido_saida_pedido_saida_id 
    
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

    def gravar_item_pedido_saida(self, numero):
        self.pedido_saida_pedido_saida_id = numero
        pedido_saida = self.gravar()
        

        if not pedido_saida:
            raise ValueError("Erro ao criar pedido!")

        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = """
                UPDATE estoque 
                SET estoque_quantidade = estoque_quantidade - %s
                WHERE estoque_id = %s
            """

            valores = (
                self.item_pedido_saida_quantidade,        
                self.estoque_estoque_id  
            )
            
            cursor.execute(sql, valores)
            conexao.commit()
            
            return "Produto e estoque cadastrados com sucesso!"
            
        except Exception as e:
            conexao.rollback() 
            raise ValueError(f"Erro ao cadastrar o estoque do produto: {e}")
            
        finally:
            cursor.close()
            conexao.close()
    
    def _validar_quantidade(self, cursor, id_produto, quantidade):
        sql = """
            SELECT estoque_quantidade
            FROM estoque
            WHERE id_produto = %s
            AND id_localizacao = %s
        """

        cursor.execute(sql, (id_produto))
        estoque = cursor.fetchone()

        if estoque is None:
            raise Exception("Produto não encontrado no estoque.")

        quantidade_atual = float(estoque["estoque_quantidade"])

        if quantidade_atual < quantidade:
            raise Exception("Saldo insuficiente em estoque.")

    def _atualizar_estoque_saida(self, cursor, id_produto, id_localizacao, quantidade):
        sql = """
            UPDATE estoque
            SET estoque_quantidade = estoque_quantidade - %s
            WHERE id_produto = %s
            AND id_localizacao = %s
        """

        cursor.execute(
            sql,
            (quantidade, id_produto)
        )

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
        item_pedido_saida  = self.buscar_por_id(id)

        if not item_pedido_saida:
            raise ValueError("Pedido não encontrado!")


        return Item_pedido_saida(**item_pedido_saida)

    @classmethod
    def buscar_todo_item_pedido_saida(cls, order_by=pk):
        item_pedido_saida = cls.buscar_tudo(order_by) 

        if not item_pedido_saida: 
            raise ValueError("Item de pedido de saida nao encontrado não encontrado.") 

        return item_pedido_saida

    @staticmethod
    def buscar_estoque_por_produto(produto_id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            cursor.execute("SELECT estoque_id FROM estoque WHERE produto_produto_id = %s", (produto_id,))
            resultado = cursor.fetchone()
            if not resultado:
                raise ValueError("Estoque não encontrado para esse produto.")
            return resultado["estoque_id"]
        finally:
            cursor.close()
            conexao.close()
# Importamos o crud base e o manipular, além do conectar para que possamso fazer a integração e manipulação de dados do pedido saíida
from core.crud_base import Crud_base
from core.manipular import Manipular 
import datetime
from core.conectar import Database


# Criamos a classe de pedido saída definindo sua chave primária, nome da tabela e campos
class Pedido_saida(Crud_base):
    pk = "pedido_saida_id"
    tabela = "pedido_saida"
    fields = [ "pedido_saida_nome", "pedido_saida_data", "pedido_entrada_status", "animal_animal_id"]

    def __init__(self, pedido_saida_nome,pedido_saida_data, animal_animal_id, pedido_entrada_status = "PENDENTE" ): #Aqui definimos os dados para cada uma das variáveis
        self.pedido_saida_id = None
        self.pedido_saida_nome = pedido_saida_nome
        self.pedido_saida_data = pedido_saida_data 
        self.pedido_entrada_status = pedido_entrada_status
        self.animal_animal_id = animal_animal_id

    def validar_pedido_saida(self): # Aqui pegamos cada dado e com as funções do manipular validamos eles 
        erros = [
            Manipular.validar_vazio(self.pedido_saida_nome, "nome"),
            Manipular.validar_vazio(self.pedido_saida_data, "data"),
            Manipular.validar_data(self.pedido_saida_data, "data"),
            Manipular.validar_vazio(self.animal_animal_id, "animal"),     
        ]          
    
        return [ erro for erro in erros if erro]

    def converter_data_saida(data_str): # Pega a data em formato de ano, mes e dia e converte para dia, mes e ano
            formatos = ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d']
            for formato in formatos:
                try:
                    return datetime.strptime(data_str.strip(), formato).strftime('%Y-%m-%d')
                except ValueError:
                    continue
            return None

    def gravar_pedido_saida(self): # Depois de passar pelas validações ele grava os dados no banco senão dá uma mensagem de erro
        pedido_saida = self.gravar()

        if not pedido_saida:
            raise ValueError("Erro ao criar pedido!")

        return pedido_saida

    def deletar_pedido_saida(self, id): #Caso queira deletar o pedido essa função fara isso buscando o id do pedido
        pedido_saida = self.buscar_por_id(id)

        if not pedido_saida:
            raise ValueError("Pedido não encontrado")

        self.deletar()
        return "Pedido deletado com sucesso!"

    def atualizar_pedido_saida(self, id): #Caso queira atualizar o pedido essa função fara isso buscando o id do pedido
        pedido_saida = self.buscar_por_id(id)

        if not pedido_saida:
            raise ValueError("Pedido não encontrado")

        self.atualizar(id)
        return "Pedido atualizado com sucesso!"
    
    @classmethod
    def buscar_todos_pedidos_saida(cls, order_by="pedido_saida_nome"): # Caso queria listar todos os pedidos essa função listará ordenando com o order by
        pedido_saida  = cls.buscar_tudo(order_by)

        if not pedido_saida:
            raise ValueError("Pedido não encontrado!")

        return pedido_saida
    
from core.crud_base import Crud_base
from core.manipular import Manipular 

# Nessa parte fazemos outra classe para a segunda parte do pedido, onde se localizam os itens
class Item_pedido_saida(Crud_base):
    pk = "item_pedido_saida_id"
    tabela = "item_pedido_saida"
    fields = [ "item_pedido_saida_nome", "item_pedido_saida_quantidade","item_pedido_saida_lote", "pedido_saida_pedido_saida_id", "produto_produto_id"]

    def __init__(self, item_pedido_saida_nome, item_pedido_saida_quantidade, item_pedido_saida_lote, pedido_saida_pedido_saida_id, produto_produto_id):
        self.item_pedido_saida_id = None
        self.item_pedido_saida_nome = item_pedido_saida_nome
        self.item_pedido_saida_lote = item_pedido_saida_lote
        self.item_pedido_saida_quantidade = item_pedido_saida_quantidade
        self.pedido_saida_pedido_saida_id= pedido_saida_pedido_saida_id 
        self.produto_produto_id = produto_produto_id
    
    def validar_item_pedido_saida(self):
        erros = [
            Manipular.validar_vazio(self.item_pedido_saida_nome, "nome"),
            Manipular.validar_numero_negativo(self.item_pedido_saida_quantidade, "quantidade"),
            Manipular.validar_vazio(self.item_pedido_saida_quantidade, "quantidade"),
            Manipular.validar_vazio(self.item_pedido_saida_lote, "lote"),       
        ]          
    
        return [ erro for erro in erros if erro]

    def gravar_item_pedido_saida(self, numero): #Depois de seguir a mesma estrutura do cabeçalho do pedido ele grava no banco de dados na tabela estoque com a quantidade de itens removidos, senão ele dá como estoque inválido
        self.pedido_saida_pedido_saida_id = numero
        pedido_saida = self.gravar()

        if not pedido_saida:
            raise ValueError("Erro ao cadastrar items!")

        estoque_id_encontrado = self.buscar_estoque_por_produto(self.produto_produto_id)

        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = """
                UPDATE estoque 
                SET estoque_quantidade = estoque_quantidade - %s
                WHERE estoque_id = %s AND estoque_quantidade >= %s
            """

            valores = (
                self.item_pedido_saida_quantidade,        
                estoque_id_encontrado,
                self.item_pedido_saida_quantidade
            )
            
            cursor.execute(sql, valores)
            linhas = cursor.rowcount
            if linhas == 0:
                raise ValueError("Estoque insuficiente")

            conexao.commit()
            
            return pedido_saida
            
        except Exception as e:
            conexao.rollback() 
            raise ValueError(f"Erro ao cadastrar o estoque do produto: {e}")
            
        finally:
            cursor.close()
            conexao.close()
    
    def _validar_quantidade(self, cursor, id_produto, quantidade): # Aqui a função selecionará para verificar se a quantidade removida condiz com o quanto há no estoque, e se há o produto no estoque
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

    def _atualizar_estoque_saida(self, cursor, id_produto, id_localizacao, quantidade): # Aqui atualiza a quantidade de estoque de saída
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

    def deletar_item_pedido_saida(self, id): # essa função deleta o item do pedido buscando por id
        pedido_saida = self.buscar_por_id(id)

        if not pedido_saida:
            raise ValueError("Pedido não encontrado")

        self.deletar()
        return "Pedido deletado com sucesso!"

    def atualizar_item_pedido_saida(self, id): #essa função atualiza o item do pedido buscando por id
        pedido_saida = self.buscar_por_id(id)

        if not pedido_saida:
            raise ValueError("Pedido não encontrado")

        self.atualizar(id)
        return "Pedido atualizado com sucesso!"

    def buscar_item_pedido_saida(self): #essa função busca o item do pedido buscando por id
        item_pedido_saida  = self.buscar_por_id(id)

        if not item_pedido_saida:
            raise ValueError("Pedido não encontrado!")


        return Item_pedido_saida(**item_pedido_saida)

    @classmethod
    def buscar_todo_item_pedido_saida(cls, order_by=pk): #essa função lista todos os itens do pedido ordenando com o ordem by
        item_pedido_saida = cls.buscar_tudo(order_by) 

        if not item_pedido_saida: 
            raise ValueError("Item de pedido de saida nao encontrado não encontrado.") 

        return item_pedido_saida

    @staticmethod
    def buscar_estoque_por_produto(produto_id): # Essa função busca no estoque por produto específico
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
    
    @classmethod
    def buscar_por_pedido(cls, pedido_saida_id): # Esse busca o pedido pelo id dele
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM item_pedido_saida WHERE pedido_saida_pedido_saida_id = %s"
            cursor.execute(sql, (pedido_saida_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()
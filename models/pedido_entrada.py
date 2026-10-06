from core.crud_base import Crud_base
from core.manipular import Manipular
from core.conectar import Database
from datetime import datetime

class Pedido_entrada(Crud_base):
    tabela = "pedido_entrada" #nome da tabela no banco
    pk = "pedido_entrada_id" #chave primaria da tabela
    fields = ["pedido_entrada_nome", "pedido_entrada_data", "pedido_entrada_status", "fornecedor_fornecedor_id"] #campos que temos na tela

    def __init__(self, pedido_entrada_nome, pedido_entrada_data, pedido_entrada_status, fornecedor_fornecedor_id=None): #definição de campos
        self.usuario_senha = usuario_senha
        self.usuario_nome = usuario_nome
        self.pedido_entrada_nome = pedido_entrada_nome
        self.pedido_entrada_data = pedido_entrada_data
        self.pedido_entrada_status = pedido_entrada_status
        self.fornecedor_fornecedor_id = fornecedor_fornecedor_id

    def validar_pedido_entrada (self): #executa as validações e retorna o erro
        erros = [
            Manipular.validar_vazio (self.pedido_entrada_nome, "pedido_entrada_nome"), #campo não pode ser vazio
            Manipular.validar_vazio (self.pedido_entrada_data, "pedido_entrada_data"), #campo não pode ser vazio
            Manipular.validar_vazio (self.pedido_entrada_status, "pedido_entrada_status"), #campo não pode ser vazio
            Manipular.validar_data(self.pedido_entrada_data, "pedido_entrada_data") #validação da data
        ]
        return [ erro for erro in erros if erro] #retorna o erro
    
    @staticmethod
    def converter_data(data_str): #def para converter data
        formatos = ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d'] #tipos de formatos aceitos na converção de data
        for formato in formatos:
            try:
                return datetime.strptime(data_str.strip(), formato).strftime('%Y-%m-%d')
            except ValueError:
                continue
        return None #retorno de não sucesso
    
    def gravar_pedido_entrada (self): #def para gravar pedido entrada
        pedido_entrada = self.gravar()

        if not pedido_entrada:
            raise ValueError("Erro ao cadastrar pedido de entrada.") #se algo der errado, essa mensagem é exibida

        return pedido_entrada #se der certo retorna o pedido_entrada

    @classmethod
    def relacao_entre_tabelas(cls, id): #def usada para estabelecer relação entre tabelas
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

    def deletar_pedido_entrada(cls, id): #def para cadastrar pedido entrada
        pedido_entrada = cls.buscar_por_id(id) #buscando pedido entrada por id

        if not pedido_entrada:
            raise ValueError("Pedido de entrada não encontrado.") #se não encontrar o pedido, retorna essa mensagem
        if cls.relacao_entre_tabelas(id):
            raise ValueError("Não é possível excluir o pedido de entrada porque ele possui pedidos ou movimentações vinculadas.") #se outros campos estiverem ligados ao pedido entrada, esse não pode ser excluido
        cls.deletar(id) #se der certo, deleta

        return "Pedido de entrada deletado com sucesso!" #menagem de sucesso 

    def atualizar_pedido_entrada(self, id): #def para atualizar pedido entrada
        pedido_entrada = self.buscar_por_id(id)

        if not pedido_entrada:
            raise ValueError("Pedido de entrada não encontrado!") #se não encontrar o pedido, retorna essa mensagem
        if self.relacao_entre_tabelas(id):
            raise ValueError("Não é possível atualizar o pedido de entrada porque ele possui pedidos ou movimentações vinculadas.") #se outros campos estiverem ligados ao pedido entrada, esse não pode ser atualizado
        self.atualizar(id) #se der certo, atualiza

        return "Pedido de entrada atualizado com sucesso!" #menagem de sucesso 
    
    @classmethod
    def buscar_todo_pedido_entrada(cls, order_by="pedido_entrada_nome"): #def para buscar todo pedido entrada
        pedido_entrada = cls.buscar_tudo(order_by) 

        if not pedido_entrada:
            raise ValueError("Pedidos de entrada não encontrados") #se não encontrar o pedido, retorna essa mensagem

        return pedido_entrada #se der certo, retorna o pedido entrada

class Item_pedido_entrada(Crud_base): 
    tabela = "item_pedido_entrada" #nome da tabela no banco
    pk = "item_pedido_entrada_id"  #chave primária
    fields = ["item_pedido_entrada_nome" ,"item_pedido_entrada_lote", "item_pedido_entrada_quantidade","item_pedido_entrada_validade", "item_pedido_entrada_valor_unitario", "pedido_entrada_pedido_entrada_id", "produto_produto_id"]

    def __init__(self, item_pedido_entrada_lote,item_pedido_entrada_quantidade,item_pedido_entrada_validade,item_pedido_entrada_valor_unitario, item_pedido_entrada_nome, pedido_entrada_pedido_entrada_id, produto_produto_id): #definição de campos
        self.usuario_senha = usuario_senha
        self.item_pedido_entrada_lote = item_pedido_entrada_lote
        self.item_pedido_entrada_quantidade = item_pedido_entrada_quantidade
        self.item_pedido_entrada_validade = item_pedido_entrada_validade
        self.item_pedido_entrada_valor_unitario = item_pedido_entrada_valor_unitario
        self.item_pedido_entrada_nome = item_pedido_entrada_nome
        self.pedido_entrada_pedido_entrada_id= pedido_entrada_pedido_entrada_id
        self.produto_produto_id = produto_produto_id

    def validar_item_pedido_entrada (self): #executa as validações e retorna o erro
        erros = [
            Manipular.validar_vazio (self.item_pedido_entrada_nome, "item_pedido_entrada_nome"), #campo não pode ser vazio
            Manipular.validar_vazio (self.item_pedido_entrada_lote, "item_pedido_entrada_lote"), #campo não pode ser vazio
            Manipular.validar_vazio (self.item_pedido_entrada_quantidade, "item_pedido_entrada_quantidade"), #campo não pode ser vazio
            Manipular.validar_vazio (self.item_pedido_entrada_valor_unitario, "item_pedido_entrada_valor_unitario"), #campo não pode ser vazio
            Manipular.validar_numero_negativo (self.item_pedido_entrada_quantidade, "item_pedido_entrada_quantidade"), #campo não pode ter numero negativo
            Manipular.validar_numero_negativo (self.item_pedido_entrada_valor_unitario, "item_pedido_entrada_valor_unitario"), #campo não pode ter numero negativo
            Manipular.validar_data(self.item_pedido_entrada_validade, "item_pedido_entrada_validade") #validação da data
        ]

        return [ erro for erro in erros if erro] #retorna o erro
    
    def gravar_item_pedido_entrada(self, numero): #def pra gravar item pedido entrada
        self.pedido_entrada_pedido_entrada_id= numero #busca pelo numero
        itens = self.gravar() #grava item do pedido

        if not itens:
            raise ValueError("Erro ao cadastrar item de pedido de entrada.")

        conexao = Database.connect() #conectando com o banco
        cursor = conexao.cursor() 

        try: #atualizando no banco
            #soma quantia do item ao estoque atual
            sql = """  
                UPDATE estoque 
                SET estoque_quantidade = estoque_quantidade + %s
                WHERE produto_produto_id = %s
            """

            valores = (
                self.item_pedido_entrada_quantidade, #quanto entrou     
                self.produto_produto_id #qual produto entrou
            )
            
            cursor.execute(sql, valores)
            conexao.commit() #confirma a alteração do banco            
            return itens
            
        except Exception as e:
            conexao.rollback() #se der erro, desfaz a alteração
            raise ValueError(f"Erro ao cadastrar o estoque do produto: {e}")
            
        finally: #fechamento de cursor e conexão
            cursor.close()
            conexao.close() 
        
        
        

    def deletar_item_pedido_entrada(cls, id): #função para deletar item pedido 
        item_pedido_entrada = cls.buscar_por_id(id) #confirma que o item peido existe

        if not item_pedido_entrada:
            raise ValueError("Item de Pedido de entrada não encontrado.") #se não encontrar o item pedido, retorna essa mensagem
        if cls.relacao_entre_tabelas(id):
            raise ValueError("Não é possível excluir o item de pedido de entrada porque ele possui pedidos ou movimentações vinculadas.") #se o item pedido possuir movimentações atreladas a ele, não será possivel exclui-lo
        cls.deletar(id) #se der certo, deleta

        return "Item de Pedido de entrada deletado com sucesso!" #mensagem de sucesso

    def atualizar_item_pedido_entrada(self, id): #atualização do item pedido
        item_pedido_entrada = self.buscar_por_id(id) #busca o item pedido entrada pelo id

        if not item_pedido_entrada:
            raise ValueError("Item de pedido de entrada não encontrado!") #mensagem de retorno, caso não encontre vai apresentar essa mensagem

        quantidade_antiga = int(item_pedido_entrada["item_pedido_entrada_quantidade"])
        quantidade_nova = int(self.item_pedido_entrada_quantidade) 
        diferenca = quantidade_nova - quantidade_antiga #atualização de quantia de item pedido entraa

        self.atualizar(id) #grava os novos dados do item

        if diferenca != 0:
            conexao = Database.connect()
            cursor = conexao.cursor()
            try: #a função só pode ser realizada se a quantia no estoque realmente tiver mudado
                sql = """
                    UPDATE estoque
                    SET estoque_quantidade = estoque_quantidade + %s
                    WHERE produto_produto_id = %s
                """
                cursor.execute(sql, (diferenca, self.produto_produto_id))
                conexao.commit() #confirma a alteração do banco 
            except Exception as e:
                conexao.rollback() #se der erro, desfaz a alteração
                raise ValueError(f"Erro ao ajustar o estoque do produto: {e}") #mensagem de erro
            finally: #fechamento de cursor e conexão
                cursor.close()
                conexao.close()

        return "Item de pedido de entrada atualizado com sucesso!" #mensagem de sucesso

    @classmethod
    def buscar_item_pedido_entrada(cls, order_by="item_pedido_entrada_id"):
        item_pedido_entrada = cls.buscar_tudo(order_by)

        if not item_pedido_entrada:
            raise ValueError("item_pedido_entrada não encontrado.") 

        return item_pedido_entrada


    @classmethod
    def buscar_por_pedido_entrada(cls, pedido_entrada_id):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            sql = f"SELECT * FROM {cls.tabela} WHERE pedido_entrada_pedido_entrada_id = %s"
            cursor.execute(sql, (pedido_entrada_id,))
            colunas = [desc[0] for desc in cursor.description]
            linhas = cursor.fetchall()
            return [dict(zip(colunas, linha)) for linha in linhas]
        finally:
            cursor.close()
            conexao.close()
   

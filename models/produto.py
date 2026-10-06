# ===== Importar as classes =====#
from core.crud_base import Crud_base
from core.manipular import Manipular
from core.conectar import Database
import base64
import os
from datetime import datetime

# ===== Cria a classe GerenciamentoPerfil ===#
class Produto(Crud_base):
    tabela = "produto"
    pk = "produto_id"

    # Define a tabela e os campos do banco  
    fields = ["produto_nome", "produto_descricao", "produto_categoria", "usuario_usuario_id", "produto_imagem", "imagem_tipo", "imagem_blob"]
    fields_estoque = ["estoque_quantidade", "estoque_observacao", "produto_produto_id", "produto_usuario_usuario_id"]


    #Essa def esta definindo os campos
    def __init__(self, produto_nome, produto_descricao, produto_categoria, usuario_usuario_id=None, produto_imagem=None, imagem_tipo=None, imagem_blob=None, **kwargs):
        self.produto_nome = produto_nome
        self.produto_descricao = produto_descricao
        self.produto_categoria = produto_categoria
        self.usuario_usuario_id = usuario_usuario_id
        self.produto_imagem = produto_imagem
        self.imagem_tipo = imagem_tipo
        self.imagem_blob = imagem_blob

    def validar_produto(self):
        erros = [
            Manipular.validar_vazio(self.produto_nome, "nome"),# verifica se os dados estão vazio
            Manipular.validar_vazio(self.produto_categoria, "categoria"),# verifica se os dados estão vazio
            Manipular.validar_not_caracter(self.produto_nome, "nome"),# verifica se os dados estão aceitando caractere especial
            Manipular.validar_min_caracter(self.produto_nome, "nome"),# verifica se os dados estão aceitando menos que 3 caracteres
            Manipular.validar_letra(self.produto_nome, "nome"),# verifica se os dados estão aceitando numeros
            Manipular.validar_not_caracter(self.produto_descricao, "descricao"),# verifica se os dados estão aceitando caractere especial
        ]

        return [ erro for erro in erros if erro] # Retorna  os erros 


      # ====== Método para gravar o produto ===== #
    def gravar_produto(self, estoque_quantidade=0, estoque_observacao=None):
        produto_id = self.gravar() # chama o método gravar do Crud_base e recebe o id gerado

        if not produto_id: # verifica se foi encontrado
            raise ValueError("Erro ao cadastrar produto.") #retorna se tiver erro
        
            
        return produto_id # retorna os dados encontrado
    
    # ====== Método para verificar relação com outras tabelas ===== #
    @classmethod
    def relacao_entre_tabelas(cls, id):
        '''
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            queries = [
                "SELECT COUNT(*) FROM movimentacao WHERE produto_id = %s",
                "SELECT COUNT(*) FROM pedido_movimentacao WHERE produto_id = %s"
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


     # ====== Método para deletar os dados do produto ===== #
    @classmethod
    def deletar_produto(cls, id):
        produto = cls.buscar_por_id(id) # chama o método para de buscar por id do Crud_base
        if not produto: # verifica se foi encontrado
            raise ValueError("Produto não encontrado") # retorna se tiver erro
        
        #===== começa a conexao do banco ====#
        conexao = Database.connect() 
        cursor = conexao.cursor()
        try:
            # 1. Apagar os dependentes (filhos) na tabela item_pedido_saida
            query_deletar_saidas = """
                DELETE FROM item_pedido_saida 
                WHERE produto_produto_id = %s
            """
            cursor.execute(query_deletar_saidas, (id,))

            # 2. Apagar os dependentes (filhos) na tabela item_pedido_entrada
            query_deletar_entradas = """
                DELETE FROM item_pedido_entrada 
                WHERE produto_produto_id = %s
            """
            cursor.execute(query_deletar_entradas, (id,))
            
            # 3. Agora sim, com os filhos apagados, deletamos o registo "Pai" na tabela estoque.
            query_deletar_pai = "DELETE FROM estoque WHERE produto_produto_id = %s"
            cursor.execute(query_deletar_pai, (id,))
            
            # Confirma as exclusões na base de dados
            conexao.commit()
            
        except Exception as e:
            # Se der qualquer erro, desfaz tudo
            conexao.rollback()
            raise e # repassa o erro
            
        finally:
            cursor.close() # fecha o cursor
            conexao.close() # fecha a conexão
        
        cls.deletar(id) #deleta no Crud_base o produto em si
        return "Produto deletado com sucesso" #Returna que foi deletado
    

    # ====== Método para atualizar os dados do produto ===== #
    def atualizar_produto(self, id):
        produto = self.buscar_por_id(id) # chama o método para de buscar por id do Crud_base
        if not produto: # verifica se foi encontrado
            raise ValueError("Produto não encontrado!") #retorna se tiver erro
        if self.relacao_entre_tabelas(id): # verifica se tem pedidos ou movimentações vinculadas
            raise ValueError("Não é possível atualizar o produto porque ele possui pedidos ou movimentações vinculadas.")
        self.atualizar(id) # chama o método de atualizar do Crud_base

        return "Produto atualizado com sucesso!" # retorna se os dados foram atualizados
        
    @classmethod
    def buscar_produto_id(cls, id): 
        produto = cls.buscar_por_id(id) # chama o método para de buscar por id do Crud_base

        if not produto:  # verifica se foi encontrado
            raise ValueError("Produto não encontrado") #retorna se tiver erro
        
        produto["imagem_base64"] = None # começa sem imagem
        if produto.get("imagem_blob"): # verifica se o produto tem imagem salva
            produto["imagem_base64"] = base64.b64encode(produto["imagem_blob"]).decode("utf-8") 
        else:
            produto["imagem_base64"] = None # sem imagem

        return produto # retorna os dados encontrados

     # ===== Método para buscar todos os produtos com o estoque ===== #
    @classmethod
    def buscar_todo_produto(cls, order_by="produto_nome"):
        conexao = Database.connect() # abre a conexão com o banco
        cursor = conexao.cursor(dictionary=True) # retorna os resultados como dicionário

        try:
        # retorna os resultados como dicionário
            sql = f"""
            SELECT p.*, COALESCE(e.estoque_quantidade, 0) AS estoque_quantidade
            FROM produto p
            LEFT JOIN (
                SELECT produto_produto_id, SUM(estoque_quantidade) AS estoque_quantidade
                FROM estoque
                GROUP BY produto_produto_id
            ) e ON e.produto_produto_id = p.produto_id
            ORDER BY p.{order_by}
            """
            cursor.execute(sql)
            produtos = cursor.fetchall()  # pega todos os produtos encontrados

            for produto in produtos: # percorre cada produto
                produto["imagem_base64"] = None
                if produto.get("imagem_blob"): # verifica se tem imagem
                    produto["imagem_base64"] = base64.b64encode(produto["imagem_blob"]).decode("utf-8") # converte a imagem para base64

            return produtos # retorna a lista de produtos
        finally:
            cursor.close() # fecha o cursor
            conexao.close() # fecha a conexão

     # ===== Método para filtrar o estoque por categoria ===== #
    @classmethod
    def filtro_categoria(cls, categoria):
        if not categoria: #verifica se foi encontrada 
            return [] #retorna lista vazia se não tiver categoria

        conexao = Database.connect() #conexão com o banco
        cursor = conexao.cursor(dictionary=True) #retorna o resultado como dicionario

        try:
           #soma o estoque de todos os produtos da categoria 
            sql = """
                SELECT p.produto_categoria, SUM(e.estoque_quantidade) AS estoque_quantidade 
                FROM produto p
                LEFT JOIN estoque e ON e.produto_produto_id = p.produto_id
                WHERE p.produto_categoria = %s
                GROUP BY p.produto_categoria;
                """

            cursor.execute(sql, (categoria,))
            resultados = cursor.fetchall() #pega o resultado da busca

           
            if resultados: #verifica que algo foi encontrado
                return resultados #retorna os dados encontrados
            else:
                return []  #retorna lista vazia se não encontrou
                
        except Exception as e:
            print(f"Erro na busca por categoria: {e}") #mostra o erro no trminal
            return [] # retorna lista vazia se der erro
            
        finally:
            cursor.close()
            conexao.close()
    

    # ===== Método para contar produto por quantidade ===== #
    @classmethod
    def contar_produtos(cls, order_by="produto_id"):
        produto = cls.buscar_tudo(order_by) # chama o método para de buscar tudo do Crud_base
        if not produto: # verifica se foi encontrado
            raise ValueError("Produto não encontrato") # retorna se tiver erro
        produtos = 0 #conta os produtos
        for i in produto: #percorre cada produto
            produtos = produtos + 1 #soma 1 cada produto
        return produtos #retorna o total de produtos


# produto.py

    # ===== Método para buscar os produtos vencidos ===== #
    @staticmethod
    def buscar_vencidos_db(nome=None, quantidade=None):
        """
        Busca produtos vencidos tratando o campo VARCHAR de validade
        e agrupa por produto.
        """
        conexao = None 
        cursor = None 


        #busca o produto com validade menos que a data de hoje 
        try:
            conexao = Database.connect() #conexão com o banco
            cursor = conexao.cursor(dictionary=True) #retorna como dicionario

            query = """
                SELECT 
                    p.produto_id,
                    p.produto_nome,
                    p.produto_categoria,
                    COALESCE(e.estoque_quantidade, 0) AS estoque_quantidade

                FROM item_pedido_entrada ipe

                INNER JOIN produto p 
                    ON p.produto_id = ipe.produto_produto_id

                LEFT JOIN estoque e 
                    ON e.produto_produto_id = p.produto_id

                WHERE 
                    (
                        STR_TO_DATE(ipe.item_pedido_entrada_validade, '%Y-%m-%d') < CURDATE()
                        OR
                        STR_TO_DATE(ipe.item_pedido_entrada_validade, '%d/%m/%Y') < CURDATE()
                    )
            """

            parametros = [] #lista com os valores do filtro 

            if nome: #se informou o nome, filtra por ele
                query += " AND p.produto_nome LIKE %s"
                parametros.append(f"%{nome}%")

            if quantidade is not None: # se informou quantidade, filtra por ele
                query += " AND e.estoque_quantidade = %s"
                parametros.append(quantidade)

            query += """
                GROUP BY 
                    p.produto_id, 
                    p.produto_nome, 
                    p.produto_categoria, 
                    e.estoque_quantidade
                ORDER BY p.produto_nome ASC
            """

            cursor.execute(query, tuple(parametros))
            return cursor.fetchall() #retorna os produtos vencidos 

        finally:
            if cursor is not None:
                cursor.close()
            if conexao is not None:
                conexao.close()
    

    # ====== Método para somar o estoque total ==== #
    @classmethod
    def total_estoque(cls):
        conexao = Database.connect() #conexão com o banco
        cursor = conexao.cursor(dictionary=True) #retorna com dicionario
        try:
            #soma a quantidade de todo o estoque 
            sql = """
            SELECT SUM(e.estoque_quantidade) AS total
            FROM estoque e;
            """
            cursor.execute(sql)
            resultado = cursor.fetchone() # pega o resultado da soma

            if not resultado: # verifica se encontrou alguma coisa
                return ValueError("Nenhum produto encontrado") 

            return resultado['total'] if resultado and resultado['total'] else 0 #retorna o total
        except Exception as e:
            print(f"Erro ao buscar total de estoque: {e}") #mostra o erro no terminal 
            return 0
        finally:
            cursor.close()
            conexao.close()


    # ===== Método para buscar o nome do produto pelo id ===== #
    @classmethod
    def buscar_nome_produto(cls, produto_id):
        # Exemplo utilizando consulta ao banco (ajuste conforme o seu banco/ORM)
        conexao = Database.connect() #conexão com o banco
        cursor = conexao.cursor() 
        cursor.execute("SELECT produto_nome FROM produto WHERE produto_id = %s", (produto_id,))
        resultado = cursor.fetchone() # pega o resultado da busca 
        return resultado[0] if resultado else "" #retorna o nome ou vazio se não encontro


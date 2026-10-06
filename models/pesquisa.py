from core.crud_base import Crud_base
from core.manipular import Manipular 
from core.conectar import Database

class Pesquisa(Crud_base):
    tabela = "produto"
    pk = "produto_id"

    def __init__(self, produto_nome):
        self.produto_nome = produto_nome
    #Valida se não está vazio o nome e a categoria
    def validar_produto(self):
        erros = [
            Manipular.validar_vazio(self.produto_nome, "nome"),
            Manipular.validar_vazio(self.produto_categoria, "categoria")
        ]

        return [ erro for erro in erros if erro]
    
    
    from core.conectar import Database

    # Busca o produto
    @classmethod
    def buscar_tudo_pesquisa(cls, termo): #termo escrito pelo usuário na barra de pesquisa
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        sql = "SELECT * FROM produto WHERE produto_nome LIKE %s" #armazena o código usado para ser usado no banco, nesse a busca
        cursor.execute(sql, (f"%{termo}%",)) # Executa o código sql, junto do termo digitado pelo usuário na barra de pesquisa
        resultados = cursor.fetchall() #retorna todos os resultados encontrados

        cursor.close()
        conexao.close()

        return resultados #retorna os resultado obtidos do select do banco, ou seja, o produto encontrado ou a fala dele

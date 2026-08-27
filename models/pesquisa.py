from core.crud_base import Crud_base
from core.manipular import Manipular 
from core.conectar import Database

class Pesquisa(Crud_base):
    tabela = "produto"
    pk = "produto_id"

    def __init__(self, produto_nome):
        self.produto_nome = produto_nome

    def validar_produto(self):
        erros = [
            Manipular.validar_vazio(self.produto_nome, "nome"),
            Manipular.validar_vazio(self.produto_categoria, "categoria")
        ]

        return [ erro for erro in erros if erro]
    
    
    from core.conectar import Database


    @classmethod
    def buscar_tudo_pesquisa(cls, termo):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        sql = "SELECT * FROM produto WHERE produto_nome LIKE %s"
        cursor.execute(sql, (f"%{termo}%",))
        resultados = cursor.fetchall()

        cursor.close()
        conexao.close()

        return resultados

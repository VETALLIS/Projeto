from core.crud_base import Crud_base
from core.conectar import Database

class Estoque(Crud_base):
    tabela = "estoque"
    pk = "estoque_id"
    fields = ["produto_produto_id", "estoque_quantidade", "estoque_observacao", "produto_usuario_usuario_id"]

    def __init__(self, produto_produto_id, estoque_observacao, produto_usuario_usuario_id, estoque_quantidade=0):
        self.produto_produto_id = produto_produto_id
        self.estoque_quantidade = estoque_quantidade
        self.estoque_observacao = estoque_observacao
        self.produto_usuario_usuario_id = produto_usuario_usuario_id

    def gravar_estoque(self):
        gravar = self.gravar()

        if not gravar:
            raise ValueError("Erro ao cadastrar estoque.")

        return gravar

    
    @staticmethod
    def buscar_estoque_por_produto(produto_id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            cursor.execute("SELECT estoque_id FROM estoque WHERE produto_produto_id = %s LIMIT 1", (produto_id,))
            resultado = cursor.fetchone()
            if not resultado:
                raise ValueError("Estoque não encontrado para esse produto.")
            return resultado["estoque_id"]
        finally:
            cursor.close()
            conexao.close()

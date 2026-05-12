from core.crud_base import Crud_base
from core.manipular import Manipular

class produto(Crud_base):

    # Define a tabela e os campos do banco
    tabela = "produto"
    fields = ["produto_id","produto_nome", "produto_descricao", "produto_categoria", "usuario_usuario_id"]

    # Define os atributos 
    def __init__(self, produto_id, produto_nome, produto_descricao, produto_categoria, usuario_usuario_id):
        self.produto_id = produto_id
        self.produto_nome = produto_nome
        self.produto_descricao = produto_descricao
        self.produto_categoria = produto_categoria
        self.usuario_usuario_id = usuario_usuario_id

    @classmethod
    def low_stock(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM produto WHERE id=%s"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    
    def deletar_produto(self, id):
        produto = self.buscar_por_id(id)

        if not produto:
            raise ValueError("Produto não encontrado")

        self.deletar()
        return "Produto deletado com sucesso!"

    def atualizar_produto(self, id):
        produto = self.buscar_por_id(id)

        if not produto:
            raise ValueError("Produto não encontrado")

        self.atualizar()
        return "Produto atualizado com sucesso!"

    def buscar_produto(self):
        produto  = self.buscar_por_id(id)

        if not produto:
            raise ValueError("Produto não encontrado!")

        return produto(**produto)

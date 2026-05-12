from core.crud_base import Crud_base
from core.conectar import Database

class Informacao_Produto(Crud_base):

    tabela = "produto"
    fields = ["produto_id", "produto_nome", "produto_descricao", "produto_categoria", "usuario_usuario_id"]

    def __init__(self, produto_id, produto_nome, produto_descricao, produto_categoria, usuario_usuario_id):
        self.produto_id = produto_id
        self.produto_nome = produto_nome
        self.produto_descricao = produto_descricao
        self.produto_categoria = produto_categoria
        self.usuario_usuario_id = usuario_usuario_id


    @classmethod
    def buscar_produto(cls, produto_id):
        produto = cls.buscar_por_id(produto_id)

        if not produto:
            raise ValueError("Produto não encontrado!")

        return produto

    def deletar_produto(self, produto_id):
        produto = self.buscar_por_id(produto_id)

        if not produto:
            raise ValueError("Produto não encontrado")

        produto.deletar()
        return "Produto deletado com sucesso!"

    def atualizar_produto(self, produto_id):
        produto = self.buscar_por_id(produto_id)

        if not produto:
            raise ValueError("Produto não encontrado")

        produto.atualizar()
        return "Produto atualizado com sucesso!"
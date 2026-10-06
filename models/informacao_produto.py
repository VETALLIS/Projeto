from core.crud_base import Crud_base # Importo a classe Crud_base, porque essa classe vai HERDAR dela
from core.conectar import Database # Importo o Database pra conseguir abrir conexão nos métodos que têm SQL próprio
import base64 # base64 serve pra transformar a imagem (bytes) em texto
import os

class Informacao_Produto(Crud_base): # Essa classe representa um produto. O (Crud_base) entre parênteses significa herança:
# ela é uma "filha" da Crud_base e aproveita tudo que a mãe tem

    tabela = "produto"  # aqui eu preencho as variáveis que a Crud_base deixou vazias:
    pk = "produto_id"
    fields = ["produto_id", "produto_nome", "produto_descricao", "produto_categoria", "usuario_usuario_id", "produto_imagem", "imagem_tipo","imagem_blob"]

    def __init__(self, produto_id, produto_nome, produto_descricao, produto_categoria, usuario_usuario_id,produto_imagem, imagem_tipo, imagem_blob ):
        # guardo cada valor recebido dentro do objeto (self)
        # os nomes precisam ser iguais aos de "fields", porque o getattr da Crud_base usa eles
        self.produto_id = produto_id
        self.produto_nome = produto_nome
        self.produto_descricao = produto_descricao
        self.produto_categoria = produto_categoria
        self.usuario_usuario_id = usuario_usuario_id
        self.produto_imagem = produto_imagem
        self.imagem_tipo = imagem_tipo
        self.imagem_blob = imagem_blob




    @classmethod
    def buscar_produto_com_estoque(cls, produto_id):
        """Busca produto + estoque usando JOIN"""
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = (
                "SELECT p.produto_id, p.produto_nome, p.produto_descricao, p.produto_imagem , p.imagem_tipo, p.imagem_blob,"
                "p.produto_categoria, p.usuario_usuario_id, e.estoque_id, "
                "e.estoque_quantidade, e.estoque_observacao "
                "FROM produto p "
                "LEFT JOIN estoque e ON p.produto_id = e.produto_produto_id "
                 # LEFT JOIN = traz o produto mesmo que ele ainda não tenha estoque cadastrado
                "WHERE p.produto_id = %s"
            )
            cursor.execute(sql, (produto_id,))

            produto = cursor.fetchone()   # fetchone pega só uma linha (um produto só)

            produto["imagem_base64"] = None
            if produto.get("imagem_blob"):
                produto["imagem_base64"] = base64.b64encode(produto["imagem_blob"]).decode("utf-8")
            else:
                produto["imagem_base64"] = None
            
            return produto
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def buscar_produto(cls, produto_id):
        """Mantém compatibilidade com o método anterior"""
        produto = cls.buscar_produto_com_estoque(produto_id)

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
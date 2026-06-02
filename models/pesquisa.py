from core.crud_base import Crud_base
from core.manipular import Manipular 

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
    
    
    @classmethod
    def buscar_tudo_pesquisa(cls, dados):
        produto = cls.buscar_pesquisa(dados)

        if not produto:
            raise ValueError("Produtos não encontrado")

        return produto

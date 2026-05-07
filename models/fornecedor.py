from core.crud_base import Crud_base
from core.manipular import Manipular 

class Fornecedor(Crud_base):
    tabela = "fornecedor"
    fields = ["fornecedor_nome", "fornecedor_cnpj", "fornecedor_endereco", "fonecedor_pedido_minimo", "fornecedor_tipo_produtos"]

    def __init__(self, fornecedor_nome, fornecedor_cnpj, fornecedor_endereco, fornecedor_pedido_minimo, fornecedor_tipo_produtos):
        self.fornecerdor_nome = fornecedor_nome
        self.fornecedor_cnpj = fornecedor_cnpj
        self.fornecedor_endereco = fornecedor_endereco
        self.fornecedor_pedido_minimo = fornecedor_pedido_minimo
        self.fornecedor_tipo_produtos = fornecedor_tipo_produtos

    def validar_fornecedor(self):
        erros = [
            Manipular.validar_vazio(self.fornecerdor_nome, "nome"),
            Manipular.validar_vazio(self.fornecedor_cnpj, "cnpj"),
            Manipular.validar_vazio(self.fornecedor_endereco, "endereço")
        ]          
    
        return [ erro for erro in erros if erro]

    def gravar_fornecedor(self):
        fornecedor = self.gravar()

        if not fornecedor:
            raise ValueError("Erro ao criar fornecedor!")

        return "Fornecedor criado com sucesso"

    def deletar_fornecedor(self, id):
        fornecedor = self.buscar_por_id(id)

        if not fornecedor:
            raise ValueError("Fornecedor não encontrado")

        self.deletar()
        return "Fornecedor deletado com sucesso!"

    def atualizar_fornecedor(self, id):
        fornecedor = self.buscar_por_id(id)

        if not fornecedor:
            raise ValueError("Fornecedor não encontrado")

        self.atualizar()
        return "Fornecedor atualizado com sucesso!"

    def buscar_fornecedor(self):
        fornecedor  = self.buscar_por_id(id)

        if not fornecedor:
            raise ValueError("Fornecedor não encontrado!")

        return Fornecedor(**fornecedor)
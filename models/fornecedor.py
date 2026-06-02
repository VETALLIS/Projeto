from core.crud_base import Crud_base
from core.manipular import Manipular 

class Fornecedor(Crud_base):
    tabela = "fornecedor"
    fields = ["fornecedor_nome", "fornecedor_cnpj", "fornecedor_endereço", "fornecedor_pedido_minimo", "fornecedor_tipo_produtos"]

    def __init__(self, nome, cnpj, endereço, pedido_minimo, tipo_produtos):
        self.fornecedor_nome = nome
        self.fornecedor_cnpj = cnpj
        self.fornecedor_endereço = endereço
        self.fornecedor_pedido_minimo = pedido_minimo
        self.fornecedor_tipo_produtos = tipo_produtos

    def validar_fornecedor(self):
        erros = [
            Manipular.validar_vazio(self.fornecedor_nome, "nome"),
            Manipular.validar_vazio(self.fornecedor_cnpj, "cnpj"),
            Manipular.validar_vazio(self.fornecedor_endereço, "endereço"),
            Manipular.validar_vazio(self.fornecedor_pedido_minimo, "pedido_minimo")
            
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

    def buscar_fornecedor_id(self):
        fornecedor  = self.buscar_por_id(id)

        if not fornecedor:
            raise ValueError("Fornecedor não encontrado!")

        return Fornecedor(**fornecedor)
    
    def buscar_fornecedor(cls):
        fornecedor  = cls.buscar_tudo()

        if not fornecedor:
            raise ValueError("Fornecedor não encontrado!")

        return fornecedor
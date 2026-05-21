from core.crud_base import Crud_base
from core.conectar import Database
from core.manipular import Manipular

class Lista_compra(Crud_base):

    tabela = "lista_compra"
    pk = "lista_compra_id"
    fields = [
            "lista_compra_nome", 
            "lista_compra_quantidade", 
            "lista_compra_valor", 
            "lista_compra_status", 
            "estoque_estoque_id"
        ]

    def __init__(self, lista_compra_nome, lista_compra_quantidade, lista_compra_valor, lista_compra_status="Pendente", estoque_estoque_id=None, **kwargs):
        self.lista_compra_nome = lista_compra_nome 
        self.lista_compra_quantidade = lista_compra_quantidade
        self.lista_compra_valor = lista_compra_valor
        self.lista_compra_status = lista_compra_status
        self.estoque_estoque_id = estoque_estoque_id


    def validar_lista_compra(self):
        erros = [
            Manipular.validar_vazio(self.lista_compra_nome, "nome"),
            Manipular.validar_vazio(self.lista_compra_quantidade, "quantidade"),
            Manipular.validar_vazio(self.lista_compra_valor, "valor"),
            Manipular.validar_vazio(self.lista_compra_status, "status")
            
        ]          
    
        return [ erro for erro in erros if erro]

    def gravar_lista_compra(self):
        lista_compra = self.gravar()

        if not lista_compra:
            raise ValueError("Erro ao criar lista de compras!")                                                                                                                     

        return "Lista de compras criada com sucesso"

    def deletar_lista_compra(self, id):
        lista_compra = self.buscar_por_id(id)

        if not lista_compra:
            raise ValueError("Lista de compra não encontrada")

        self.deletar()
        return "Lista de compra deletada com sucesso!"

    def atualizar_lista_compra(self, id):
        lista_compra = self.buscar_por_id(id)

        if not lista_compra:
            raise ValueError("Lista de compra não encontrada")

        self.atualizar()
        return "Lista de compra atualizada com sucesso!"

    def buscar_lista_compra_id(self):
        lista_compra_id = self.buscar_por_id(id)

        if not lista_compra_id:
            raise ValueError("Lista de compra não encontrada!")

        return Lista_compra(**Lista_compra)

    def buscar_lista_compra(cls):
        lista_compra=cls.buscar_tudo()

        if not lista_compra:
            raise ValueError("Lista de compra nãoencontrado")

        return Lista_compra(**lista_compra)
# ===== Importar as classes =====#
from core.crud_base import Crud_base
from core.conectar import Database
from core.manipular import Manipular

# ===== Cria a classe Animal ===#
class Lista_compra(Crud_base):

    # Define a tabela e os campos do banco
    tabela = "lista_compra"
    pk = "lista_compra_id"
    fields = [
            "lista_compra_nome", 
            "lista_compra_quantidade", 
            "lista_compra_valor", 
            "lista_compra_status", 
        ]

    # Define os atributos 
    def __init__(self, lista_compra_nome=None, lista_compra_quantidade=None, lista_compra_valor=None, lista_compra_status="Pendente",  **kwargs):
        self.lista_compra_nome = lista_compra_nome 
        self.lista_compra_quantidade = lista_compra_quantidade
        self.lista_compra_valor = lista_compra_valor
        self.lista_compra_status = lista_compra_status
       

    # Faz a validação dos dados para a gravação com o banco
    def validar_lista_compra(self):
        erros = [
            Manipular.validar_vazio(self.lista_compra_nome, "nome"),# verifica se os dados estão vazio
            Manipular.validar_min_caracter(self.lista_compra_nome, "nome"),# verifica se os dados estão aceitando menos que 3 caracteres
            Manipular.validar_not_caracter(self.lista_compra_nome, "nome"),# verifica se os dados estão aceitando caractere especial
            Manipular.validar_letra(self.lista_compra_nome, "nome"),# verifica se os dados não estão com número
            Manipular.validar_vazio(self.lista_compra_quantidade, "quantidade"),# verifica se os dados estão vazio
            Manipular.validar_numero(self.lista_compra_quantidade, "quantidade"),# verifica se os dados estão com número
            Manipular.validar_vazio(self.lista_compra_valor, "valor"),# verifica se os dados estão vazio
            Manipular.validar_numero(self.lista_compra_valor, "valor"),# verifica se os dados estão com número
            Manipular.validar_vazio(self.lista_compra_status, "status")# verifica se os dados estão vazio

            
        ]          
    
        return [ erro for erro in erros if erro] # Retorna  os erros 

    # ====== Método de gravação dos dados da lista de compra ==== #
    def gravar_lista_compra(self):
        lista_compra = self.gravar() # chama o método gravar da Classe Crude_base

        if not lista_compra: # Verifica se a gravação no banco deu certo
            raise ValueError("Erro ao criar lista de compras!") # Retorna o erro                                                                                                                    

        return "Lista de compras criada com sucesso" # Retorna mensagem de sucesso



    def deletar_lista_compra(self, id): #deletar lista
        lista_compra = self.buscar_por_id(id) #busca lista por id

        if not lista_compra:
            raise ValueError("Lista de compra não encontrada") #se o lista não for encontrado, ele retorna a mensagem

        self.deletar(id)
        return "Lista de compra deletada com sucesso!"#se encontrar deleta e retorna essa mensagem


     # ====== Método para atualizar os dados da lista ===== #
    def atualizar_lista_compra(self, id):
        lista_compra = self.buscar_por_id(id) # chama o método para de buscar por id do Crud_base

        if not lista_compra: # verifica se foi encontrado
            raise ValueError("Lista de compra não encontrada") #retorna se tiver erro

        self.atualizar() # chama o método de atualizar do Crud_base
        return "Lista de compra atualizada com sucesso!"# retorna se os dados foram atualizados



    def buscar_lista_compra_id(self, id):
        lista_compra_id = self.buscar_por_id(id) # chama o método para de buscar por id do Crud_base

        if not lista_compra_id: # verifica se foi encontrado
            raise ValueError("Lista de compra não encontrada!") #retorna se tiver erro

        return Lista_compra(**Lista_compra)

    @classmethod
    def buscar_lista_compra(cls, order_by=pk):
        lista_compra = cls.buscar_tudo(order_by) # chama o método para de buscar por id do Crud_base

        if not lista_compra: # verifica se foi encontrado
            raise ValueError("Nada encontrato") # retorna se tiver erro

        return lista_compra # retorna os dados encontrado
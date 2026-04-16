# Importa a classes
from core.crud_base import Crud_base
from core.manipular import Manipular 

# Cria a classe Fornecedor 
class Fornecedor(Crud_base):
    # define a tabela e os campos para o banco de dados
    tabela = "fornecedor"
    fields = ["fornecedor_nome", "fornecedor_cnpj", "fornecedor_endereco", "fonecedor_pedido_minimo", "fornecedor_tipo_produtos"]

    # define os atributos
    def __init__(self, fornecedor_nome, fornecedor_cnpj, fornecedor_endereco, fornecedor_pedido_minimo, fornecedor_tipo_produtos):
        self.fornecerdor_nome = fornecedor_nome
        self.fornecedor_cnpj = fornecedor_cnpj
        self.fornecedor_endereco = fornecedor_endereco
        self.fornecedor_pedido_minimo = fornecedor_pedido_minimo
        self.fornecedor_tipo_produtos = fornecedor_tipo_produtos

    # vlaida os dados
    def validar_fornecedor(self):
        erros = [
            Manipular.validar_vazio(self.fornecerdor_nome, "nome"), # verifica se os dados estão vazio
            Manipular.validar_vazio(self.fornecedor_cnpj, "cnpj"), # verifica se os dados estão vazio
            Manipular.validar_vazio(self.fornecedor_endereco, "endereço") # verifica se os dados estão vazio
        ]          
    
        return [ erro for erro in erros if erro] #retorna se houver erros

    #Método de gravação dos dados de  fornecedor
    def gravar_fornecedor(self):
        fornecedor = self.gravar() # chama o método gravar do Crud_base

        if not fornecedor: # verifica se foi cadastrado
            raise ValueError("Erro ao criar fornecedor!") # retorna erro

        return "Fornecedor criado com sucesso" # retorna sucesso

    # Método de deletar dados do fornecedor
    def deletar_fornecedor(self, id):
        fornecedor = self.buscar_por_id(id) # Chama o metodo buscar por id do Crud_base

        if not fornecedor: # verifica se foi encontrado
            raise ValueError("Fornecedor não encontrado") # retorna erro

        self.deletar() # Chama a função de deletar do Crud_base
        return "Fornecedor deletado com sucesso!" # retorna sucesso

    # Método para atualizar dados de fornecedor
    def atualizar_fornecedor(self, id):
        fornecedor = self.buscar_por_id(id) # chama o método para procurar fornecedor do Crude_base

        if not fornecedor: # verfifica se foi encontrado 
            raise ValueError("Fornecedor não encontrado") # retorna erro

        self.atualizar() # chama o método atualizar do Crud_base
        return "Fornecedor atualizado com sucesso!" #retorna sucesso

    # Método para buscar fornecedor
    def buscar_fornecedor(self):
        fornecedor  = self.buscar_por_id(id) # chama o método buscar por id do Crud_base

        if not fornecedor: # verifica se foi encontrado
            raise ValueError("Fornecedor não encontrado!") # retorna erro

        return Fornecedor(**fornecedor) # retorna os dados que foram encontrados
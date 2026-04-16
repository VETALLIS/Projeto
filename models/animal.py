# ===== Importar as classes =====#
from core.crud_base import Crud_base
from core.manipular import Manipular

# ===== Cria a classe Animal ===#
class Animal(Crud_base):

    # Define a tabela e os campos do banco
    tabela = "animal"
    fields = ["animal_especie", "animal_quantidade", "animal_sexo", "animal_raca", "animal_identificacao", "animal_idade"]

    # Define os atributos 
    def __init__(self, animal_especie, animal_quantidade, animal_sexo, animal_raca, animal_identificacao, animal_idade):
        self.animal_especie = animal_especie
        self.animal_quantidade = animal_quantidade
        self.animal_sexo = animal_sexo
        self.animal_raca = animal_raca
        self.animal_identificacao = animal_identificacao
        self.animal_idade = animal_idade

    # Faz a validação dos dados para a gravação com o banco
    def validar(self):
        erros = [
            Manipular.validar_vazio(self.animal_especie, "especie"), # verifica se os dados estão vazio
            Manipular.validar_vazio(self.animal_quantidade, "quantidade"), # verifica se os dados estão vazio
            Manipular.validar_vazio(self.animal_sexo, "sexo"), # verifica se os dados estão vazio
            Manipular.validar_vazio(self.animal_raca, "raca"), # verifica se os dados estão vazio
            Manipular.validar_vazio(self.animal_identificacao, "identificacao"), # verifica se os dados estão vazio
            Manipular.validar_vazio(self.animal_idade, "idade"), # verifica se os dados estão vazio
            Manipular.validar_caracter(self.animal_especie, "especie"), # verifica se o dados tem caracteres especiais
            Manipular.validar_caracter(self.animal_quantidade, "quantidade"), # verifica se o dados tem caracteres especiais
            Manipular.validar_caracter(self.animal_sexo, "sexo"), # verifica se o dados tem caracteres especiais
            Manipular.validar_caracter(self.animal_raca, "raca"), # verifica se o dados tem caracteres especiais
            Manipular.validar_caracter(self.animal_identificacao, "identificacao"), # verifica se o dados tem caracteres especiais
        ]

        return [ erro for erro in erros if erro] # Retorna  os erros 

    # ====== Método de gravação dos dados do animal ==== #
    def gravar_animal(self):
        animal = self.gravar() # chama o método gravar da Classe Crude_base

        if not animal: # Verifica se a gravação no banco deu certo
            raise ValueError("Erro ao cadastrar animal.") # Retorna o erro

        return "Animal Cadastrado com sucesso!" # Retorna mensagem de sucesso

    # ===== Método de deletar dados dos animais ===== #
    def deletar_animal(self, id):
        animal = self.buscar_por_id(id) # chama o método de buscar por id do Crud_base

        if not animal: # Verifica se os dados foram encontrados 
            raise ValueError("Animal não encontrado.")

        self.deletar(id) # Chama o método deletar da classe Crud_base
        return "Animal deletado com sucesso!" # retorna se os dados foram deletados

    # ====== Método para atualizar os dados dos animais ===== #
    def atualizar_animal(self, id):
        animal = self.buscar_por_id(id) # busca o animal por id, para ver se está no banco

        if not animal: # verifica se foi encontrado
            raise ValueError("Animal não encontrado.")

        self.atualizar(id) # chama o método de atualizar do Crud_base
        return "Animal autualizado com sucesso!" # retorna se os dados foram atualizados

    # ===== Método para buscar animal pelo id ===== #
    def buscar_animal_por_id(self, id):
        animal = self.buscar_por_id(id) # chama o método para de buscar por id do Crud_base

        if not animal: # verifica se foi encontrado
            raise ValueError("Animal não encontrado.") # retorna se tiver erro

        return Animal(**animal)# retorna os dados encontrado
# ===== Importar as classes =====#
from core.crud_base import Crud_base
from core.manipular import Manipular
from core.conectar import Database

# ===== Cria a classe Animal ===#
class Animal(Crud_base):

    # Define a tabela e os campos do banco
    tabela = "animal"
    pk = "animal_id"
    fields = ["animal_especie","animal_sexo", "animal_raca", "animal_identificacao", "animal_idade"]

    # Define os atributos 
    def __init__(self, animal_especie, animal_sexo, animal_raca, animal_identificacao, animal_idade):
        self.animal_especie = animal_especie
        self.animal_sexo = animal_sexo
        self.animal_raca = animal_raca
        self.animal_identificacao = animal_identificacao
        self.animal_idade = animal_idade

    # Faz a validação dos dados para a gravação com o banco
    def validar_animal(self):
        erros = [
            Manipular.validar_vazio(self.animal_especie, "especie"), # verifica se os dados estão vazio
            Manipular.validar_vazio(self.animal_sexo, "sexo"), # verifica se os dados estão vazio
            Manipular.validar_vazio(self.animal_raca, "raca"), # verifica se os dados estão vazio
            Manipular.validar_vazio(self.animal_identificacao, "identificacao"), # verifica se os dados estão vazio
            Manipular.validar_vazio(self.animal_idade, "idade"), # verifica se os dados estão vazio
        ]

        return [ erro for erro in erros if erro] # Retorna  os erros 

    # ====== Método de gravação dos dados do animal ==== #
    def gravar_animal(self):
        animal = self.gravar() # chama o método gravar da Classe Crude_base

        if not animal: # Verifica se a gravação no banco deu certo
            raise ValueError("Erro ao cadastrar animal.") # Retorna o erro

        return "Animal Cadastrado com sucesso!" # Retorna mensagem de sucesso

    # ===== Método de deletar dados dos animais ===== #
    @classmethod
    def deletar_animal(cls, id):
        animal = cls.buscar_por_id(id)
        if not animal:
            raise ValueError("Animal não encontrado")
        
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            query_deletar_saidas = """
                DELETE FROM pedido_saida 
                WHERE animal_animal_id IN (
                    SELECT animal_id FROM animal WHERE animal_animal_id = %s
                )
            """
            cursor.execute(query_deletar_saidas, (id,))

            query_deletar_pai = "DELETE FROM animal WHERE animal_id = %s"
            cursor.execute(query_deletar_pai, (id,))
            
            conexao.commit()
            
        except Exception as e:
            conexao.rollback()
            raise e 
            
        finally:
            cursor.close()
            conexao.close()
        
        cls.deletar(id)
        return "Animal deletado com sucesso"

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


    @classmethod
    def buscar_animal(cls, order_by="animal_id"):
            animal = cls.buscar_tudo(order_by) # chama o método para de buscar por id do Crud_base
    
            if not animal: # verifica se foi encontrado
                raise ValueError("Animal não encontrado.") # retorna se tiver erro
    
            return animal

    @classmethod
    def contar_animal(cls, order_by=pk):
        animal = cls.buscar_tudo(order_by) # chama o método para de buscar por id do Crud_base

        if not animal: # verifica se foi encontrado
            raise ValueError("Animal não encontrado.  Casdastre um animal!") # retorna se tiver erro

        return animal# retorna os dados encontrado

    @classmethod
    def contar_animais(cls, order_by="animal_id"):
        animal = cls.buscar_tudo(order_by)
        if not animal:
            raise ValueError("Animal não encontrato")
        animais = 0
        for i in animal:
            animais = animais + 1
        return animais


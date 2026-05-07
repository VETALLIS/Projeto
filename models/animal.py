from dataclasses import fields
from core.crud_base import Crud_base
from core.manipular import Manipular

class Animal(Crud_base):
    tabela = "animal"
    fields = ["animal_especie", "animal_quantidade", "animal_sexo", "animal_raca", "animal_identificacao", "animal_idade"]

    def __init__(self, animal_especie, animal_quantidade, animal_sexo, animal_raca, animal_identificacao, animal_idade):
        self.animal_especie = animal_especie
        self.animal_quantidade = animal_quantidade
        self.animal_sexo = animal_sexo
        self.animal_raca = animal_raca
        self.animal_identificacao = animal_identificacao
        self.animal_idade = animal_idade

    def validar(self):
        erros = [
            Manipular.validar_vazio(self.animal_especie, "especie"),
            Manipular.validar_vazio(self.animal_quantidade, "quantidade"),
            Manipular.validar_vazio(self.animal_sexo, "sexo"),
            Manipular.validar_vazio(self.animal_raca, "raca"),
            Manipular.validar_vazio(self.animal_identificacao, "identificacao"),
            Manipular.validar_vazio(self.animal_idade, "idade"),
            Manipular.validar_caracter(self.animal_especie, "especie"),
            Manipular.validar_caracter(self.animal_quantidade, "quantidade"),
            Manipular.validar_caracter(self.animal_sexo, "sexo"),
            Manipular.validar_caracter(self.animal_raca, "raca"),
            Manipular.validar_caracter(self.animal_identificacao, "identificacao"),
        ]

        return [ erro for erro in erros if erro]

    def gravar_animal(self):
        animal = self.gravar()

        if not animal:
            raise ValueError("Erro ao cadastrar animal.")

        return "Animal Cadastrado com sucesso!"

    def deletar_animal(self, id):
        animal = self.buscar_por_id(id)

        if not animal:
            raise ValueError("Animal não encontrado.")

        self.deletar(id)
        return "Animal deletado com sucesso!"

    def atualizar_animal(self, id):
        animal = self.buscar_por_id(id)

        if not animal:
            raise ValueError("Animal não encontrado.")

        self.atualizar(id)
        return "Animal autualizado com sucesso!"

    def buscar_animal_por_id(self, id):
        animal = self.buscar_por_id(id)

        if not animal:
            raise ValueError("Animal não encontrado.")

        return Animal(**animal)
from core.crud_base import Crud_base
from core.manipular import Manipular

class Usuario(Crud_base):
    tabela = "usuario"
    pk = "usuario_id"

    fields = ["usuario_senha", "usuario_nome", "usuario_email", "usuario_cpf", "usuario_cargo" ]

    def __init__(self, usuario_senha, usuario_nome, usuario_email, usuario_cpf, usuario_cargo, usuario_confirmar_senha):
        self.usuario_senha = usuario_senha
        self.usuario_nome = usuario_nome
        self.usuario_email = usuario_email
        self.usuario_cpf = usuario_cpf
        self.usuario_cargo = usuario_cargo
        self.usuario_confirmar_senha = usuario_confirmar_senha

    def validar(self, secret_key):
        erros = [
            Manipular.validar_vazio(self.usuario_senha, "senha"),
            Manipular.validar_vazio(self.usuario_nome, "nome"),
            Manipular.validar_vazio(self.usuario_email, "email"),
            Manipular.validar_vazio(self.usuario_cpf, "cpf"),
            Manipular.validar_vazio(self.usuario_cargo, "cargo"),
            Manipular.validar_vazio(self.usuario_confirmar_senha, "confirmar_senha"),
            Manipular.validar_cpf(self.usuario_cpf, "cpf", secret_key),
            Manipular.validar_email(self.usuario_email, "email", secret_key),
            Manipular.comparar_criacao_senha(self.usuario_senha, self.usuario_confirmar_senha)
        ]

        return [ erro for erro in erros if erro]

    def gravar_usuario(self):
        usuario = self.gravar()

        if not usuario:
            raise ValueError("Erro ao cadastrar usuário.")

        return "Usuário cadastrado com sucesso!"

    @classmethod
    def deletar_usuario(cls, id):
        usuario = cls.buscar_por_id(id)

        if not usuario:
            raise ValueError("Usuario não encontrado.")

        cls.deletar(id)

    def atualizar_usuario(self, id):
        usuario = self.buscar_por_id(id)

        if not usuario:
            raise ValueError("Usuario não encontrado.")
           
        self.atualizar(id)
        return "Usuario atualizado com sucesso!"


    @classmethod
    def buscar_usuario_por_id(cls, id):
        usuario  = cls.buscar_por_id(id)

        if not usuario:
            raise ValueError("Usuario não encontrado.")

        usuario.pop("usuario_id", None)
        return Usuario(**usuario)

    



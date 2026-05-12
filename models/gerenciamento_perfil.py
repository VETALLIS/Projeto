from core.crud_base import Crud_base
from core.manipular import Manipular

class GerenciametoPerfil(Crud_base):
    tabela = "usuario"
    pk = "usuario_id"

    fields = ["usuario_senha", "usuario_nome", "usuario_email", "usuario_cpf", "usuario_cargo" ]

    def __init__(self, usuario_nome, usuario_email, usuario_cargo):
        self.usuario_nome = usuario_nome
        self.usuario_email = usuario_email
        self.usuario_cargo = usuario_cargo

    def validar_perfil(self, secret_key):
        erros = [
            Manipular.validar_vazio(self.usuario_nome, "nome"),
            Manipular.validar_vazio(self.usuario_email, "email"),
            Manipular.validar_vazio(self.usuario_confirmar_senha, "cargo"),
            Manipular.validar_email(self.usuario_email, "email", secret_key),
        ]

        return [ erro for erro in erros if erro]

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
        return GerenciametoPerfil(**usuario)

    



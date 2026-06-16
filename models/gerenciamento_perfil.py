from core.crud_base import Crud_base
from core.manipular import Manipular

class GerenciamentoPerfil(Crud_base):
    tabela = "usuario"
    pk = "usuario_id"

    fields = ["usuario_nome", "usuario_email", "usuario_cargo", "usuario_imagem", "imagem_tipo" , "imagem_blob" ]

    def __init__(self, usuario_nome, usuario_email, usuario_cargo, usuario_id, usuario_imagem, imagem_tipo, imagem_blob):
        self.usuario_nome = usuario_nome
        self.usuario_email = usuario_email
        self.usuario_cargo = usuario_cargo
        self.usuario_id = usuario_id
        self.usuario_imagem = usuario_imagem
        self.imagem_tipo = imagem_tipo
        self.imagem_blob = imagem_blob

    def validar_perfil(self, secret_key):
        erros = [
            Manipular.validar_vazio(self.usuario_nome, "nome"),
            Manipular.validar_vazio(self.usuario_email, "email"),
            Manipular.validar_vazio(self.usuario_cargo, "cargo"),
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
        return GerenciamentoPerfil(**usuario)

    



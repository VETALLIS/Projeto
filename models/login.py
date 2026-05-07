from core.crud_base import Crud_base
from core.manipular import Manipular

class Login(Crud_base):
    
    def __init__(self, login_email, login_senha):
        self.usuario_email = login_email
        self.usuario_senha = login_senha

    def login_validar(self, secret_key):
        erros = [
            Manipular.validar_email(self.usuario_email, "email", secret_key),
            Manipular.validar_vazio(self.usuario_email, "email"),
            Manipular.validar_vazio(self.usuario_senha, "senha")
        ]

        return [ erro for erro in erros if erro]
    
    
    def autenticar_login(self):
        usuario = self.buscar_para_login(self.usuario_email)

        if not usuario:
            raise ValueError("Usuário não encontrado")

        if usuario["usuario_senha"] != self.usuario_senha:
            raise ValueError("Senha incorreta")

        return "Login realizado com sucesso"
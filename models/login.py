# importa as classes 
from core.crud_base import Crud_base
from core.manipular import Manipular

# Cria a classe Login
class Login(Crud_base):
    
    # define os atributos
    def __init__(self, login_email, login_senha):
        self.usuario_email = login_email
        self.usuario_senha = login_senha

    # valida os dados para login
    def login_validar(self, secret_key):
        erros = [
            Manipular.validar_email(self.usuario_email, "email", secret_key), # valida se o email é valido
            Manipular.validar_vazio(self.usuario_email, "email"), # verifica se os dados estão vazio
            Manipular.validar_vazio(self.usuario_senha, "senha") # verifica se os dados estão vazio
        ]

        return [ erro for erro in erros if erro] # retorna erros, se houver
    
    # Método para autenticar login
    def autenticar_login(self):
        usuario = self.buscar_para_login(self.usuario_email) # procura o usuario pelo email, chamando o método buscar_para_login do Crud_base

        if not usuario: # verifica se o email foi rncontrado
            raise ValueError("Usuário não encontrado") # retorna erro se não foi encontrado

        if usuario["usuario_senha"] != self.usuario_senha: # verifica se a senha cadastra com o email, é a mesma que foi adicionada pelo usuario
            raise ValueError("Usuário não encontrado") # retorna erro se a senha estivar incorreta 

        return "Login realizado com sucesso" # retorna sucesso
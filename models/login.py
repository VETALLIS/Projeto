# ===== Importar as classes =====#
from core.crud_base import Crud_base
from core.manipular import Manipular

# ===== Cria a classe GerenciamentoPerfil ===#
class Login(Crud_base):
    
    #Essa def esta definindo os campos
    def __init__(self, login_email, login_senha):
        self.usuario_email = login_email
        self.usuario_senha = login_senha


    def validar_login(self, secret_key):
        erros = [
            Manipular.validar_email(self.usuario_email, "email", secret_key),#verificar se o email esta certo
            Manipular.validar_vazio(self.usuario_email, "email"),# verifica se os dados estão vazio
            Manipular.validar_vazio(self.usuario_senha, "senha")# verifica se os dados estão vazio
        ]

        return [ erro for erro in erros if erro] # Retorna  os erros 
    
    
    # ===== Método para autenticar o login ===== #
    def autenticar_login(self): 
        usuario = self.buscar_para_login(self.usuario_email)# chama o método que busca o usuário pelo email

        if not usuario:# verifica se o usuário foi encontrado
            raise ValueError("Usuário não encontrado")# retorna se não encontrar


        if usuario["usuario_senha"] != self.usuario_senha: # compara a senha do banco com a senha informada
            raise ValueError("Senha incorreta") # retorna se a senha estiver errada

        return "Login realizado com sucesso", usuario # retorna a mensagem de sucesso e os dados do usuário
    
    # ===== Método para buscar login pelo id ===== #
    def buscar_login(self):
        login = self.buscar_por_id() # chama o método para de buscar por id do Crud_base

        if not login: # verifica se foi encontrado
            raise ValueError("Usuario não encontrado") # retorna se tiver erro
        
        return login # retorna
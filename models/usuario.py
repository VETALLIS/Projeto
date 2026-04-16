# Importa as classes
from core.crud_base import Crud_base
from core.manipular import Manipular

# Cria a classe Usuario
class Usuario(Crud_base):
    # define a tabela, PK e os campos para o DB
    tabela = "usuario"
    pk = "usuario_id"
    fields = ["usuario_senha", "usuario_nome", "usuario_email", "usuario_cpf", "usuario_cargo"]

    # define os atributos
    def __init__(self, usuario_senha, usuario_nome, usuario_email, usuario_cpf, usuario_cargo):
        self.usuario_senha = usuario_senha
        self.usuario_nome = usuario_nome
        self.usuario_email = usuario_email
        self.usuario_cpf = usuario_cpf
        self.usuario_cargo = usuario_cargo

    # valida os dados 
    def validar(self, secret_key):
        erros = [
            Manipular.validar_vazio(self.usuario_senha, "senha"), # valida se o dado não esta vazio
            Manipular.validar_vazio(self.usuario_nome, "nome"), # valida se o dado não esta vazio
            Manipular.validar_vazio(self.usuario_email, "email"), # valida se o dado não esta vazio
            Manipular.validar_vazio(self.usuario_cpf, "cpf"), # valida se o dado não esta vazio
            Manipular.validar_vazio(self.usuario_cargo, "cargo"), # valida se o dado não esta vazio
            Manipular.validar_caracter(self.usuario_senha, "senha"), # valida se tem caracteres especiais 
            Manipular.validar_cpf(self.usuario_cpf, "cpf", secret_key), # valida o cpf, com a api do invetexto
            Manipular.validar_email(self.usuario_email, "email", secret_key), # valida o email, com a api do invetexto
        ]

        return [ erro for erro in erros if erro] # retorna se houver erros

    # Método para gravar dados do usuario
    def gravar_usuario(self):
        usuario = self.gravar() # chama o método gravar do Crud_base

        if not usuario: # verifica se foi gravado
            raise ValueError("Erro ao cadastrar usuário.") # retorna se houver erro

        return "Usuário cadastrado com sucesso!" # retorna sucesso


    # Método para deletar dados do usuario
    @classmethod
    def deletar_usuario(cls, id):
        usuario = cls.buscar_por_id(id) # chama o método para buscar do Crud_base

        if not usuario: # verifica s eo usuario foi encontrado
            raise ValueError("Usuario não encontrado.") # retorna se tiver erro

        cls.deletar(id) # chama o metodo deletar do Crud_base

    # Método para atualizar dados do usuario
    def atualizar_usuario(self, id):
        usuario = self.buscar_por_id(id) # chama o método buscar do Crud_base

        if not usuario: # Verifica se foi encontrado
            raise ValueError("Usuario não encontrado.") # retorna se tiver erro
           
        self.atualizar(id) # chama o método para atualizar 
        return "Usuario atualizado com sucesso!" # retorna sucesso

    # Método para buscar usuario pelo id
    @classmethod
    def buscar_usuario_por_id(cls, id):
        usuario  = cls.buscar_por_id(id) # chama o método buscar por id da classe Crud_base

        if not usuario: # verifica se foi encontrado
            raise ValueError("Usuario não encontrado.") # retorna se tiver errro

        usuario.pop("usuario_id", None) # remove o id para retorna par o usuario
        return Usuario(**usuario) # retorna os dados de usuario

    



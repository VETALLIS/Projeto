# ===== Importar as classes =====#
from core.crud_base import Crud_base
from core.manipular import Manipular

# ===== Cria a classe GerenciamentoPerfil ===#
class GerenciamentoPerfil(Crud_base):
    tabela = "usuario"
    pk = "usuario_id"

    # Define a tabela e os campos do banco
    fields = ["usuario_nome", "usuario_email", "usuario_cargo", "usuario_imagem", "imagem_tipo" , "imagem_blob" ]
    
    #Essa def esta definindo os campos
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
            Manipular.validar_vazio(self.usuario_nome, "nome"),# verifica se os dados estão vazio
            Manipular.validar_vazio(self.usuario_email, "email"),# verifica se os dados estão vazio
            Manipular.validar_vazio(self.usuario_cargo, "cargo"),# verifica se os dados estão vazio
            Manipular.validar_email(self.usuario_email, "email", secret_key),# verifica a avaliação externa do email
            Manipular.validar_min_caracter(self.usuario_nome, "nome"),# verifica se os dados estão aceitando menos que 3 caracteres
            Manipular.validar_letra(self.usuario_nome, "nome"),# verifica se os dados estão aceitando numeros
            Manipular.validar_not_caracter(self.usuario_nome, "nome") # verifica se os dados não estão aceitando caractere especial
        ]

        return [ erro for erro in erros if erro] # Retorna  os erros 


    # ====== Método para deletar os dados do usuario ===== #
    @classmethod
    def deletar_usuario(cls, id): 
        usuario = cls.buscar_por_id(id) # chama o método para de buscar por id do Crud_base

        if not usuario: # verifica se foi encontrado
            raise ValueError("Usuario não encontrado.") # retorna se tiver erro

        cls.deletar(id) # função deletar do Crud_base


    # ====== Método para atualizar os dados do usuario ===== #
    def atualizar_usuario(self, id):
        
        usuario = self.buscar_por_id(id) # busca o usuario por id, para ver se está no banco

        if not usuario: # verifica se foi encontrado
            raise ValueError("Usuario não encontrado.") # retorna se tiver erro

           
        self.atualizar(id) # chama o método de atualizar do Crud_base
        return "Usuario atualizado com sucesso!" # retorna se os dados foram atualizados

    # ===== Método para buscar usuario pelo id ===== #
    @classmethod
    def buscar_usuario_por_id(cls, id):
        usuario = cls.buscar_por_id(id) # chama o método para de buscar por id do Crud_base

        if not usuario: # verifica se foi encontrado
            raise ValueError("Usuario não encontrado.") # retorna se tiver erro


        return usuario # retorna os dados encontrado

    



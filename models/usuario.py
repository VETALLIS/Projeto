from core.crud_base import Crud_base #importação
from core.manipular import Manipular #importação
from core.conectar import Database #importação
import base64 #importação

class Usuario(Crud_base):
    tabela = "usuario" #nome da tabela
    pk = "usuario_id" #chave primaria da tabela

    fields = ["usuario_senha", "usuario_nome", "usuario_email", "usuario_cpf", "usuario_cargo", "usuario_imagem", "imagem_blob",  "imagem_tipo" ] #campos que temos na tela

    def __init__(self, usuario_senha, usuario_nome, usuario_email, usuario_cpf, usuario_cargo, usuario_confirmar_senha, usuario_imagem, imagem_tipo, imagem_blob): #definição de campos
        self.usuario_senha = usuario_senha
        self.usuario_nome = usuario_nome
        self.usuario_email = usuario_email
        self.usuario_cpf = usuario_cpf
        self.usuario_cargo = usuario_cargo
        self.usuario_confirmar_senha = usuario_confirmar_senha
        self.usuario_imagem = usuario_imagem
        self.imagem_tipo = imagem_tipo
        self.imagem_blob = imagem_blob

    def validar_usuario(self, secret_key): #executa as validações e retorna o erro
        erros = [
            Manipular.validar_vazio(self.usuario_senha, "senha"), #campo não pode ser vazio
            Manipular.validar_vazio(self.usuario_nome, "nome"), #campo não pode ser vazio
            Manipular.validar_vazio(self.usuario_email, "email"), #campo não pode ser vazio
            Manipular.validar_vazio(self.usuario_cpf, "cpf"), #campo não pode ser vazio
            Manipular.validar_vazio(self.usuario_cargo, "cargo"), #campo não pode ser vazio
            Manipular.validar_vazio(self.usuario_confirmar_senha, "confirmar_senha"), #campo não pode ser vazio
            Manipular.validar_cpf(self.usuario_cpf, "cpf", secret_key), #campo valida cpf, validação externa
            Manipular.validar_email(self.usuario_email, "email", secret_key), #campo valida email, validação externa
            Manipular.validar_caracter(self.usuario_senha, "senha"), #regras de senha, precisa ter caractere especial
            Manipular.comparar_criacao_senha(self.usuario_senha, self.usuario_confirmar_senha), #regras de senha, no confirmar senha
            Manipular.validar_not_caracter(self.usuario_nome, "nome"), #nome não pode aceitar caractere especial
            Manipular.validar_letra(self.usuario_nome, "nome"), #rnome não pode aceitar numero, apenas letra
            Manipular.validar_min_caracter(self.usuario_senha, "senha"), #regras de senha, caractere minimo
            Manipular.validar_numero(self.usuario_senha, "senha"), #regras de senha, senha precisa ter numero
            Manipular.validar_min_caracter(self.usuario_nome, "nome") #nome não pode aceitar menos que 3 caracteres
        ] #chamando as validações que serão usadas nessa tela, elas veem do manipular.py

        return [ erro for erro in erros if erro] #retorna o erro

    def gravar_usuario(self):  #def para criar o usuário e armazena-lo no banco
        usuario = self.gravar() 

        if not usuario:
            raise ValueError("Erro ao cadastrar usuário.")

        return "Usuário cadastrado com sucesso!" #mensagem de retorno

    @classmethod #def para excluir usuario no editar usuario
    def deletar_usuario(cls, id):
        usuario = cls.buscar_por_id(id) #confirma que o usuario existe

        if not usuario:
            raise ValueError("Usuario não encontrado.") #se não existe, aparece essa mensagem

        cls.deletar(id) #se encontrar o usuario, deleta

    def atualizar_usuario(self, id): #atualizando usuario no editar
        usuario = self.buscar_por_id(id) #confirma que o usuario existe

        if not usuario:
            raise ValueError("Usuario não encontrado.") #se não existe, aparece essa mensagem
           
        self.atualizar(id) #grava os novos dados no banco
        return "Usuario atualizado com sucesso!" #mensagem de retorno


    @classmethod #mostrando usuario na tela de funcionários cadastrados
    def buscar_usuario_por_id(cls, id):
        usuario  = cls.buscar_por_id(id) #confirma que o usuario existe

        if not usuario:
            raise ValueError("Usuario não encontrado.") #se não existe, aparece essa mensagem


        return usuario #retorna o usuario

    def buscar_email_existe(self): #se já tem um email cadastrado, não se pode cadastrar um outro funcionario
        usuario = self.buscar_email(self.usuario_email) #busca o email

        if usuario:
            raise ValueError("Esse email já foi cadastrado") #se o email ja estiver sendo usado, aparece essa mensagem
        return None #retorno
    
    @classmethod 
    def buscar_usuario(cls):
        usuarios = cls.buscar_tudo(cls.pk) #busca usuario, ordenado pela chave primaria

        if not usuarios:
            raise ValueError("Usuario não encontrato")

        for usuario in usuarios: #coloca a imagem nos usuarios
            if usuario.get("imagem_blob"):
                usuario["imagem_base64"] = base64.b64encode(usuario["imagem_blob"]).decode("utf-8")
            else:
                usuario["imagem_base64"] = None #fot não encontrada

        return usuarios #retorna os usuarios
    

    @classmethod #procurando os campos, e atribuindo 
    def inserir_usuario_adm(cls, dados):
        usuario = cls(
            usuario_senha=dados.get("usuario_senha"),
            usuario_nome=dados.get("usuario_nome"),
            usuario_email=dados.get("usuario_email"),
            usuario_confirmar_senha=dados.get("usuario_confirmar_senha"),
            usuario_imagem=dados.get("usuario_imagem"),
            imagem_tipo=dados.get("imagem_tipo"),
            imagem_blob=dados.get("imagem_blob"),
            usuario_cpf=dados.get("usuario_cpf"),
            usuario_cargo=dados.get("usuario_cargo"),
        )

        inserir = cls.gravar(usuario) #grava o usuario no campo



        if not inserir:
            print("Usuario não cadastrado")
            raise ValueError("Usuario não cadastrado")
            

        return inserir #retorno
    
    @classmethod #analisa os dados cadastrados, com o banco
    def has_related_records(cls, id):
        conexao = Database.connect() #conectando com o banco
        cursor = conexao.cursor()
        try:
            queries = [
                "SELECT COUNT(*) FROM produto WHERE usuario_usuario_id = %s",
            ]
            total = 0
            for sql in queries:
                cursor.execute(sql, (id,))
                total += cursor.fetchone()[0] #verifica se tem relação com outras tabelas, não pode ter
            return total > 0
        finally:
            cursor.close()
            conexao.close()

    
    @classmethod #buscando usuario por id
    def safe_delete(cls, id): #delete seguro
        usuario = cls.buscar_por_id(id)
        if not usuario:
            raise ValueError("Usuario não encontrado.") #usuario nao encontrado
        if cls.has_related_records(id):
            raise ValueError("Não é possível excluir o usuario porque ele possui pedidos ou movimentações vinculadas.") #só pode excluir o usuário se ele não estiver vinculado com outros campos
        cls.deletar(id) #se encontrar deleta
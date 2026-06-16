from core.crud_base import Crud_base
from core.manipular import Manipular
from core.conectar import Database

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

    def validar_usuario(self, secret_key):
        erros = [
            Manipular.validar_vazio(self.usuario_senha, "senha"),
            Manipular.validar_vazio(self.usuario_nome, "nome"),
            Manipular.validar_vazio(self.usuario_email, "email"),
            Manipular.validar_vazio(self.usuario_cpf, "cpf"),
            Manipular.validar_vazio(self.usuario_cargo, "cargo"),
            Manipular.validar_vazio(self.usuario_confirmar_senha, "confirmar_senha"),
            Manipular.validar_cpf(self.usuario_cpf, "cpf", secret_key),
            Manipular.validar_email(self.usuario_email, "email", secret_key),
            Manipular.validar_caracter(self.usuario_senha, "senha"),
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


        return usuario

    def buscar_email_existe(self):
        usuario = self.buscar_email(self.usuario_email)

        if usuario:
            raise ValueError("Esse email já foi cadastrado")

        return None
    
    @classmethod
    def buscar_usuario(cls):
        usuario = cls.buscar_tudo()

        if not usuario:
            raise ValueError("Usuario não encontrato")
        
        return usuario

    @classmethod
    def inserir_usuario_adm(cls, dados):
        usuario = cls(
                usuario_senha=dados.get("usuario_senha"),
                usuario_nome=dados.get("usuario_nome"),
                usuario_email=dados.get("usuario_email"),
                usuario_cpf=dados.get("usuario_cpf", "00000000000"), 
                usuario_cargo=dados.get("usuario_cargo", "admin"),   
                usuario_confirmar_senha=dados.get("usuario_confirmar_senha")
            )

        inserir = cls.gravar(usuario)



        if not inserir:
            print("Usuario não cadastrado")
            raise ValueError("Usuario não cadastrado")
            

        return inserir
    
    @classmethod
    def has_related_records(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            queries = [
                "SELECT COUNT(*) FROM produto WHERE usuario_usuario_id = %s",
            ]
            total = 0
            for sql in queries:
                cursor.execute(sql, (id,))
                total += cursor.fetchone()[0]
            return total > 0
        finally:
            cursor.close()
            conexao.close()

    
    @classmethod
    def safe_delete(cls, id):
        usuario = cls.buscar_por_id(id)
        if not usuario:
            raise ValueError("Usuario não encontrado.")
        if cls.has_related_records(id):
            raise ValueError("Não é possível excluir o usuario porque ele possui pedidos ou movimentações vinculadas.")
        cls.deletar(id)
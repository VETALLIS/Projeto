# Importa a classes
from core.crud_base import Crud_base
from core.manipular import Manipular
from core.conectar import Database

# Cria a classe Produto
class Produto(Crud_base):
    # define a tabela, os campos e a PK, para o banco
    tabela = "produto"
    pk = "produto_id"
    fields = ["produto_nome", "produto_descricao", "produto_categoria", "usuario_usuario_id"]

    # define os atributos
    def __init__(self, produto_nome, produto_descricao, produto_categoria, usuario_usuario_id):
        self.produto_nome = produto_nome
        self.produto_descricao = produto_descricao
        self.produto_categoria = produto_categoria
        self.usuario_usuario_id = usuario_usuario_id

    # valida os dados 
    def validar(self):
        erros = [
            Manipular.validar_vazio(self.produto_nome, "nome"), # valida se o campos esta vazio
            Manipular.validar_caracter(self.produto_nome, "nome"), # valida se tem caracteres especiais no nome
            Manipular.validar_vazio(self.produto_categoria, "categoria") # valida se o campos esta vazio
        ]

        return [ erro for erro in erros if erro] # retorna erro, se houver erros
    
    # Método de gravar produto
    def gravar_produto(self):
        produto = self.gravar() # chama o método do Crud_base

        if not produto: # verifica se foi gravado
            raise ValueError("Erro ao cadastrar produto.") # retorna se teve erro
        
        return "Cadastrado" # retorno sucesso
    
    # Método de verificação de relação de dados com otra tabela
    @classmethod
    def relacao_entre_tabelas(cls, id):
        
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            queries = [
                "SELECT COUNT(*) FROM movimentacao WHERE produto_id = %s", # verifica relação na tabela movimentação
            ]
            total = 0
            for sql in queries:
                cursor.execute(sql, (id,))
                total += cursor.fetchone()[0] 
            return total > 0
        finally:
            cursor.close()
            conexao.close()
        return False

    # Método de deletar dados de produto
    @classmethod
    def deletar_produto(cls, id):
        produto = cls.buscar_por_id(id) # chama o método de buscar por id do Crud_base

        if not produto: # verifica se foi encontrado
            raise ValueError("Produto não encontrado.") # retorna se não foi encontrado
        if cls.relacao_entre_tabelas(id): # verifica se tem relação com outra tabela
            raise ValueError("Não é possível excluir o produto porque ele possui pedidos ou movimentações vinculadas.") # retorna se tiver relações
        
        cls.deletar(id) # chama o método para deletar produto do Crud_base

        return "Produto deletado com sucesso!" # retorna sucesso
    
    # Método atualizar dados de produto
    def atualizar_produto(self, id):
        produto = self.buscar_por_id(id) # chama o método do Crud_base, para o produto

        if not produto: # verifica se foi encontrado
            raise ValueError("Produto não encontrado!") # retorna se não foi encontrado
        if self.relacao_entre_tabelas(id): # verifica se tem relação com outras tabelas
            raise ValueError("Não é possível atualizar o produto porque ele possui pedidos ou movimentações vinculadas.") # retorna se tiver relação com outras tabelas
        
        self.atualizar(id) # chama o método atualizar do Crud_base, para atualizar os dados

        return "Produto atualizado com sucesso!" # retorna sucesso

    # Método para buscar produto port id
    @classmethod
    def buscar_produto_id(cls, id):
        produto = cls.buscar_por_id(id) # chama o método do Crud_base para buscar

        if not produto: # verifica se foi encontrado
            raise ValueError("Produto não encontrado") # retorna se não foi encontrado

        return Produto(**produto) # retorna os dados encontrados

    # Método para buscar todos os produtso
    @classmethod
    def buscar_todo_produto(cls, order_by="produto_nome"):
        produto = cls.buscar_tudo(order_by) # chama o método do Crud_base para buscar os produtos

        if not produto: # verifica se foi encontrado
            raise ValueError("Produtos não encontrado") # retorna erro, se não foi encontrado

        return f"Produtos encontrados " # retorna sucesso
        

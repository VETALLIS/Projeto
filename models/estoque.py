# ===== Importar as classes =====#
from core.crud_base import Crud_base
from core.conectar import Database

# ===== Cria a classe GerenciamentoPerfil ===#
class Estoque(Crud_base):
    tabela = "estoque"
    pk = "estoque_id"
    # Define a tabela e os campos do banco 
    fields = ["produto_produto_id", "estoque_quantidade", "estoque_observacao", "produto_usuario_usuario_id"]


    #Essa def esta definindo os campos
    def __init__(self, produto_produto_id, estoque_observacao, produto_usuario_usuario_id, estoque_quantidade=0):
        self.produto_produto_id = produto_produto_id
        self.estoque_quantidade = estoque_quantidade
        self.estoque_observacao = estoque_observacao
        self.produto_usuario_usuario_id = produto_usuario_usuario_id

    def gravar_estoque(self):
        gravar = self.gravar()# chama o método de gravar do Crud_base

        if not gravar:# verifica se a gravação deu certo
            raise ValueError("Erro ao cadastrar estoque.")# retorna se tiver erro

        return gravar # retorna

    
    @staticmethod
    def buscar_estoque_por_produto(produto_id): 
        conexao = Database.connect() # abre a conexão com o banco
        cursor = conexao.cursor(dictionary=True) # cria o cursor retornando dicionário
        try:
            cursor.execute("SELECT estoque_id FROM estoque WHERE produto_produto_id = %s LIMIT 1", (produto_id,)) # busca o estoque do produto
            resultado = cursor.fetchone()# pega apenas um resultado
            if not resultado: # verifica se foi encontrado
                raise ValueError("Estoque não encontrado para esse produto.")# retorna se tiver erro
            return resultado["estoque_id"] # retorna o id do estoque
        finally:
            cursor.close()
            conexao.close()

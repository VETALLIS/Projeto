# ===== Importar as classes =====#
from core.crud_base import Crud_base
from core.manipular import Manipular 
from core.conectar import Database

# ===== Cria a classe GerenciamentoPerfil ===#
class Fornecedor(Crud_base):
    tabela = "fornecedor"
    pk = "fornecedor_id"

    # Define a tabela e os campos do banco  
    fields = ["fornecedor_nome", "fornecedor_cnpj", "fornecedor_endereco", "fornecedor_pedido_minimo", "fornecedor_tipo_produtos"]

    #Essa def esta definindo os campos
    def __init__(self, nome, cnpj, endereco, pedido_minimo, tipo_produtos):
        self.fornecedor_nome = nome
        self.fornecedor_cnpj = cnpj
        self.fornecedor_endereco = endereco
        self.fornecedor_pedido_minimo = pedido_minimo
        self.fornecedor_tipo_produtos = tipo_produtos

    def validar_fornecedor(self, secret_key):
        erros = [
            Manipular.validar_vazio(self.fornecedor_nome, "nome"),# verifica se os dados estão vazio
            Manipular.validar_vazio(self.fornecedor_cnpj, "cnpj"),# verifica se os dados estão vazio
            Manipular.validar_cnpj(self.fornecedor_cnpj, "cnpj", secret_key),# verifica se o cnpj é valido
            Manipular.validar_vazio(self.fornecedor_endereco, "endereco"),# verifica se os dados estão vazio
            Manipular.validar_vazio(self.fornecedor_pedido_minimo, "pedido_minimo"),# verifica se os dados estão vazio
            Manipular.validar_not_caracter(self.fornecedor_nome, "nome"),# verifica se os dados estão aceitando caractere especial
            Manipular.validar_min_caracter(self.fornecedor_nome, "nome"),# verifica se os dados estão aceitando menos que 3 caracteres
            Manipular.validar_letra(self.fornecedor_nome, "nome"),# verifica se os dados estão aceitando numeros
            Manipular.validar_not_caracter(self.fornecedor_tipo_produtos, "produtos"),# verifica se os dados estão aceitando caractere especial
            Manipular.validar_letra(self.fornecedor_tipo_produtos, "produtos"),# verifica se os dados estão aceitando numeros
            
        ]          
    
        return [ erro for erro in erros if erro] # Retorna  os erros 


    # ====== Método de gravação dos dados do fornecedor ==== #
    def gravar_fornecedor(self):
        fornecedor = self.gravar() # chama o método gravar da Classe Crude_base

        if not fornecedor: # Verifica se a gravação no banco deu certo
            raise ValueError("Erro ao criar fornecedor!") # Retorna o erro

        return "Fornecedor criado com sucesso" # Retorna mensagem de sucesso

    

    # ====== Método para deletar os dados do fornecedor ===== #
    @classmethod
    def deletar_fornecedor(cls, id):
        fornecedor = cls.buscar_por_id(id) # chama o método para de buscar por id do Crud_base
        if not fornecedor: # verifica se foi encontrado
            raise ValueError("Fornecedor não encontrado") # retorna se tiver erro
        
        #===== começa a conexao do banco ====#
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            query_deletar_itens = """
                DELETE ipe FROM item_pedido_entrada ipe
                INNER JOIN pedido_entrada pe 
                    ON ipe.pedido_entrada_pedido_entrada_id = pe.pedido_entrada_id
                WHERE pe.fornecedor_fornecedor_id = %s
            """
            cursor.execute(query_deletar_itens, (id,))
            
            query_deletar_saidas = """
                DELETE FROM pedido_entrada
                WHERE fornecedor_fornecedor_id IN (
                    SELECT fornecedor_id FROM fornecedor WHERE fornecedor_fornecedor_id = %s
                )
            """
            cursor.execute(query_deletar_saidas, (id,))

            query_deletar_pai = "DELETE FROM fornecedor WHERE fornecedor_id = %s"
            cursor.execute(query_deletar_pai, (id,))
            
            # Confirma as exclusões na base de dados
            conexao.commit()
            
        except Exception as e:
            # Se der qualquer erro, desfaz tudo
            conexao.rollback()
            raise e # repassa o erro
            
        finally:
            cursor.close() # fecha o cursor
            conexao.close() # fecha a conexão
        
        cls.deletar(id) #deleta no Crud_base o produto em si
        return "fornecedor deletado com sucesso" #Returna que foi deletado

    
    # ====== Método para atualizar os dados dos fornecedores ===== #
    def atualizar_fornecedor(self, id):
        fornecedor = self.buscar_por_id(id) # busca o fornecedor por id, para ver se está no banco

        if not fornecedor: # verifica se foi encontrado
            raise ValueError("Fornecedor não encontrado")  # Retorna o erro

        self.atualizar(id) # chama o método de atualizar do Crud_base
        return "Fornecedor updated com sucesso!" # retorna se os dados foram atualizados


     # ===== Método para buscar fornecedor pelo id ===== #
    def buscar_fornecedor_id(self):
        fornecedor  = self.buscar_por_id(id) # chama o método para de buscar por id do Crud_base

        if not fornecedor: # verifica se foi encontrado
            raise ValueError("Fornecedor não encontrado!") # retorna se tiver erro

        return Fornecedor(**fornecedor) 
    

    @classmethod
    def buscar_fornecedor(cls, order_by="fornecedor_nome"):
        fornecedor  = cls.buscar_tudo(order_by) # chama o método para de buscar por id do Crud_base

        if not fornecedor: # verifica se foi encontrado
            raise ValueError("Fornecedor não encontrado!") # retorna se tiver erro

        return fornecedor # retorna os dados encontrado
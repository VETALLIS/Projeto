# ======= Importação da classe de conexão com o banco ========== #
from core.conectar import Database

# ======= Criação da classe crud_base ====== #
class Crud_base:
    # Definição de tabelas, campos e PK, para a alteração de dados no banco
    tabela = ""
    fields = []
    pk = "id"


    # ===== Método para buscar os dados do banco ======= #
    @classmethod
    def buscar_tudo(cls, order_by="id"):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = f"SELECT * FROM {cls.tabela} ORDER BY {order_by}" # Busca os dados ordenando por ID
            cursor.execute(sql)
            return cursor.fetchall() # Retorna todos os dados encontrados
        finally:
            cursor.close()
            conexao.close()

    # ====== Método de gravação de dados no banco ===== #
    def gravar(self):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            colunas = ", ".join(self.fields) # Pega a lista de campos do fields, definido acima e os separa por virgula 
            marcadores = ", ".join(["%s"] * len(self.fields)) # Cria uma string com o número correto de marcadores de posição %s, separados por vírgula.
            valores = tuple(getattr(self, campo) for campo in self.fields) # Cria uma tupla contendo os valores reais dos atributos do objeto correspondentes aos campos listados em self.fields

            sql = f"INSERT INTO {self.tabela} ({colunas}) VALUES ({marcadores})" # Grava no banco com a tabela, os campos e os dados definidos nas variaveis acima

            cursor.execute(sql, valores)
            conexao.commit()
            return cursor.lastrowid # Retorna a ultima linha por ID gravada
        except Exception:
            conexao.rollback()
            raise
        finally:
            cursor.close()
            conexao.close()

    # ====== Método de atualização de dados ===== #
    def atualizar(self, id):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            campos = ", ".join([f"{campo} = %s" for campo in self.fields])# Pega os dados da lista filds e os separam por virgula
            valores = tuple(getattr(self, campo) for campo in self.fields) + (id,)# Pega os valores para atualizar

            sql = f"UPDATE {self.tabela} SET {campos} WHERE {self.pk} = %s" # Atualiza os dados procurando quais dados seram atualizados

            cursor.execute(sql, valores)
            conexao.commit()
            return cursor.rowcount # Retorna a quantidade de linhas atualizadas
        except Exception:
            conexao.rollback()
            raise
        finally:
            cursor.close()
            conexao.close()

    # ===== Método de deletar dados ===== #
    @classmethod
    def deletar(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = f"DELETE FROM {cls.tabela} WHERE {cls.pk} = %s" # Deletar os dados pela chave primaria
            cursor.execute(sql, (id,))
            conexao.commit()
            return cursor.rowcount
        except Exception:
            conexao.rollback()
            raise
        finally:
            cursor.close()
            conexao.close()

    # ====== Buscar dados por id ====== #
    @classmethod
    def buscar_por_id(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = f"SELECT * FROM {cls.tabela} WHERE {cls.pk} = %s" # Seleciona pela chave primaria
            cursor.execute(sql, (id,))
            return cursor.fetchone() # Retorna o primeiro resultado
        finally:
            cursor.close()
            conexao.close()

    # ====== Buscar email para login ===== #
    @classmethod
    def buscar_para_login(cls, email):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = "SELECT * FROM usuario WHERE usuario_email = %s " # Seleciona no banco pelo email
            cursor.execute(sql, (email,))
            resultados = cursor.fetchall() # Pega todos os dados
            return resultados[0] if resultados else None
        finally:
            cursor.close()
            conexao.close()
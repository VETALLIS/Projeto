import mysql.connector # Importo a biblioteca que faz a ponte entre o Python e o MySQL
from mysql.connector import Error # Importo a classe Error, que é o tipo de erro que o MySQL costuma lançar
# assim eu consigo capturar só os erros do banco, e não qualquer erro
from config import DB_CONFIG # Importo o DB_CONFIG do arquivo config.py
# lá ficam guardados host, usuário, senha e nome do banco

class Database: # Essa classe só serve pra criar a conexão com o banco
# todas as outras classes (como a Crud_base) usam ela pra conectar
    @staticmethod     # @staticmethod = método que não precisa de self nem de cls
    # dá pra chamar direto: Database.connect(), sem criar objeto
    def connect():
        try:    # try/except pra tratar o erro caso a conexão falhe
            return mysql.connector.connect(**DB_CONFIG)  # o ** "abre" o dicionário DB_CONFIG e passa cada item como argumento
        except Error as e:  # se der erro, eu levanto uma Exception com uma mensagem em português
            # e mostro o erro original (e) pra conseguir descobrir o que aconteceu
            raise Exception(f"Falha na conexão com o banco de dados: {e}")

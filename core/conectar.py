# ======== Importar biblioteca para a conexão com banco ======= #
import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

# ======== Classe para conexão com o banco ====== #  
class Database:
    @staticmethod
    def connect():
        try:
            return mysql.connector.connect(**DB_CONFIG)
        except Error as e:
            raise Exception(f"Falha na conexão com o banco de dados: {e}")

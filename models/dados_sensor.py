# ===== Importar as classes =====#
from core.crud_base import Crud_base
from core.conectar import Database


# ===== Cria a classe das leituras dos sensores (tabela dados_sensor) ===#
class Dados_sensor(Crud_base):
    tabela = "dados_sensor"
    pk = "dados_sensor_id"

    # ===== Método para buscar o id da última leitura do sensor RFID ===== #
    @classmethod
    def ultimo_id_rfid(cls):
        conexao = Database.connect() # abre a conexão com o banco
        cursor = conexao.cursor()
        try:
            # filtra pelo sensor MFRC522 para não varrer as leituras de temperatura e luz
            sql = """
                SELECT MAX(d.dados_sensor_id)
                FROM dados_sensor d
                INNER JOIN sensor s ON s.sensor_id = d.sensor_sensor_id
                WHERE s.sensor_modelo = 'MFRC522'
                  AND d.dados_sensor_rfid_uid IS NOT NULL
            """
            cursor.execute(sql)
            resultado = cursor.fetchone()
            if resultado and resultado[0]: # se existe alguma leitura
                return int(resultado[0]) # retorna o id dela
            return 0 # nenhuma tag foi lida ainda
        finally:
            cursor.close() # fecha o cursor
            conexao.close() # fecha a conexão


    # ===== Método para buscar a leitura de RFID mais nova que um id ===== #
    @classmethod
    def buscar_rfid_depois_de(cls, ultimo_id):
        conexao = Database.connect() # abre a conexão com o banco
        cursor = conexao.cursor(dictionary=True) # retorna como dicionário
        try:
            sql = """
                SELECT d.dados_sensor_id, d.dados_sensor_rfid_uid
                FROM dados_sensor d
                INNER JOIN sensor s ON s.sensor_id = d.sensor_sensor_id
                WHERE s.sensor_modelo = 'MFRC522'
                  AND d.dados_sensor_rfid_uid IS NOT NULL
                  AND d.dados_sensor_id > %s
                ORDER BY d.dados_sensor_id DESC
                LIMIT 1
            """
            cursor.execute(sql, (ultimo_id,))
            return cursor.fetchone() # retorna a leitura ou None se não houver nenhuma nova
        finally:
            cursor.close() # fecha o cursor
            conexao.close() # fecha a conexão
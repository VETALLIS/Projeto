from mysql.connector import pooling

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "vetallis_db_2_3",
}

pool = pooling.MySQLConnectionPool(
    pool_name="pool_sensores",
    pool_size=5,
    **DB_CONFIG
)

def salvar_leitura( device_id, sensor, temperatura=None, umidade=None, distancia=None, rfid_uid=None ):

    conn = None
    cursor = None

    try:

        conn = pool.get_connection()

        cursor = conn.cursor()

        # O sensor fisico e encontrado na tabela sensor:
        #   device_id (JSON) = sensor_n_serie
        #   sensor    (JSON) = sensor_modelo
        # O valor que chega em "distancia" vai para dados_sensor_luminosidade.
        sql = """
            INSERT INTO dados_sensor
            (
                dados_sensor_temperatura,
                dados_sensor_umidade,
                dados_sensor_luminosidade,
                dados_sensor_rfid_uid,
                dados_sensor_data_time,
                sensor_sensor_id
            )
            SELECT %s, %s, %s, %s, NOW(), sensor_id
            FROM sensor
            WHERE sensor_n_serie = %s
              AND sensor_modelo = %s
            LIMIT 1
        """

        valores = ( temperatura, umidade, distancia, rfid_uid, device_id, sensor )

        cursor.execute(
            sql,
            valores
        )

        conn.commit()

        if cursor.rowcount == 0:

            print(
                f"Sensor nao cadastrado: "
                f"{device_id} | {sensor}"
            )

            return False

        print(
            f"Leitura salva: "
            f"{device_id} | {sensor}"
        )

        return True
    except Exception as erro:

        print(
            "Erro ao salvar leitura:"
        )

        print(erro)

        return False
    finally:

        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()

def listar_leituras( device_id=None, sensor=None, limite=100 ):

        conn = None
        cursor = None

        try:

            # ---------------------------------------------
            # Protecao simples para o LIMIT
            # ---------------------------------------------

            limite = int(limite)

            if limite < 1:
                limite = 1

            if limite > 1000:
                limite = 1000


            conn = pool.get_connection()

            cursor = conn.cursor(
                dictionary=True
            )


            # ---------------------------------------------
            # MONTA A CONSULTA
            # ---------------------------------------------

            sql = """
                SELECT
                    d.dados_sensor_id AS id,
                    s.sensor_n_serie AS device_id,
                    s.sensor_modelo AS sensor,
                    d.dados_sensor_temperatura AS temperatura,
                    d.dados_sensor_umidade AS umidade,
                    d.dados_sensor_luminosidade AS luminosidade,
                    d.dados_sensor_rfid_uid AS rfid_uid,
                    d.dados_sensor_data_time AS timestamp

                FROM dados_sensor d

                INNER JOIN sensor s
                    ON s.sensor_id = d.sensor_sensor_id
            """

            filtros = []

            valores = []


            # ---------------------------------------------
            # FILTRO DEVICE
            # ---------------------------------------------

            if device_id:

                filtros.append(
                    "s.sensor_n_serie = %s"
                )

                valores.append(
                    device_id
                )


            # ---------------------------------------------
            # FILTRO SENSOR
            # ---------------------------------------------

            if sensor:

                filtros.append(
                    "s.sensor_modelo = %s"
                )

                valores.append(
                    sensor
                )


            # ---------------------------------------------
            # WHERE
            # ---------------------------------------------

            if filtros:

                sql += " WHERE "

                sql += " AND ".join(
                    filtros
                )


            # ---------------------------------------------
            # ORDENACAO E LIMITE
            # ---------------------------------------------

            sql += """
                ORDER BY d.dados_sensor_data_time DESC, d.dados_sensor_id DESC
                LIMIT %s
            """

            valores.append(
                limite
            )


            cursor.execute(
                sql,
                tuple(valores)
            )

            resultado = cursor.fetchall()

            return resultado


        except Exception as erro:

            print(
                "Erro ao listar leituras:"
            )

            print(erro)

            return []


        finally:

            if cursor is not None:
                cursor.close()

            if conn is not None:
                conn.close()


if __name__ == "__main__":

    print()
    print("================================")
    print("   TESTE DATABASE - SENAI")
    print("================================")

    print()
    print("Testando conexao com MySQL...")


    # =================================================
    # TESTE DHT11
    # =================================================

    print()
    print("Inserindo teste DHT11...")

    salvar_leitura(
        device_id="esp32-teste",
        sensor="DHT11",
        temperatura=25,
        umidade=60
    )


    # =================================================
    # TESTE HC-SR04
    # =================================================

    print()
    print("Inserindo teste HC-SR04...")

    salvar_leitura(
        device_id="esp32-teste",
        sensor="HC-SR04",
        distancia=38.50
    )


    # =================================================
    # TESTE MFRC522
    # =================================================

    print()
    print("Inserindo teste MFRC522...")

    salvar_leitura(
        device_id="esp32-teste",
        sensor="MFRC522",
        rfid_uid="TESTE-01-02-03"
    )


    # =================================================
    # CONSULTAR
    # =================================================

    print()
    print("================================")
    print("LEITURAS GRAVADAS")
    print("================================")

    leituras = listar_leituras(
        device_id="esp32-teste",
        limite=10
    )


    for leitura in leituras:

        print()
        print(leitura)


    print()
    print("================================")
    print("TESTE FINALIZADO")
    print("================================")
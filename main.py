"""
main.py
Projeto IoT SENAI - ESP32 MULTISSENSOR


Sensores:
DHT11
LDR (modulo)
MFRC522
Arquitetura:
ESP32
  -> HiveMQ Cloud (MQTT)
  -> FastAPI
  -> MySQL
"""


import network
import time
import ujson
import dht


from machine import Pin, SPI, ADC
from umqtt.simple import MQTTClient
from mfrc522 import MFRC522




# =====================================================
# 1. ESCOLHA DOS SENSORES
# =====================================================


USAR_DHT11 = True
USAR_LDR = True
USAR_RFID = True




# =====================================================
# 2. IDENTIFICACAO DO ESP32
# =====================================================


DEVICE_ID = "vetallis"




# =====================================================
# 3. WIFI
# =====================================================


WIFI_SSID = "SENAI-IOT"
WIFI_PASSWORD = "12345678"




# =====================================================
# 4. MQTT - HIVEMQ CLOUD
# =====================================================


MQTT_BROKER = "b1600c60a35c4520b32b9507d0b47b02.s1.eu.hivemq.cloud"
MQTT_PORT = 8883


MQTT_USER = "IOT-SENAI"
MQTT_PASSWORD = "12345678"


MQTT_CLIENT_ID = "esp32-sensores-01"


MQTT_TOPIC = b"sensores/leitura/vetallis"




# =====================================================
# 5. CONFIGURACAO DHT11
# =====================================================


if USAR_DHT11:
    sensor_dht = dht.DHT11(Pin(14))




# =====================================================
# 6. CONFIGURACAO LDR (MODULO)
# =====================================================
#
# | VCC | 3V3         |
# | GND | GND         |
# | AO  | GPIO 34     |
# | DO  | (nao usado) |
#
# Mais luz = valor bruto MENOR na maioria dos modulos.
# Se o seu funcionar ao contrario, LDR_INVERTIDO = False.


LDR_INVERTIDO = False

if USAR_LDR:
    ldr = ADC(Pin(34))
    ldr.atten(ADC.ATTN_11DB)




# =====================================================
# 7. CONFIGURACAO MFRC522
# =====================================================
#
# | SDA  | GPIO 5  |
# | SCK  | GPIO 18 |
# | MOSI | GPIO 23 |
# | MISO | GPIO 19 |
# | RST  | GPIO 22 |
# | 3.3V | 3V3     |
# | GND  | GND     |
#
# Ganho da antena (registrador 0x26):
# No teste, este modulo leu com 0x48, 0x58 e 0x68
# e NAO leu com 0x70/0x78. Usamos o valor do meio.
# Se ficar instavel, teste 0x48 ou 0x68.


RFID_GANHO = 0x68


# Quantas leituras seguidas sem cartao para considerar
# que o cartao foi retirado (evita repetir o UID).
RFID_MISSES_PARA_LIBERAR = 10


# Reinicia o modulo se ficar este tempo sem cartao
# (evita que o chip "trave" depois de um tempo ligado).
RFID_REINICIO_MS = 20000


rfid = None
ultimo_reinicio_rfid = 0




def configurar_rfid(mostrar=False):
    """Reset completo do MFRC522 + reaplica ganho e antena."""


    global rfid
    global ultimo_reinicio_rfid


    spi = SPI(
        2,
        baudrate=1000000,
        polarity=0,
        phase=0,
        sck=Pin(18),
        mosi=Pin(23),
        miso=Pin(19)
    )


    rfid = MFRC522(
        spi=spi,
        gpioRst=22,
        gpioCs=5
    )


    rfid._wreg(0x26, RFID_GANHO)


    # Garante que o driver da antena esta ligado
    rfid._wreg(0x14, rfid._rreg(0x14) | 0x03)


    ultimo_reinicio_rfid = time.ticks_ms()


    if mostrar:
        print("MFRC522 configurado. Versao:", hex(rfid._rreg(0x37)))




if USAR_RFID:


    print()
    print("Configurando MFRC522...")


    configurar_rfid(mostrar=True)




# =====================================================
# 8. CONTROLE DO RFID
# =====================================================


ultimo_uid = None
leituras_sem_cartao = 0




# =====================================================
# 9. CONECTAR AO WIFI
# =====================================================


def conectar_wifi():


    print()
    print("================================")
    print("CONECTANDO AO WIFI")
    print("================================")


    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)


    if not wifi.isconnected():


        print("Conectando ao Wi-Fi...")
        wifi.connect(WIFI_SSID, WIFI_PASSWORD)


        contador = 0


        while not wifi.isconnected():


            print(".", end="")
            time.sleep(1)
            contador += 1


            if contador >= 30:
                print()
                print("ERRO: Wi-Fi nao conectou.")
                return False


    print()
    print("Wi-Fi conectado com sucesso!")


    configuracao = wifi.ifconfig()


    print()
    print("IP:     ", configuracao[0])
    print("Mascara:", configuracao[1])
    print("Gateway:", configuracao[2])
    print("DNS:    ", configuracao[3])


    return True




# =====================================================
# 10. CONECTAR AO MQTT
# =====================================================


def conectar_mqtt():


    print()
    print("================================")
    print("CONECTANDO AO MQTT")
    print("================================")


    print("Broker:", MQTT_BROKER)
    print("Porta:", MQTT_PORT)
    print("Usuario:", MQTT_USER)
    print("Client ID:", MQTT_CLIENT_ID)
    print("TLS: ATIVADO | SNI: ATIVADO")
    print("Conectando...")


    try:


        cliente = MQTTClient(
            MQTT_CLIENT_ID,
            MQTT_BROKER,
            port=MQTT_PORT,
            user=MQTT_USER,
            password=MQTT_PASSWORD,
            ssl=True,
            ssl_params={"server_hostname": MQTT_BROKER}
        )


        cliente.connect()


        print()
        print("MQTT CONECTADO COM SUCESSO!")


        return cliente


    except Exception as erro:


        print()
        print("ERRO NA CONEXAO MQTT")
        print("Tipo:", type(erro))
        print("Erro:", erro)


        return None




# =====================================================
# 11. PUBLICAR MQTT (com reconexao automatica)
# =====================================================


def publicar(dados):


    global client


    mensagem = ujson.dumps(dados)


    print()
    print("Publicando MQTT...")
    print("Topico:", MQTT_TOPIC)
    print("Mensagem:", mensagem)


    for tentativa in range(2):


        try:


            client.publish(MQTT_TOPIC, mensagem)


            print("MQTT enviado com sucesso!")


            return True


        except Exception as erro:


            print("ERRO AO PUBLICAR MQTT:", erro)


            # Na primeira falha, tenta reconectar e reenviar
            if tentativa == 0:


                print("Tentando reconectar ao MQTT...")


                novo = conectar_mqtt()


                if novo is None:
                    return False


                client = novo


    return False




# =====================================================
# 12. INICIALIZACAO DO DHT11
# =====================================================


def inicializar_dht11():


    print()
    print("================================")
    print("INICIALIZANDO DHT11")
    print("================================")


    time.sleep(2)


    try:
        sensor_dht.measure()
    except OSError:
        pass


    time.sleep(2)


    try:


        sensor_dht.measure()


        print("DHT11 inicializado com sucesso!")
        print("Temperatura inicial:", sensor_dht.temperature(), "C")
        print("Umidade inicial:", sensor_dht.humidity(), "%")


        return True


    except OSError as erro:


        print("DHT11 ainda nao respondeu.")
        print("Erro:", erro)


        return False




# =====================================================
# 13. LEITURA DO DHT11
# =====================================================


def ler_dht11():


    try:


        sensor_dht.measure()


        temperatura = sensor_dht.temperature()
        umidade = sensor_dht.humidity()


        print()
        print("--------------------------------")
        print("DHT11")
        print("--------------------------------")
        print("Temperatura:", temperatura, "C")
        print("Umidade:", umidade, "%")


        publicar({
            "device_id": DEVICE_ID,
            "sensor": "DHT11",
            "temperatura": temperatura,
            "umidade": umidade
        })


    except OSError as erro:


        print()
        print("Aviso: leitura DHT11 nao realizada.")
        print("Erro:", erro)




# =====================================================
# 14. LEITURA DO LDR (MODULO)
# =====================================================


def ler_ldr():


    try:


        # Media de 10 leituras para reduzir ruido
        soma = 0


        for _ in range(10):
            soma += ldr.read()
            time.sleep_ms(5)


        bruto = soma // 10


        # Mais luz = percentual maior
        if LDR_INVERTIDO:
            luminosidade = ((4095 - bruto) * 100) / 4095
        else:
            luminosidade = (bruto * 100) / 4095


        luminosidade = round(luminosidade, 1)


        print()
        print("--------------------------------")
        print("LDR")
        print("--------------------------------")
        print("Valor bruto:", bruto)
        print("Luminosidade:", luminosidade, "%")


        publicar({
            "device_id": DEVICE_ID,
            "sensor": "LDR",
            "ldr_bruto": bruto,
            "luminosidade": luminosidade
        })


    except Exception as erro:


        print()
        print("Aviso: leitura LDR nao realizada.")
        print("Erro:", erro)




# =====================================================
# 15. CONVERTER UID RFID
# =====================================================


def converter_uid(uid):


    # Usa so os 4 primeiros bytes: o 5o e o BCC (checksum)
    return "-".join("{:02X}".format(b) for b in uid[:4])




# =====================================================
# 16. LEITURA RFID
# =====================================================


def detectar_cartao():
    """Tenta ate 3 vezes: a antena deste modulo e intermitente."""


    for _ in range(3):


        status, _tipo = rfid.request(rfid.REQIDL)


        if status == rfid.OK:
            return True


        time.sleep_ms(10)


    return False




def ler_rfid():


    global ultimo_uid
    global leituras_sem_cartao


    try:


        # ---------------------------------------------
        # NENHUM CARTAO
        # ---------------------------------------------


        if not detectar_cartao():


            if ultimo_uid is not None:


                leituras_sem_cartao += 1


                if leituras_sem_cartao >= RFID_MISSES_PARA_LIBERAR:


                    print()
                    print("Cartao retirado. RFID liberado.")


                    ultimo_uid = None
                    leituras_sem_cartao = 0


            # Sem cartao: reinicia o modulo de tempos em tempos
            if time.ticks_diff(time.ticks_ms(), ultimo_reinicio_rfid) >= RFID_REINICIO_MS:
                configurar_rfid()


            return


        # Cartao detectado
        leituras_sem_cartao = 0


        # ---------------------------------------------
        # LER UID
        # ---------------------------------------------


        # request + anticoll sempre em par, varias tentativas
        uid = None


        for _ in range(15):


            st, _tipo = rfid.request(rfid.REQIDL)


            if st == rfid.OK:


                st, dados_uid = rfid.anticoll()


                if st == rfid.OK:
                    uid = dados_uid
                    break


            time.sleep_ms(20)


        if uid is None:
            # Falhou agora, tenta de novo no proximo ciclo
            return


        uid_texto = converter_uid(uid)


        # Mesmo cartao ainda na antena
        if uid_texto == ultimo_uid:
            return


        # ---------------------------------------------
        # NOVO CARTAO
        # ---------------------------------------------


        print()
        print("--------------------------------")
        print("MFRC522")
        print("--------------------------------")
        print("Novo cartao detectado!")
        print("UID:", uid_texto)


        publicado = publicar({
            "device_id": DEVICE_ID,
            "sensor": "MFRC522",
            "rfid_uid": uid_texto
        })


        if publicado:


            ultimo_uid = uid_texto


            print("Cartao registrado.")
            print("Retire o cartao para permitir nova leitura.")


    except Exception as erro:


        print()
        print("Aviso: falha na leitura RFID.")
        print("Erro:", erro)


        try:
            configurar_rfid()
        except Exception as erro2:
            print("Falha ao reiniciar RFID:", erro2)




# =====================================================
# 17. INICIO DO SISTEMA
# =====================================================


print()
print("================================")
print("     SISTEMA IoT - SENAI")
print("================================")
print("ESP32 MULTISSENSOR")
print()
print("Sensores habilitados:")
print("DHT11:", USAR_DHT11)
print("LDR:", USAR_LDR)
print("MFRC522:", USAR_RFID)
print("================================")




# =====================================================
# 18. CONECTAR AO WIFI
# =====================================================


if not conectar_wifi():


    print()
    print("Sistema interrompido. Motivo: falha no Wi-Fi.")


    raise SystemExit




# =====================================================
# 19. CONECTAR AO MQTT
# =====================================================


client = conectar_mqtt()


if client is None:


    print()
    print("Sistema interrompido. Motivo: falha no MQTT.")


    raise SystemExit




# =====================================================
# 20. INICIALIZAR DHT11
# =====================================================


if USAR_DHT11:


    if not inicializar_dht11():


        print()
        print("DHT11 sera testado novamente durante o funcionamento.")




# =====================================================
# 21. SISTEMA PRONTO
# =====================================================


print()
print("================================")
print("SISTEMA INICIALIZADO")
print("================================")
print("Wi-Fi: OK")
print("MQTT: OK")
print("Iniciando monitoramento...")
print("================================")




# =====================================================
# 22. CONTROLE DE TEMPO
# =====================================================
#
# DHT11 e LDR: leitura a cada 5 segundos.
# RFID: verificado continuamente.


INTERVALO_SENSORES_MS = 5000


ultima_leitura_sensores = time.ticks_ms()




# =====================================================
# 23. LOOP PRINCIPAL
# =====================================================


while True:


    agora = time.ticks_ms()


    # DHT11 + LDR
    if time.ticks_diff(agora, ultima_leitura_sensores) >= INTERVALO_SENSORES_MS:


        print()
        print("================================")
        print("NOVA RODADA DE LEITURAS")
        print("================================")


        # Reconecta Wi-Fi/MQTT se a conexao caiu
        if not network.WLAN(network.STA_IF).isconnected():


            print("Wi-Fi caiu. Reconectando...")


            if conectar_wifi():


                novo_client = conectar_mqtt()


                if novo_client is not None:
                    client = novo_client


        if USAR_DHT11:
            ler_dht11()


        if USAR_LDR:
            ler_ldr()


        ultima_leitura_sensores = time.ticks_ms()


    # RFID
    if USAR_RFID:
        ler_rfid()


    time.sleep_ms(50) 
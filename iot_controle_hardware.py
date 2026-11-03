from machine import Pin, ADC, SPI
from time import sleep, sleep_ms, ticks_ms, ticks_diff
import dht


# =====================================================
#  DRIVER DO RFID RC522 (embutido)
# =====================================================
class MFRC522:
    OK = 0
    NOTAGERR = 1
    ERR = 2

    REQIDL = 0x26
    REQALL = 0x52

    def __init__(self, spi, rst, cs):
        self.spi = spi
        self.rst = Pin(rst, Pin.OUT)
        self.cs = Pin(cs, Pin.OUT)
        self.cs.value(1)

        # Reset por hardware
        self.rst.value(0)
        sleep_ms(50)
        self.rst.value(1)
        sleep_ms(50)

        self.init()

    # ---------- Acesso aos registradores ----------
    def _wreg(self, reg, val):
        self.cs.value(0)
        self.spi.write(bytes([(reg << 1) & 0x7E, val]))
        self.cs.value(1)

    def _rreg(self, reg):
        buf = bytearray(2)
        self.cs.value(0)
        self.spi.write_readinto(bytes([((reg << 1) & 0x7E) | 0x80, 0x00]), buf)
        self.cs.value(1)
        return buf[1]

    def _sflags(self, reg, mask):
        self._wreg(reg, self._rreg(reg) | mask)

    def _cflags(self, reg, mask):
        self._wreg(reg, self._rreg(reg) & (~mask & 0xFF))

    # ---------- Comunicação com o cartão ----------
    def _tocard(self, cmd, send):
        recv = []
        bits = 0
        irq_en = 0
        wait_irq = 0
        n = 0
        stat = self.ERR

        if cmd == 0x0E:      # autenticação
            irq_en = 0x12
            wait_irq = 0x10
        elif cmd == 0x0C:    # transmitir e receber
            irq_en = 0x77
            wait_irq = 0x30

        self._wreg(0x02, irq_en | 0x80)
        self._cflags(0x04, 0x80)
        self._sflags(0x0A, 0x80)
        self._wreg(0x01, 0x00)

        for c in send:
            self._wreg(0x09, c)
        self._wreg(0x01, cmd)

        if cmd == 0x0C:
            self._sflags(0x0D, 0x80)

        i = 2000
        while True:
            n = self._rreg(0x04)
            i -= 1
            if i == 0 or (n & 0x01) or (n & wait_irq):
                break

        self._cflags(0x0D, 0x80)

        if i:
            if (self._rreg(0x06) & 0x1B) == 0x00:
                stat = self.OK
                if n & irq_en & 0x01:
                    stat = self.NOTAGERR
                elif cmd == 0x0C:
                    n = self._rreg(0x0A)
                    lbits = self._rreg(0x0C) & 0x07
                    if lbits != 0:
                        bits = (n - 1) * 8 + lbits
                    else:
                        bits = n * 8
                    if n == 0:
                        n = 1
                    elif n > 16:
                        n = 16
                    for _ in range(n):
                        recv.append(self._rreg(0x09))
            else:
                stat = self.ERR

        return stat, recv, bits

    # ---------- Funções públicas ----------
    def init(self):
        self.reset()
        self._wreg(0x2A, 0x8D)
        self._wreg(0x2B, 0x3E)
        self._wreg(0x2D, 30)
        self._wreg(0x2C, 0)
        self._wreg(0x15, 0x40)
        self._wreg(0x11, 0x3D)
        self.antenna_on()

    def reset(self):
        self._wreg(0x01, 0x0F)
        sleep_ms(50)

    def antenna_on(self):
        self._sflags(0x14, 0x03)

    def versao(self):
        """Deve retornar 0x91 ou 0x92 se o módulo estiver comunicando."""
        return self._rreg(0x37)

    def request(self, mode):
        self._wreg(0x0D, 0x07)
        stat, recv, bits = self._tocard(0x0C, [mode])
        if stat != self.OK or bits != 0x10:
            stat = self.ERR
        return stat, bits

    def anticoll(self):
        ser_chk = 0
        self._wreg(0x0D, 0x00)
        stat, recv, bits = self._tocard(0x0C, [0x93, 0x20])
        if stat == self.OK:
            if len(recv) == 5:
                for i in range(4):
                    ser_chk ^= recv[i]
                if ser_chk != recv[4]:
                    stat = self.ERR
            else:
                stat = self.ERR
        return stat, recv


# =====================================================
#  CONFIGURAÇÃO
# =====================================================
PINO_DHT = 14          # se continuar dando timeout, teste 27 ou 26
PINO_LDR = 34          # ADC1 (32 a 39)

# RFID (RC522) - VSPI
PINO_RST = 2
PINO_CS = 5            # SDA no módulo

INTERVALO_SENSORES = 2000   # ms entre leituras de DHT11 e LDR

sensor = dht.DHT11(Pin(PINO_DHT))

ldr = ADC(Pin(PINO_LDR))
ldr.atten(ADC.ATTN_11DB)
ldr.width(ADC.WIDTH_12BIT)

R_FIXO = 10000         # resistor do divisor, em ohms (ajuste se trocar)
LUX_CONST = 500        # constante de calibração do lux (ajuste com um luxímetro)

# Faixa observada (se ajusta sozinha)
leitura_min = 4095
leitura_max = 0

# Para fixar a faixa depois de testar, ex.: FAIXA_MANUAL = (50, 900)
FAIXA_MANUAL = None

# SPI(2) = VSPI: SCK=18, MOSI=23, MISO=19
spi = SPI(2, baudrate=1000000, polarity=0, phase=0,
          sck=Pin(18), mosi=Pin(23), miso=Pin(19))
leitor = MFRC522(spi, rst=PINO_RST, cs=PINO_CS)

# Cartões autorizados (opcional): leia os UIDs e cole aqui
CARTOES_AUTORIZADOS = {
    # "A1B2C3D4": "Maria",
    # "11223344": "Chaveiro azul",
}

# Tempo para o DHT11 estabilizar depois de ligar
sleep(2)


# =====================================================
#  FUNÇÕES
# =====================================================
def ler_dht(tentativas=1):
    """Lê o DHT11. Com 1 tentativa, o RFID não fica travado se o sensor falhar."""
    for _ in range(tentativas):
        try:
            sensor.measure()
            return sensor.temperature(), sensor.humidity()
        except OSError:
            sleep_ms(300)
    return None, None


def ler_ldr(amostras=10):
    soma = 0
    for _ in range(amostras):
        soma += ldr.read()
        sleep(0.005)
    return soma // amostras


def calcular_porcentagem(valor):
    """Mais luz = maior porcentagem (LDR entre o pino e o GND)."""
    global leitura_min, leitura_max

    if FAIXA_MANUAL:
        minimo, maximo = FAIXA_MANUAL
    else:
        leitura_min = min(leitura_min, valor)
        leitura_max = max(leitura_max, valor)
        minimo, maximo = leitura_min, leitura_max

    if maximo - minimo < 20:
        return None

    pct = (valor - minimo) / (maximo - minimo) * 100
    pct = 100 - pct
    return max(0, min(100, pct))


def calcular_lux(valor):
    """Lux APROXIMADO. LDR entre o pino e o GND, resistor fixo no 3,3 V."""
    if valor <= 0 or valor >= 4095:
        return None
    v = valor / 4095 * 3.3
    r_ldr = R_FIXO * v / (3.3 - v)
    if r_ldr <= 0:
        return None
    return LUX_CONST / (r_ldr / 1000)


def mostrar_sensores():
    # --- DHT11 ---
    temperatura, umidade = ler_dht()
    if temperatura is None:
        print("DHT11: sem resposta (confira fios, pinos S/+/- e alimentação)")
    else:
        print(f"Umidade: {umidade}%")
        print(f"Temperatura: {temperatura}°C")

    # --- LDR ---
    ldr_valor = ler_ldr()
    luz_pct = calcular_porcentagem(ldr_valor)
    luz_lux = calcular_lux(ldr_valor)

    print(f"Luminosidade (bruto): {ldr_valor}")

    if luz_pct is None:
        print("Luminosidade: calibrando... varie a luz sobre o LDR")
    else:
        print(f"Luminosidade: {luz_pct:.0f}%")

    if luz_lux is None:
        print("Luminosidade: fora da faixa de medição (lux)")
    else:
        print(f"Luminosidade: ~{luz_lux:.0f} lux (aproximado)")

    print(f"Faixa vista: {leitura_min} a {leitura_max}")
    print("-" * 30)


def verificar_rfid():
    """Retorna o UID (string hex) se um cartão novo foi lido, senão None."""
    global ultimo_uid

    stat, _ = leitor.request(leitor.REQIDL)
    if stat != leitor.OK:
        ultimo_uid = None          # cartão saiu, libera nova leitura
        return None

    stat, uid = leitor.anticoll()
    if stat != leitor.OK:
        return None

    uid_hex = "".join("{:02X}".format(b) for b in uid[:4])
    if uid_hex == ultimo_uid:      # mesmo cartão ainda encostado
        return None

    ultimo_uid = uid_hex
    return uid_hex


# =====================================================
#  TESTE DO RFID
# =====================================================
versao = leitor.versao()
if versao in (0x91, 0x92):
    print(f"RC522 OK (versão 0x{versao:02X})")
else:
    print(f"RC522 não respondeu (leu 0x{versao:02X}). Confira fios e alimentação.")
print("Aproxime um cartão ou chaveiro quando quiser...")
print("=" * 30)


# =====================================================
#  LOOP PRINCIPAL
# =====================================================
ultimo_uid = None
ultima_leitura = ticks_ms() - INTERVALO_SENSORES   # lê os sensores já na 1ª volta

while True:
    # --- RFID: verificado o tempo todo ---
    uid_hex = verificar_rfid()
    if uid_hex:
        print("*" * 30)
        print(f"CARTÃO LIDO - UID: {uid_hex}")
        print(f"UID (decimal): {int(uid_hex, 16)}")
        if CARTOES_AUTORIZADOS:
            if uid_hex in CARTOES_AUTORIZADOS:
                print(f"Acesso liberado: {CARTOES_AUTORIZADOS[uid_hex]}")
            else:
                print("Acesso negado")
        print("*" * 30)

    # --- Sensores: a cada 2 segundos ---
    if ticks_diff(ticks_ms(), ultima_leitura) >= INTERVALO_SENSORES:
        ultima_leitura = ticks_ms()
        mostrar_sensores()

    sleep_ms(100)
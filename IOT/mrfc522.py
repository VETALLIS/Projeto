"""
Driver simplificado MFRC522 para MicroPython + ESP32
Comunicação SPI
"""


from machine import Pin
from os import uname




class MFRC522:


    OK = 0
    NOTAGERR = 1
    ERR = 2


    REQIDL = 0x26
    REQALL = 0x52


    AUTHENT1A = 0x60
    AUTHENT1B = 0x61




    def __init__(
        self,
        spi,
        gpioRst,
        gpioCs
    ):


        self.spi = spi


        self.rst = Pin(
            gpioRst,
            Pin.OUT
        )


        self.cs = Pin(
            gpioCs,
            Pin.OUT
        )


        self.cs.value(1)


        self.rst.value(0)


        self.rst.value(1)


        self._wreg(
            0x01,
            0x0F
        )


        self._wreg(
            0x2A,
            0x8D
        )


        self._wreg(
            0x2B,
            0x3E
        )


        self._wreg(
            0x2D,
            30
        )


        self._wreg(
            0x2C,
            0
        )


        self._wreg(
            0x15,
            0x40
        )


        self._wreg(
            0x11,
            0x3D
        )


        self._antenna_on()




    # =================================================
    # ESCREVER REGISTRADOR
    # =================================================


    def _wreg(
        self,
        reg,
        val
    ):


        self.cs.value(0)


        self.spi.write(
            bytes([
                (reg << 1) & 0x7E,
                val
            ])
        )


        self.cs.value(1)




    # =================================================
    # LER REGISTRADOR
    # =================================================


    def _rreg(
        self,
        reg
    ):


        self.cs.value(0)


        self.spi.write(
            bytes([
                ((reg << 1) & 0x7E) | 0x80
            ])
        )


        val = self.spi.read(
            1
        )


        self.cs.value(1)


        return val[0]




    # =================================================
    # SET BIT MASK
    # =================================================


    def _sflags(
        self,
        reg,
        mask
    ):


        self._wreg(
            reg,
            self._rreg(reg) | mask
        )




    # =================================================
    # CLEAR BIT MASK
    # =================================================


    def _cflags(
        self,
        reg,
        mask
    ):


        self._wreg(
            reg,
            self._rreg(reg) & (~mask)
        )




    # =================================================
    # ANTENA
    # =================================================


    def _antenna_on(self):


        if ~(self._rreg(0x14)) & 0x03:


            self._sflags(
                0x14,
                0x03
            )




    # =================================================
    # COMUNICAÇÃO COM CARTÃO
    # =================================================


    def _tocard(
        self,
        cmd,
        send
    ):


        recv = []


        bits = 0


        irq_en = 0


        wait_irq = 0




        if cmd == 0x0E:


            irq_en = 0x12


            wait_irq = 0x10




        if cmd == 0x0C:


            irq_en = 0x77


            wait_irq = 0x30




        self._wreg(
            0x02,
            irq_en | 0x80
        )


        self._cflags(
            0x04,
            0x80
        )


        self._sflags(
            0x0A,
            0x80
        )


        self._wreg(
            0x01,
            0x00
        )




        for c in send:


            self._wreg(
                0x09,
                c
            )




        self._wreg(
            0x01,
            cmd
        )




        if cmd == 0x0C:


            self._sflags(
                0x0D,
                0x80
            )




        i = 2000




        while True:


            n = self._rreg(
                0x04
            )


            i -= 1


            if not (
                i != 0
                and not (n & 0x01)
                and not (n & wait_irq)
            ):


                break




        self._cflags(
            0x0D,
            0x80
        )




        if i:


            if (
                self._rreg(0x06)
                & 0x1B
            ) == 0x00:


                stat = self.OK




                if n & irq_en & 0x01:


                    stat = self.NOTAGERR




                elif cmd == 0x0C:


                    n = self._rreg(
                        0x0A
                    )


                    last_bits = (
                        self._rreg(0x0C)
                        & 0x07
                    )




                    if last_bits:


                        bits = (
                            (n - 1) * 8
                            + last_bits
                        )


                    else:


                        bits = n * 8




                    if n == 0:


                        n = 1




                    elif n > 16:


                        n = 16




                    for _ in range(n):


                        recv.append(
                            self._rreg(0x09)
                        )




                return stat, recv, bits




        return self.ERR, recv, bits




    # =================================================
    # REQUEST
    # =================================================


    def request(
        self,
        mode
    ):


        self._wreg(
            0x0D,
            0x07
        )




        stat, recv, bits = self._tocard(


            0x0C,


            [mode]
        )




        if (
            stat != self.OK
            or bits != 0x10
        ):


            stat = self.ERR




        return stat, bits




    # =================================================
    # ANTICOLLISION
    # =================================================


    def anticoll(self):


        ser_chk = 0


        ser = [
            0x93,
            0x20
        ]




        self._wreg(
            0x0D,
            0x00
        )




        stat, recv, bits = self._tocard(


            0x0C,


            ser
        )




        if stat == self.OK:


            if len(recv) == 5:


                for i in range(4):


                    ser_chk ^= recv[i]




                if ser_chk != recv[4]:


                    stat = self.ERR




            else:


                stat = self.ERR




        return stat, recv
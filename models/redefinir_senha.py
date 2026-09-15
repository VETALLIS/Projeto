import random
import smtplib
from core.crud_base import Crud_base
from core.conectar import Database

class Redefinir(Crud_base):

    tabela = "recuperar"
    fields = ["recuperar_codigo"]
    pk = "recuperar_id"

    def gerar_codigo(self):
        numeros = []
        for i in range(5):
            numero = random.randint(1, 9)
            numeros.append(numero)

        return numeros

    def enviar_email(self, email, codigo):

        try:
            servidor_email = smtplib.SMTP('smtp.gmail.com', 587)
            servidor_email.starttls()
            servidor_email.login('vetalisge@gmail.com', 'fhzy sfsq dqoi xzjt')

            remetente = 'vetalisge@gmail.com'
            destinatario = email
            conteudo = f'Ola, este e um email de teste. {codigo}'

            servidor_email.sendmail(remetente, destinatario, conteudo)
            return True
        except Exception as e:
            print(f"Erro ao enviar email: {e}")
        finally:
            servidor_email.quit()

    def buscar_email_redefinir(self, email):
        buscar = self.buscar_email(email)

        if not buscar:
            return False

        return buscar

    def gravar_codigo(self, numeros):
        self.recuperar_codigo = "".join(str(n) for n in numeros)
        gravar = self.gravar()

        if not gravar:
            return "Erro ao gravar código de recuperação"

        return gravar

    
    @classmethod
    def buscar_codigo(cls, numero):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = f"SELECT * FROM {cls.tabela} where recuperar_codigo = %s"
            cursor.execute(sql, (numero,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conexao.close()

    def verificar_codigo(self, numeros):
        buscar = self.buscar_codigo(numeros)

        if not buscar:
            return False

        if not buscar["recuperar_codigo"] == numeros:
            return None

        return "Codigos validos"     
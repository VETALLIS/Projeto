import random
import smtplib
from core.crud_base import Crud_base

class Redefinir(Crud_base):

    def gerar_codigo(self):
        numeros = []
        for i in range(5):
            numero = random.randint(1, 9)
            numeros.append(numero)

        print(numeros)

    def enviar_email(self, email):
        codigo = self.gerar_codigo()
        try:
            servidor_email = smtplib.SMTP('smtp.gmail.com', 587)
            servidor_email.starttls()
            servidor_email.login('vetalisge@gmail.com', 'fhzy sfsq dqoi xzjt')

            remetente = 'vetalisge@gmail.com'
            destinatario = email
            conteudo = f'Olá, este é um email de teste. {codigo}'

            servidor_email.sendmail(remetente, destinatario, conteudo)
        except Exception as e:
            print(f"Erro ao enviar email: {e}")
        finally:
            servidor_email.quit()

    def buscar_email_redefinir(self, email):
        buscar = self.buscar_email(email)

        if not buscar:
            return False

        return None
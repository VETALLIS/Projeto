import smtplib
from email.message import EmailMessage
from core.crud_base import Crud_base

class Contato(Crud_base):

    def __init__(self, contato_nome, contato_email, contato_mensagem):
        self.contato_nome = contato_nome
        self.contato_email = contato_email
        self.contato_mensagem = contato_mensagem

    @classmethod
    def enviar_email(cls, dados):
        
        # Criar a mensagem

        corpo = (f" Nome: {dados['contato_nome']} \n Contato: {dados['contato_email']} \n Mensagem: {dados['contato_mensagem']}")
        msg = EmailMessage()
        msg.set_content(corpo)
        msg["Subject"] = "Contato do formulario"
        msg["From"] = "vetalisge@gmail.com"
        msg["To"] = "vitoria.h.silva9@aluno.senai.br"

        # Enviar via servidor SMTP (exemplo do Gmail)
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        senha_app = "sxoh ahjn ghxz bxxm"

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as servidor:
                servidor.starttls()  # Segurança TLS
                servidor.login(msg["From"], senha_app)
                servidor.send_message(msg)
            print("E-mail enviado com sucesso!")
        except Exception as e:
            print(f"Erro ao enviar: {e}")

            return produto


import smtplib
from email.message import EmailMessage
from core.crud_base import Crud_base
from core.manipular import Manipular 

class Contato(Crud_base):

    def __init__(self, contato_nome, contato_email, contato_mensagem):
        self.contato_nome = contato_nome
        self.contato_email = contato_email
        self.contato_mensagem = contato_mensagem

    def validar_contato(self, secret_key):
        erros = [
            Manipular.validar_vazio(self.contato_nome, "nome"),# verifica se os dados estão vazio
            Manipular.validar_vazio(self.contato_email, "email"),# verifica se os dados estão vazio
            Manipular.validar_email(self.contato_email, "email", secret_key),# verifica se o cnpj é valido
            Manipular.validar_vazio(self.contato_mensagem, "mensagem"),# verifica se os dados estão vazio
            Manipular.validar_not_caracter(self.contato_nome, "nome"),# verifica se os dados estão aceitando caractere especial
            Manipular.validar_min_caracter(self.contato_nome, "nome"),# verifica se os dados estão aceitando menos que 3 caracteres
            Manipular.validar_letra(self.contato_nome, "nome"),# verifica se os dados estão aceitando numeros
            
        ]          
    
        return [ erro for erro in erros if erro]

    @classmethod
    def enviar_email(cls, dados):
        
        # Criar a mensagem

        corpo = (f" Nome: {dados['contato_nome']} \n Contato: {dados['contato_email']} \n Mensagem: {dados['contato_mensagem']}")
        msg = EmailMessage()
        msg.set_content(corpo)
        msg["Subject"] = "Contato do formulario"
        msg["From"] = "vetalisge@gmail.com"
        msg["To"] = "vetalisge@gmail.com"

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

            return "Erro {e}"
import smtplib
from email.message import EmailMessage

# Criar a mensagem
corpo = "Olá, este é um teste enviado pelo Python!"
msg = EmailMessage()
msg.set_content(corpo)
msg["Subject"] = "A vitoria esta maulca"
msg["From"] = "vetalisge@gmail.com"
msg["To"] = "vitoria.h.silva9@aluno.senai.br"

# Enviar via servidor SMTP (exemplo do Gmail)
smtp_server = "smtp.gmail.com"
smtp_port = 587
senha_app = "@v3t1i525"

try:
  with smtplib.SMTP(smtp_server, smtp_port) as servidor:
    servidor.starttls()  # Segurança TLS
    servidor.login(msg["From"], senha_app)
    servidor.send_message(msg)
  print("E-mail enviado com sucesso!")
except Exception as e:
  print(f"Erro ao enviar: {e}")
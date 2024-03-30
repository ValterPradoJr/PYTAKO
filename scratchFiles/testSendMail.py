import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender_email, sender_password, receiver_email, subject, message_body):
    try:
        # Configurar a mensagem
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject

        # Corpo da mensagem
        body = message_body
        message.attach(MIMEText(body, 'plain'))

        # Conectar-se ao servidor SMTP do Gmail
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print("Erro ao enviar o e-mail:", e)

# Preencha com suas informações
sender_email = 'appbolaodosguri@gmail.com'
sender_password = 'qpiq qeda snqw cblu'
receiver_email = 'tomas.heuert@hotmail.com'
subject = 'Teste de Envio de E-mail'
message_body = 'Olá! Este é um teste de envio de e-mail.'

# Envie o e-mail
send_email(sender_email, sender_password, receiver_email, subject, message_body)
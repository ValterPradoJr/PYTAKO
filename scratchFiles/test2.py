import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, render_template, redirect, url_for
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import secrets


# Função para gerar token único
def generate_token():
    return secrets.token_urlsafe(16)

# Função para enviar e-mail usando SMTP do Gmail
def send_email(receiver_email, token):
    # sender_email = 'appbolaodosguri@gmail.com'  # Seu endereço de e-mail do Gmail
    # password = 'Bolao@2022'  # Sua senha do Gmail
    sender_email = '215192016@eniac.edu.br'  # Seu endereço de e-mail do Gmail
    password = 'Nidabenimsevgilim*963,'  # Sua senha do Gmail

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'Redefinição de Senha'

    body = f'Você solicitou a redefinição de senha. Use o seguinte token para redefinir sua senha: {token}'
    message.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender_email, password)
        server.send_message(message)

send_email('tomas.heuert@hotmail.com', generate_token())


# # Rota para solicitar redefinição de senha
# @app.route('/forgot-password', methods=['GET', 'POST'])
# def forgot_password():
#     if request.method == 'POST':
#         email = request.form['email']
#         session = Session()
#         user = session.query(User).filter_by(email=email).first()
#         if user:
#             token = generate_token()
#             send_email(email, token)
#             # Atualizar o token no banco de dados
#         session.close()
#         return redirect(url_for('login'))
#     return render_template('forgot_password.html')
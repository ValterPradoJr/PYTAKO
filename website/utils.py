import json
import smtplib
import secrets
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Função para gerar token único
def generate_token():
    return secrets.token_urlsafe(4).upper()

def send_email(receiver_email, subject, message_body):
    mail_attempt = {'status': True, 'message': ''}

    try:

        sender_email = 'appbolaodosguri@gmail.com'
        sender_password = 'qpiq qeda snqw cblu'

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
        mail_attempt["status"] = True
        mail_attempt["message"] = "Código de confirmação enviado para: " + receiver_email + ".\nPode ser que você precise checar sua caixa de spam."
    except Exception as e:
        print("Erro ao enviar o e-mail:", e)
        mail_attempt["status"] = False
        mail_attempt["message"] = "Erro ao enviar o e-mail: " + e

    return mail_attempt

def calcular_resultado(tabela_atual, apostas, usuarios):
    print (tabela_atual, apostas,usuarios)
    if not apostas:
        return
    bolao = Bolao()
    resultado = []
    for usuario in usuarios:
        print(usuario.nome_completo)
    for aposta in apostas:

        try: 
            apostador = next(user for user in usuarios if user.id == aposta.user_id)
        except StopIteration:
            continue
        print(aposta.user_id)
        aposta_json = json.loads(aposta.aposta_json)
        soma_pontuacao = 0
        for json_row in aposta_json:
            posicao_aposta = int(json_row['id'])
            posicao_real = int(next(item for item in tabela_atual if item['nome'] == json_row['nome'])['id'])
            soma_pontuacao += bolao.calcular_pontuacao(posicao_aposta, posicao_real)

        resultado.append({'user': apostador, 'pontuacao': soma_pontuacao, 'data_confirmacao': aposta.data_confirmacao, 'id_aposta': aposta.id})

    return resultado

class Bolao:
    def __init__(self):
        self.regras_pontuacao = {
            "1": 30,
            "2": 20,
            "3": 20,
            "4": 20,
            "5": 20,
            "6": 20,
            "7": 10,
            "8": 10,
            "9": 10,
            "10": 10,
            "11": 10,
            "12": 10,
            "13": 10,
            "14": 10,
            "15": 10,
            "16": 10,
            "17": 20,
            "18": 20,
            "19": 20,
            "20": 30
        }

    def calcular_pontuacao(self, posicao_aposta, posicao_real):
        if posicao_aposta == posicao_real:
            return self.regras_pontuacao[str(posicao_aposta)]
        elif posicao_real > 16 and posicao_aposta == 1:
            return -20
        elif posicao_real <= 6 and 1 <= posicao_aposta <= 6:
            return 15
        elif 7 <= posicao_real <= 16 and 7 <= posicao_aposta <= 16:
            return 5
        elif 17 <= posicao_real <= 20 and 17 <= posicao_aposta <= 20:
            return 15
        else:
            return 0

    def desempate(self, lista_apostadores):
        return sorted(lista_apostadores, key=lambda x: x["aposta_primeiro"], reverse=True)
    
def valida_cpf(cpf):
    if cpf.isdigit() and len(cpf) == 11:
        numbers = [int(digit) for digit in cpf if digit.isdigit()]
        sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != expected_digit:
            return False

        # Validação do segundo dígito verificador:
        sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != expected_digit:
            return False

        return True
    else:
        return False
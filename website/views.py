from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, Time, Aposta, User
from datetime import datetime, date
from . import db
from .utils import *
from bs4 import BeautifulSoup
import requests
import json
import os


views = Blueprint('views', __name__)
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    #Tabela brasileirão
    table = get_resultado_bolao()
    headers = [header.text.strip() for header in table.find_all("th")] # Extrair os cabeçalhos da tabela
    headers.insert(0, 'Posição:')
    headers.insert(1, '')
    headers.insert(3, 'Status')
    # Extrair os dados da tabela
    has_times = len(Time.query.all()) > 0
    data = []
    for row in table.find_all("tr"):
        images = row.findAll('img')
        row_image = ''
        for image in images:
            row_image = image['src']
        row_data = [cell.text.strip() for cell in row.find_all("td")]
        if row_data:
            row_data[1] = row_image
            row_data[2] = row_data[2].replace(" >>","")
            data.append(row_data)
            if not has_times:
                new_time = Time(nome=row_data[2].replace(" >>",""), img_url=row_image)
                db.session.add(new_time)
                db.session.commit()

    #Busca resultados bolão
    user_aposta = Aposta.query.filter_by(user_id=current_user.id).first()
    apostas = Aposta.query.all()
    #users = User.query.all()
    users = User.query.filter_by(pagou_aposta=True).all()
    table = get_resultado_bolao()
    # Extrair os dados da tabela
    data = []
    resultado_step_1 = []
    counter = 1
    resultado_step_2 = []
    for row in table.find_all("tr"):
        row_data = [cell.text.strip() for cell in row.find_all("td")]
        if row_data:
            data.append(row_data)
    for row_data in data:
        nome_time = row_data[2].replace(" >>","")
        resultado_step_1.append({'id':counter,'nome':nome_time})
        counter += 1
    if resultado_step_1:
        if users:
            resultado_step_2 = sorted(calcular_resultado(resultado_step_1,apostas,users), key=lambda x: (-x['pontuacao'], x['data_confirmacao']))
            #sorted(lista_apostadores, key=lambda x: x["aposta_primeiro"], reverse=True)
            print(resultado_step_2)

    return render_template("home.html", user=current_user, theaders=headers, tdata=data, user_aposta=user_aposta, resultados=resultado_step_2)

@views.route('/tabela_brasileirao', methods=['GET'])
@login_required
def tabela_brasileirao():
    table = get_resultado_bolao()
    headers = [header.text.strip() for header in table.find_all("th")] # Extrair os cabeçalhos da tabela
    headers.insert(0, 'Posição:')
    headers.insert(1, '')
    headers.insert(3, 'Status')
    # Extrair os dados da tabela
    has_times = len(Time.query.all()) > 0
    data = []
    for row in table.find_all("tr"):
        images = row.findAll('img')
        row_image = ''
        for image in images:
            row_image = image['src']
        row_data = [cell.text.strip() for cell in row.find_all("td")]
        if row_data:
            row_data[1] = row_image
            row_data[2] = row_data[2].replace(" >>","")
            data.append(row_data)
            if not has_times:
                new_time = Time(nome=row_data[2].replace(" >>",""), img_url=row_image)
                db.session.add(new_time)
                db.session.commit()
        
    return render_template("tabela_brasileirao.html", theaders=headers, tdata=data, user=current_user)

@views.route('/minha_aposta', methods=['GET'])
@login_required
def minha_aposta():
    data_times = Time.query.all()
    current_aposta = Aposta.query.filter_by(user_id=current_user.id).first()
    formatted_aposta = []
    has_aposta = False
    data_limite = datetime(2024, 4, 13) #deve ser a data limite + 1 dia para o cálculo pois começa a valer em 00:00:00
    # Bloqueio do botão de cadastrar apostas
    prazo_limite = datetime.now() > data_limite
    dias_restantes = data_limite - datetime.now()
    print('Prazo limite passou:',prazo_limite)
    if current_aposta:
        has_aposta = True
        for row_aposta in json.loads(current_aposta.aposta_json):
            #print(next(item for item in data_times if item.nome == row_aposta['nome']).img_url)
            row_aposta['img_url'] = next(item for item in data_times if item.nome == row_aposta['nome']).img_url
            formatted_aposta.append(row_aposta)

    return render_template("minha_aposta.html", times=data_times, 
                           user=current_user, has_aposta=has_aposta, dias_restantes=dias_restantes,
                           current_aposta=current_aposta, formatted_aposta=formatted_aposta, prazo_limite=prazo_limite)

@views.route('/regras', methods=['GET'])
@login_required
def regras():
    return render_template("regras.html", user=current_user)

@views.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    if request.method == 'POST': 
        user = User.query.filter_by(id=current_user.id).first()
        user.email = request.form.get('email')
        user.nome_completo = request.form.get('nome_completo')
        user.data_inicioti = datetime.strptime(request.form.get('data_inicioti'), '%Y-%m-%d').date()
        
        foto_perfil = request.files['foto_perfil']
        
        if foto_perfil:
            if allowed_file(foto_perfil.filename):
                upload_folder = 'website/static/users/'+str(user.id)+'/'
                
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                existing_files = os.listdir(upload_folder)
                for existing_file in existing_files:
                    file_path = os.path.join(upload_folder, existing_file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)  # Delete the existing file

                filename = upload_folder + foto_perfil.filename
                user_path = './static/users/'+str(user.id)+'/' + foto_perfil.filename
                foto_perfil.save(filename)
                user.foto_perfil = user_path
            else:
                flash('Extensão do arquivo não de imagem', category='error')
                return render_template("perfil.html", user=current_user)
        db.session.commit()
        flash('Alterações salvas com sucesso!')

    return render_template("perfil.html", user=current_user)

@views.route('/admin_area', methods=['GET','POST'])
@login_required
def admin_area():
    users = User.query.all()
    apostas = Aposta.query.all()
    for aposta in apostas:
        aposta.user = next(user for user in users if user.id == aposta.user_id)

    return render_template('admin_area.html', user=current_user, users=users, apostas=apostas)

@views.route('/apostas_outros', methods=['GET','POST'])
@login_required
def apostas_outros():
    data_times = Time.query.all()
    users = User.query.all()
    formatted_users = []
    user_aposta = Aposta.query.filter_by(user_id=current_user.id).first()
    for user in users:
        current_aposta = Aposta.query.filter_by(user_id=user.id).first()
        if current_aposta:
            formatted_aposta = []
            for row_aposta in json.loads(current_aposta.aposta_json):
            #print(next(item for item in data_times if item.nome == row_aposta['nome']).img_url)
                row_aposta['img_url'] = next(item for item in data_times if item.nome == row_aposta['nome']).img_url
                formatted_aposta.append(row_aposta)
            formatted_user = { 'user_data': user, 'aposta': current_aposta, 'formatted_aposta': formatted_aposta}
            formatted_users.append(formatted_user)

    return render_template('apostas_outros.html', user=current_user, users=formatted_users, user_aposta=user_aposta)

@views.route('/resultado_bolao', methods=['GET', 'POST'])
@login_required
def resultado_bolao():
    user_aposta = Aposta.query.filter_by(user_id=current_user.id).first()
    apostas = Aposta.query.all()
    #users = User.query.all()
    users = User.query.filter_by(pagou_aposta=True).all()
    table = get_resultado_bolao()
    # Extrair os dados da tabela
    data = []
    resultado_step_1 = []
    counter = 1
    resultado_step_2 = []
    for row in table.find_all("tr"):
        row_data = [cell.text.strip() for cell in row.find_all("td")]
        if row_data:
            data.append(row_data)
    for row_data in data:
        nome_time = row_data[2].replace(" >>","")
        resultado_step_1.append({'id':counter,'nome':nome_time})
        counter += 1
    if resultado_step_1:
        if users:
            resultado_step_2 = sorted(calcular_resultado(resultado_step_1,apostas,users), key=lambda x: (-x['pontuacao'], x['data_confirmacao']))
            #sorted(lista_apostadores, key=lambda x: x["aposta_primeiro"], reverse=True)
            print(resultado_step_2)

    return render_template('resultado_bolao.html', user=current_user, user_aposta=user_aposta, resultados=resultado_step_2)

@views.route('/salvar_aposta', methods=['POST'])
def salvar_aposta():
    aposta = json.loads(request.data)
    new_aposta = Aposta(aposta_json=json.dumps(aposta), user_id=current_user.id)
    db.session.add(new_aposta)
    db.session.commit()

    flash('Aposta salva com sucesso!', 'success')
    return True

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/handle_admin_action', methods=['POST'])
def handle_admin_action():  
    req = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    user_id = req['userId']
    action = req['action']
    user = User.query.get(user_id)
    if user:
        if action == 'admin':
            if user.has_admin and current_user.id == user.id:
                flash('Imposível revogar o próprio acesso de administrador!\nEu duvido que você realmente queira fazer isso...', category='error')
                return jsonify({})
            user.has_admin = not user.has_admin
            db.session.commit()
        if action == 'pagamento':
            user.pagou_aposta = not user.pagou_aposta
            db.session.commit()
    if action == 'excluir_aposta':
        aposta_delete = Aposta.query.get(user_id)
        if aposta_delete:
            apostador = User.query.get(aposta_delete.user_id)
            apostador.pagou_aposta = False
            db.session.delete(aposta_delete)
            db.session.commit()

    return jsonify({})

# json.dumps transforms to string
# json.loads transforms to json?
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_resultado_bolao():
    print('Requested Bolão')
    url = "https://www.terra.com.br/esportes/futebol/brasileiro-serie-a/tabela/"
    response = requests.get(url)
    print('Response Loaded')
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.find("table") #Caso precise identificar tabela não precisou
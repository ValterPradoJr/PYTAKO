from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from .utils import *
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Bem vindo de volta!', category='success')
                login_user(user, remember=True)
                user.cod_confirmacao = None
                db.session.commit()
                return redirect(url_for('views.home'))
            else:
                flash('Senha incorreta, tente novamente.', category='error')
        else:
            flash('Email não existe.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        # cpf = request.form.get('cpf')
        nome_completo = request.form.get('nome_completo')
        # data_inicioti = request.form.get('data_inicioti')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        has_admin_grant = email == 'tomas.heuert@hotmail.com'

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email já existe!', category='error')
        elif len(email) < 4:
            flash('Email deve conter mais de 3 caracteres!', category='error')
        elif len(nome_completo) < 2:
            flash('Seu nome não é tão curto, olhe seu documento de novo!', category='error')
        # elif not valida_cpf(cpf):
        #     flash('Verifique se você preencheu o CPF corretamente!', category='error')
        elif password1 != password2:
            flash('As senhas inseridas não são idênticas!', category='error')
        elif len(password1) < 7:
            flash('Senha deve conter mais de 7 caracteres!', category='error')
        else:
            new_user = User(email=email, 
                            # cpf=generate_password_hash(
                            #     cpf, method='pbkdf2:sha256'),
                            nome_completo=nome_completo, 
                            password=generate_password_hash(
                                password1, method='pbkdf2:sha256'),
                            # data_inicioti=datetime.strptime(data_inicioti, '%Y-%m-%d').date(),
                            foto_perfil='./static/no_picture.jpg',
                            has_admin=has_admin_grant)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Bem vindo ao Bolão da TI!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    pending_reset = False
    code_sent = False
    mail = None
    token = None
    if request.method == 'POST':
        controller = request.form.get('controller')
        email = request.form.get('email')
        # cpf = request.form.get('cpf')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        cod_confirmacao = request.form.get('cod_confirmacao')
        
        user = User.query.filter_by(email=email).first()
        
        test = True

        if controller == 'step1':
            if not user:
                flash('Email não encontrado!', category='error')
            else:
                token = generate_token()
                mail_body = f'Olá, você solicitou a redefinição de senha. Use o seguinte token para redefinir sua senha: {token}'
                response = send_email(user.email, 'Solicitação de alteração de senha PYTAKO', mail_body)
                if response['status']:
                    user.cod_confirmacao = token
                    db.session.commit()
                    pending_reset = True
                    mail = user.email
                    flash(response['message'], category='success')
                else:
                    flash(response['message'], category='error')
        if controller == 'step2':
            pending_reset = True
            mail = user.email
            if user.cod_confirmacao == cod_confirmacao:
                flash('Código confirmado com sucesso! Escolha uma nova senha.', category='success')
                code_sent = True
                token = cod_confirmacao
            else:
                flash('Código incorreto. Tente novamente.', category='error')
        if controller == 'step3':
            pending_reset = True
            mail = user.email
            code_sent = True
            token = cod_confirmacao
            if password1 != password2:
                flash('As senhas inseridas não são idênticas!', category='error')
            elif len(password1) < 7:
                flash('Senha deve conter mais de 7 caracteres!', category='error')
            elif check_password_hash(user.password, password1):
                flash('A senha não pode ser a mesma que a anterior. (Aparentemente você não esqueceu sua senha...)', category='error')
            else:
                user.password = generate_password_hash(password1, method='pbkdf2:sha256')
                user.cod_confirmacao = None
                db.session.commit()
                login_user(user, remember=True)
                flash('Bem vindo ao Bolão da TI!', category='success')
                flash('Senha alterada com sucesso', category='success')
                return redirect(url_for('views.home'))
    return render_template("forgot_password.html", user=current_user, pending_reset=pending_reset, code_sent=code_sent, mail=mail, token=token)


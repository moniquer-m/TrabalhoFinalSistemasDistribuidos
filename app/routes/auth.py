from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, login_required, logout_user
from app.models import User
from app.utils import validate_password, hash_password, check_password, generate_token, verify_token, send_email
from datetime import datetime, timedelta

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = current_app.config['USERS']
        login_attempts = current_app.config['LOGIN_ATTEMPTS']
        
        # Verifica se o usuário existe
        if username not in users:
            flash('Usuário não encontrado.', 'error')
            return render_template('login.html')
        
        # Verifica se o usuário está bloqueado
        if username in login_attempts:
            attempts, last_attempt = login_attempts[username]
            if attempts >= current_app.config['MAX_LOGIN_ATTEMPTS']:
                if datetime.now() - last_attempt < timedelta(minutes=current_app.config['LOGIN_TIMEOUT']):
                    remaining_time = timedelta(minutes=current_app.config['LOGIN_TIMEOUT']) - (datetime.now() - last_attempt)
                    flash(f'Conta bloqueada. Tente novamente em {remaining_time.seconds // 60} minutos e {remaining_time.seconds % 60} segundos.', 'error')
                    return render_template('login.html', is_blocked=True)
                else:
                    # Reset das tentativas após o tempo de bloqueio
                    login_attempts.pop(username)
        
        # Verifica a senha
        if check_password(users[username]['password'], password):
            user = User(username)
            login_user(user)
            flash('Login bem-sucedido!', 'success')
            login_attempts.pop(username, None)  # Remove as tentativas após login bem-sucedido
            if users[username]['role'] == 'super_admin':
                return redirect(url_for('admin.admin_panel'))
            return redirect(url_for('main.dashboard'))
        else:
            # Incrementa as tentativas de login
            if username not in login_attempts:
                login_attempts[username] = [1, datetime.now()]
            else:
                attempts, _ = login_attempts[username]
                login_attempts[username] = [attempts + 1, datetime.now()]
            
            remaining_attempts = current_app.config['MAX_LOGIN_ATTEMPTS'] - login_attempts[username][0]
            if remaining_attempts > 0:
                flash(f'Senha incorreta. Você tem mais {remaining_attempts} tentativa(s).', 'error')
            else:
                flash(f'Limite de tentativas atingido. Tente novamente em {current_app.config["LOGIN_TIMEOUT"]} minutos.', 'error')
            
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        full_name = request.form['full_name']
        email = request.form['email']

        users = current_app.config['USERS']

        if username in users:
            flash('Nome de usuário já existe. Por favor, escolha outro.', 'error')
        elif password != confirm_password:
            flash('As senhas não coincidem.', 'error')
        else:
            is_valid, message = validate_password(password)
            if not is_valid:
                flash(message, 'error')
            else:
                hashed_password = hash_password(password)
                users[username] = {
                    'password': hashed_password,
                    'full_name': full_name,
                    'email': email,
                    'role': 'pql'
                }
                current_app.config['USERS'] = users
                flash('Conta criada com sucesso! Você pode fazer login agora.', 'success')
                return redirect(url_for('auth.login'))

    return render_template('register.html')

@bp.route('/reset', methods=['GET', 'POST'])
def reset():
    if request.method == 'POST':
        email = request.form['email']
        users = current_app.config['USERS']
        user = next((user for user in users.values() if user['email'] == email), None)
        if user:
            token = generate_token(email)
            reset_url = url_for('auth.reset_with_token', token=token, _external=True)
            subject = "Instruções para redefinir sua senha"
            template = f"Para redefinir sua senha, visite o seguinte link: {reset_url}"
            
            print(f"Tentando enviar e-mail para: {email}")
            print(f"Usando servidor SMTP: {current_app.config['MAIL_SERVER']}:{current_app.config['MAIL_PORT']}")
            print(f"Usando conta de e-mail: {current_app.config['MAIL_USERNAME']}")
            
            if send_email(email, subject, template):
                flash('Um e-mail com instruções para redefinir sua senha foi enviado.', 'success')
                flash(f'Link de redefinição (apenas para desenvolvimento): {reset_url}', 'info')
            else:
                flash('Ocorreu um erro ao enviar o e-mail. Por favor, tente novamente.', 'error')
        else:
            flash('E-mail não encontrado.', 'error')
    return render_template('reset.html')

@bp.route('/reset/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    email = verify_token(token)
    if not email:
        flash('O link de redefinição de senha é inválido ou expirou.', 'error')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        new_password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if new_password != confirm_password:
            flash('As senhas não coincidem.', 'error')
            return render_template('reset_with_token.html')
        
        is_valid, message = validate_password(new_password)
        if not is_valid:
            flash(message, 'error')
            return render_template('reset_with_token.html')
        
        users = current_app.config['USERS']
        user = next((user for user in users.values() if user['email'] == email), None)
        if user:
            hashed_password = hash_password(new_password)
            user['password'] = hashed_password
            current_app.config['USERS'] = users
            flash('Sua senha foi atualizada com sucesso.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Usuário não encontrado.', 'error')
    
    return render_template('reset_with_token.html')
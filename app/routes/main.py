from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user, login_user
from app.utils import check_password, validate_password, hash_password

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    users = current_app.config['USERS']
    return render_template('dashboard.html', users=users)

@bp.route('/profile')
@login_required
def profile():
    users = current_app.config['USERS']
    user_data = users.get(current_user.id, {})
    return render_template('profile.html', user=user_data)

@bp.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    users = current_app.config['USERS']
    if request.method == 'POST':
        new_username = request.form['username']
        new_full_name = request.form['full_name']
        new_email = request.form['email']
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if not check_password(users[current_user.id]['password'], current_password):
            flash('Senha atual incorreta.', 'error')
            return redirect(url_for('main.profile'))

        if new_username != current_user.id and new_username in users:
            flash('Nome de usuário já existe. Por favor, escolha outro.', 'error')
            return redirect(url_for('main.profile'))

        old_username = current_user.id
        users[new_username] = users.pop(old_username)
        users[new_username]['full_name'] = new_full_name
        users[new_username]['email'] = new_email

        if new_password:
            if new_password == confirm_password:
                is_valid, message = validate_password(new_password)
                if not is_valid:
                    flash(message, 'error')
                    return redirect(url_for('main.profile'))
                users[new_username]['password'] = hash_password(new_password)
                flash('Perfil e senha atualizados com sucesso!', 'success')
            else:
                flash('As novas senhas não coincidem. A senha não foi atualizada.', 'error')
        else:
            flash('Perfil atualizado com sucesso!', 'success')

        current_user.id = new_username
        login_user(current_user)

        # Atualize a configuração do app com os usuários modificados
        current_app.config['USERS'] = users

        return redirect(url_for('main.profile'))
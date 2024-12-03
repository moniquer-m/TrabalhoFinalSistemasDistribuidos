from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required, current_user
from app.utils import validate_password, hash_password

bp = Blueprint('admin', __name__)

@bp.route('/admin')
@login_required
def admin_panel():
    users = current_app.config['USERS']
    if current_user.id not in users or users[current_user.id]['role'] not in ['admin', 'super_admin']:
        flash('Acesso negado. Você não tem privilégios de administrador.', 'error')
        return redirect(url_for('main.dashboard'))
    
    admin_filter = request.args.get('admin_filter', '').lower()
    user_filter = request.args.get('user_filter', '').lower()
    
    filtered_users = {
        username: user_data for username, user_data in users.items() 
        if (user_data['role'] in ['admin', 'super_admin'] and (not admin_filter or admin_filter in username.lower())) or
           (user_data['role'] in ['cliente', 'pql'] and (not user_filter or user_filter in username.lower()))
    }
    
    return render_template('admin.html', users=filtered_users)

@bp.route('/admin/add_user', methods=['POST'])
@login_required
def add_user():
    users = current_app.config['USERS']
    if current_user.id not in users or users[current_user.id]['role'] not in ['admin', 'super_admin']:
        flash('Acesso negado. Você não tem privilégios de administrador.', 'error')
        return redirect(url_for('main.dashboard'))
    
    username = request.form['username']
    password = request.form['password']
    full_name = request.form['full_name']
    email = request.form['email']
    role = request.form['role']

    if username in users:
        flash('Nome de usuário já existe. Por favor, escolha outro.', 'error')
    elif role not in ['cliente', 'pql', 'admin']:
        flash('Tipo de usuário inválido.', 'error')
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
                'role': role
            }
            current_app.config['USERS'] = users
            flash('Novo usuário adicionado com sucesso!', 'success')
    
    return redirect(url_for('admin.admin_panel'))

@bp.route('/admin/update_user/<username>', methods=['POST'])
@login_required
def update_user(username):
    users = current_app.config['USERS']
    if current_user.id not in users or users[current_user.id]['role'] not in ['admin', 'super_admin']:
        flash('Acesso negado. Você não tem privilégios de administrador.', 'error')
        return redirect(url_for('main.dashboard'))
    
    if username not in users:
        flash(f'Usuário {username} não encontrado.', 'error')
        return redirect(url_for('admin.admin_panel'))

    new_role = request.form.get('role')
    if new_role not in ['cliente', 'pql']:
        flash('Tipo de usuário inválido.', 'error')
        return redirect(url_for('admin.admin_panel'))

    if username == 'mo':
        flash('Não é permitido alterar o tipo do super admin.', 'error')
    elif users[username]['role'] == 'admin':
        flash('Não é permitido alterar o tipo de um administrador.', 'error')
    else:
        users[username]['role'] = new_role
        current_app.config['USERS'] = users
        flash(f'Tipo de usuário de {username} alterado para {new_role} com sucesso.', 'success')
    
    return redirect(url_for('admin.admin_panel'))

@bp.route('/admin/delete_user/<username>', methods=['POST'])
@login_required
def delete_user(username):
    users = current_app.config['USERS']
    if current_user.id not in users or users[current_user.id]['role'] not in ['admin', 'super_admin']:
        flash('Acesso negado. Você não tem privilégios de administrador.', 'error')
        return redirect(url_for('main.dashboard'))
    
    if username == 'mo':
        flash('Não é permitido excluir o super admin.', 'error')
    elif username == current_user.id:
        flash('Você não pode excluir seu próprio usuário.', 'error')
    elif username in users:
        del users[username]
        current_app.config['USERS'] = users
        flash(f'Usuário {username} foi excluído com sucesso.', 'success')
    else:
        flash(f'Usuário {username} não encontrado.', 'error')
    
    return redirect(url_for('admin.admin_panel'))
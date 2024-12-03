from passlib.hash import argon2
from itsdangerous import URLSafeTimedSerializer
import smtplib
from email.mime.text import MIMEText
import traceback
import re
from flask import current_app

def hash_password(password):
    return argon2.hash(password)

def check_password(hashed_password, user_password):
    return argon2.verify(user_password, hashed_password)

def validate_password(password):
    """
    Valida a senha de acordo com as seguintes regras:
    - Pelo menos 8 caracteres
    - Pelo menos uma letra maiúscula
    - Pelo menos uma letra minúscula
    - Pelo menos um número
    - Pelo menos um caractere especial
    """
    if len(password) < 8:
        return False, "A senha deve ter pelo menos 8 caracteres."
    
    if not re.search(r"[A-Z]", password):
        return False, "A senha deve conter pelo menos uma letra maiúscula."
    
    if not re.search(r"[a-z]", password):
        return False, "A senha deve conter pelo menos uma letra minúscula."
    
    if not re.search(r"\d", password):
        return False, "A senha deve conter pelo menos um número."
    
    if not re.search(r"[ !@#$%&'()*+,-./[\\$$^_`{|}~"+r'"]', password):
        return False, "A senha deve conter pelo menos um caractere especial."
    
    return True, "Senha válida."

def send_email(to, subject, template):
    msg = MIMEText(template)
    msg['Subject'] = subject
    msg['From'] = current_app.config['MAIL_USERNAME']
    msg['To'] = to

    try:
        smtp_server = smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT'])
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
        smtp_server.send_message(msg)
        smtp_server.close()
        print(f"E-mail enviado com sucesso para: {to}")
        return True
    except Exception as e:
        print(f"Erro detalhado ao enviar e-mail:")
        print(traceback.format_exc())
        return False

def generate_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])

def verify_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=current_app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
        return email
    except:
        return False
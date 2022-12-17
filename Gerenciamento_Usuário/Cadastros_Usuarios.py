import sqlite3 as sq
import bcrypt
from Crypto.Random import get_random_bytes
import re
import time
import smtplib, ssl
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

db = 'Gerenciamento_Usuário/banco_cadastro.db'

def creat_db():
    banco = sq.connect(db)
    cursor = banco.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS cadastro (login, email, senha, key, code)")
    banco.commit()
    banco.close()

def verifica(dado, select_where):
    banco = sq.connect(db)
    cursor = banco.cursor()
    cursor.execute(f"SELECT {select_where} FROM cadastro WHERE {select_where} = :dado", {'dado':dado})
    dado_db = cursor.fetchall()
    banco.commit()
    banco.close()

    if dado_db:
        return False
    return True

def verifica_usuario_att(usuario, usuario_novo, select_where = "login"):
    banco = sq.connect(db)
    cursor = banco.cursor()
    cursor.execute(f"SELECT {select_where} FROM cadastro WHERE {select_where} = :dado", {'dado':usuario_novo})
    usuario_db = cursor.fetchall()
    banco.commit()
    banco.close()

    if not usuario_db or usuario == usuario_novo:
        return True
    return False

def verifica_senha_code(usuario, senha_code, select = "senha", where = "login"):
    banco = sq.connect(db)
    cursor = banco.cursor()
    cursor.execute(f"SELECT {select} FROM cadastro WHERE {where} = :user", {'user':usuario})
    senha_code_db = cursor.fetchall()
    banco.commit()
    banco.close()
    if senha_code_db and bcrypt.checkpw(senha_code.encode(), senha_code_db[0][0]):
        return True
    return False

def valid_email(email):
    regex_email = re.compile(r"(?:\w+[\.\-\_]?[\w]*@[\w]+[\.\-][\w]+(?:[\.\-][\w]+)*)")
    email_valid = re.fullmatch(regex_email, email)
    if email_valid:
        return True
    return False

def hash(dado):
    return bcrypt.hashpw(dado.encode(), bcrypt.gensalt())

def cadastro_usuario(login, email, senha, confirm_senha):
    if senha == confirm_senha:
        banco = sq.connect(db)
        cursor = banco.cursor()
        key = get_random_bytes(16)
        hash_senha = hash(senha)
        cursor.execute("INSERT INTO cadastro VALUES (?, ?, ?, ?, ?)",
        (login, email, hash_senha, key, None))
        banco.commit()
        banco.close()
        return True
    return False

def dado(dado, select, where):
    banco = sq.connect(db)
    cursor = banco.cursor()
    cursor.execute(f"SELECT {select} FROM cadastro WHERE {where} = :dado", {'dado': dado})
    dado_db = cursor.fetchall()
    banco.commit()
    banco.close()

    if dado_db:
        return dado_db[0][0]
    return ''

def remove_usuario(usuario):
    where = "email" if valid_email(usuario) else "login"
    banco = sq.connect(db)
    cursor = banco.cursor()
    cursor.execute(f"DELETE FROM cadastro WHERE {where} = :user", {'user':usuario})
    banco.commit()
    banco.close()
    return True

def editar_usuario(usuario, usuario_novo, senha_nova, email_novo):
    hash_senha_att = hash(senha_nova)
    banco = sq.connect(db)
    cursor = banco.cursor()
    cursor.execute("UPDATE cadastro SET login = ?, email = ?, senha = ? WHERE login = ?",
    (usuario_novo, email_novo, hash_senha_att, usuario))
    banco.commit()
    banco.close()
    return True

def code_db(usuario, code):
    code = hash(code)
    atualiza_db(usuario, code)
    time.sleep(40)
    atualiza_db(usuario, None)

def atualiza_db(user, att, set = "code"):
    if set == "senha":
        att = hash(att)
    banco = sq.connect(db)
    cursor = banco.cursor()
    cursor.execute(f"UPDATE cadastro SET {set} = ? WHERE login = ?", (att, user))
    banco.commit()
    banco.close()

def code_email(usuario, receiver_email):
    code = ''.join([str(random.randint(0, 9)) for qtd in range(6)])
    smtp_server  = "smtp.office365.com"
    port = 587
    sender_email  = ""
    password = ""

    message = MIMEMultipart("alternative")
    message["Subject"] = "Sistema de Criptografia: Redefinir senha"
    message["From"] = sender_email
    message["To"] = receiver_email
    text = f'''\
        Olá,

        Seu código de verificação é: {code}'''
    html = f'''\
        <html>
            <body>
                <p>Ol&aacute; {usuario},<br>
                    Aqui est&aacute; o c&oacute;digo de verifica&ccedil;&atilde;o do Sistema de Criptografia para redefinir sua senha:<br>
                    <p <span style="font-size:22px"><strong>{code}</strong></span></span></p>
                </p>
                <p><strong>Atenciosamente,</strong><br>
                    <strong>Grupo 5</strong><br>
                </p>
            </body>
        </html>
        '''
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    message.attach(part1)
    message.attach(part2)

    context  = ssl.create_default_context()

    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        code_db(usuario, code)

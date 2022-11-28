import sqlite3 as sq
import bcrypt
from secrets import token_bytes
from getpass import getpass

db = 'Gerenciamento_Usuário/banco_cadastro.db'

def creat_db():
    banco = sq.connect(db)
    cursor = banco.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS cadastro (nome, login, pergunta, resposta, senha, key)")
    banco.commit()
    banco.close()

def verifica_usuario(cursor, usuario, usuario_att='', editar=False):
    cursor.execute("SELECT login FROM cadastro WHERE login = :user", {'user':usuario_att})
    usuario_db = cursor.fetchall()

    if usuario_db:
        if not editar:
            print("\n\033[31mERRO! Nome de usuário já cadastrado.\033[m")
            return True
        if usuario_att != usuario:
            print("\n\033[31mERRO! Nome de usuário já cadastrado.\033[m")
            return True
    return False

def verifica_senha(cursor, usuario, senha):
    cursor.execute("SELECT senha FROM cadastro WHERE login = :user", {'user':usuario})
    senha_db = cursor.fetchall()
    if senha_db:
        if bcrypt.checkpw(senha.encode(), senha_db[0][0]):
            return True
        print('\n\033[31mERRO! Senha incorreta.\033[m')
        return False
    print('\n\033[31mERRO! Usuário não cadastrado!\033[m')
    return False

def hash(dado):
    return bcrypt.hashpw(dado.encode(), bcrypt.gensalt())

def cadastro_usuario():
    nome = input('\n\033[32mNome completo: \033[m')
    login = input('\033[32mNome de usuário: \033[m')
    pergunta_seguranca = input("\033[32mDigite uma pergunta de segurança: \033[m").capitalize()
    resposta_seguranca = getpass(prompt='\033[32mResposta: \033[m').lower()
    senha = getpass(prompt='\033[32mSenha: \033[m')
    confirmacao_senha = getpass(prompt='\033[32mConfirme a senha: \033[m')

    if senha == confirmacao_senha:
        try:
            banco = sq.connect(db)
            cursor = banco.cursor()
            usuario_verificado = verifica_usuario(cursor, login)

            if not usuario_verificado:
                key = token_bytes(16)
                hash_senha, hash_resosta = hash(senha), hash(resposta_seguranca)
                cursor.execute("INSERT INTO cadastro VALUES (?, ?, ?, ?, ?, ?)",
                (nome, login, pergunta_seguranca, hash_resosta, hash_senha, key))
                print('\n\033[36mUsuário cadastrado com sucesso!\033[m')
            banco.commit()
            banco.close()

        except sq.Error as erro:
            print("\n\033[31mErro ao inserir os dados.\033[m", erro)
    else:
        print("\n\033[31mERRO! As senhas digitadas estão diferentes.\033[m")

def login():
    usuario = input('\n\033[32mNome de usuário: \033[m')
    senha = getpass(prompt='\033[32mSenha: \033[m')

    try:
        banco = sq.connect(db) 
        cursor = banco.cursor()
        senha_verificada = verifica_senha(cursor, usuario, senha)

        if senha_verificada:
            cursor.execute("SELECT key FROM cadastro WHERE login = :user", {'user':usuario})
            key_db = cursor.fetchall()
            banco.commit()
            banco.close()
            return True, usuario, key_db[0][0]

        else:
            return False, '', ''
    
    except sq.Error as erro:
        print("\n\033[31mErro no login.\033[m", erro)

def remove_usuario(usuario):
    senha = input('\033[32mConfirme sua senha: \033[m')

    banco = sq.connect(db) 
    cursor = banco.cursor()
    senha_verificada = verifica_senha(cursor, usuario, senha)

    if senha_verificada:
        cursor.execute("DELETE FROM cadastro WHERE login = :user", {'user':usuario})
        banco.commit()
        banco.close()
        print('\n\033[36mUsuário removido com sucesso.\033[m')
        return True

def editar_usuario(usuario):
    nome_att = input('\n\033[32mDigite seu nome completo: \033[m')
    usuario_att = input('\033[32mDigite seu novo nome de usuário: \033[m')
    pergunta_att = input('\033[32mDigite uma nova pergunta de segurança: \033[m')
    resposta_att = getpass(prompt='\033[32mDigite a resposta: \033[m').lower()
    senha_atual = getpass(prompt='\033[32mDigite sua senha: \033[m')
    nova_senha = getpass(prompt='\033[32mDigite sua nova senha: \033[m')
    confirme_nova_senha = getpass(prompt='\033[32mConfirme sua nova senha: \033[m')

    banco = sq.connect(db) 
    cursor = banco.cursor()
    senha_verificada = verifica_senha(cursor, usuario, senha_atual)
    usuario_verificado = verifica_usuario(cursor, usuario, usuario_att, True)

    if senha_verificada and nova_senha == confirme_nova_senha and not usuario_verificado:
        hash_senha_att, hash_resposta_att = hash(nova_senha), hash(resposta_att)
        cursor.execute("UPDATE cadastro SET nome = ?, login = ?, pergunta = ?, resposta = ?, senha = ? WHERE login = ?",
        (nome_att, usuario_att, pergunta_att, hash_resposta_att, hash_senha_att, usuario))
        banco.commit()
        banco.close()
        print('\n\033[36mUsuário atualizado com sucesso.\033[m')
        return True
    
    elif nova_senha != confirme_nova_senha:
        print('\n\033[31mERRO! As senhas digitadas estão diferentes.\033[m')

    banco.commit()
    banco.close()

def pergunta_seguranca():
    usuario = input('\n\033[32mDigite seu nome de usuário: \033[m')

    try:
        banco = sq.connect(db) 
        cursor = banco.cursor()
        cursor.execute("SELECT pergunta, resposta FROM cadastro WHERE login = :user", {'user':usuario})
        pergunta_resposta_db = cursor.fetchall()
        banco.commit()
        banco.close()

        resposta = getpass(prompt=f'\033[32m{pergunta_resposta_db[0][0]} \033[m').lower()
        if bcrypt.checkpw(resposta.encode(), pergunta_resposta_db[0][1]):
            return True, usuario
        print('\n\033[31mERRO! A resposta está errada.\033[m')
        return False, ''

    except IndexError:
        print('\n\033[31mERRO! Nome de usuário não cadastrado.\033[m')
        return False, ''

def recuperar_senha():
    pergunta_validacao, usuario = pergunta_seguranca()

    if pergunta_validacao:
        nova_senha = getpass(prompt='\033[32mDigite sua nova senha: \033[m')
        confirme_nova_senha = getpass(prompt='\033[32mConfirme sua nova senha: \033[m')
        if nova_senha == confirme_nova_senha:
            hash_senha_nova = hash(nova_senha)
            banco = sq.connect(db) 
            cursor = banco.cursor()
            cursor.execute("UPDATE cadastro SET senha = ? WHERE login = ?", (hash_senha_nova, usuario))
            banco.commit()
            banco.close()
            print('\n\033[36mSenha redefinida com sucesso.\033[m')
        else:
            print('\n\033[31mERRO! As senhas digitadas estão diferentes.\033[m')
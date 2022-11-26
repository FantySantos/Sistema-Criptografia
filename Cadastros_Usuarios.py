import sqlite3
import bcrypt

db = 'banco_cadastro.db'

def creat_db():
    banco = sqlite3.connect(db)
    cursor = banco.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS cadastro (nome, login, senha)")
    banco.commit()
    banco.close()

def cadastro_usuario():
    nome = input('\n\033[32mNome completo: \033[m')
    login = input('\033[32mNome de usuário: \033[m')
    senha = input('\033[32mSenha: \033[m')
    confirmacao_senha = input('\033[32mConfirme a senha: \033[m')

    if (senha == confirmacao_senha):
        try:
            banco = sqlite3.connect(db)
            cursor = banco.cursor()
            cursor.execute("SELECT login FROM cadastro WHERE login = :user", {'user':login})
            if cursor.fetchall():
                print("\n\033[31mNome de usuário já cadastrado.\033[m")

            else:
                hash_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
                cursor.execute("INSERT INTO cadastro VALUES (?, ?, ?)", (nome, login, hash_senha))
                banco.commit()
                banco.close()
                print('\n\033[32mUsuário cadastrado com sucesso!\033[m')

        except sqlite3.Error as erro:
            print("\n\033[31mErro ao inserir os dados.\033[m", erro)
    else:
        print("\n\033[31mAs senhas digitadas estão diferentes.\033[m")


def login():
    usuario = input('\n\033[32mNome de usuário: \033[m')
    senha = input('\033[32mSenha: \033[m')

    try:
        banco = sqlite3.connect(db) 
        cursor = banco.cursor()
        cursor.execute("SELECT senha FROM cadastro WHERE login = :user", {'user':usuario})
        senha_db = cursor.fetchall()
        banco.close()

        if bcrypt.checkpw(senha.encode('utf-8'), senha_db[0][0]):
            return True, usuario

        else:
            print('\n\033[31mSenha incorreta.\033[m')
            return False, ''
    
    except sqlite3.Error as erro:
        print("\n\033[31mErro no login.\033[m", erro)

    except IndexError as erro:
        print('\n\033[31mUsuário não cadastrado!\033[m')
    
def remove_usuario():
    usuario = input('\n\033[32mConfirme seu nome de usuário: \033[m')
    senha = input('\033[32mConfirme sua senha: \033[m')

    banco = sqlite3.connect(db) 
    cursor = banco.cursor()
    cursor.execute("SELECT senha FROM cadastro WHERE login = :user", {'user':usuario})
    senha_db = cursor.fetchall()

    if bcrypt.checkpw(senha.encode('utf-8'), senha_db[0][0]):
        cursor.execute("DELETE FROM cadastro WHERE login = :user", {'user':usuario})
        banco.commit()
        banco.close()

        print('\n\033[32mUsuário removido com sucesso.\033[m')
        return True

    else:
        print('\n\033[31mSenha incorreta.\033[m')

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
    nome = input('\nNome completo: ')
    login = input('Nome de usuário: ')
    senha = input('Senha: ')
    confirmacao_senha = input('Confirme a senha: ')

    if (senha == confirmacao_senha):
        try:
            banco = sqlite3.connect(db)
            cursor = banco.cursor()
            cursor.execute("SELECT login FROM cadastro WHERE login = :user", {'user':login})
            if cursor.fetchall():
                print("Nome de usuário já cadastrado.")

            else:
                hash_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
                cursor.execute("INSERT INTO cadastro VALUES (?, ?, ?)", (nome, login, hash_senha))
                banco.commit()
                banco.close()
                print('Usuário cadastrado com sucesso!')
                return True

        except sqlite3.Error as erro:
            print("Erro ao inserir os dados.", erro)
    else:
        print("As senhas digitadas estão diferentes.")


def login():
    usuario = input('\nNome de usuário: ')
    senha = input('Senha: ')

    
    try:
        banco = sqlite3.connect(db) 
        cursor = banco.cursor()
        cursor.execute("SELECT senha FROM cadastro WHERE login = :user", {'user':usuario})
        senha_db = cursor.fetchall()
        banco.close()

        if bcrypt.checkpw(senha.encode('utf-8'), senha_db[0][0]):
            return True, usuario

        else:
            print('Senha incorreta.')
    
    except sqlite3.Error as erro:
        print("Erro no login.", erro)

    except IndexError as erro:
        print('Usuário não cadastrado!')
    
def remove_usuario():
    usuario = input('\nConfirme seu nome de usuário: ')
    senha = input('Confirme sua senha: ')

    banco = sqlite3.connect(db) 
    cursor = banco.cursor()
    cursor.execute("SELECT senha FROM cadastro WHERE login = :user", {'user':usuario})
    senha_db = cursor.fetchall()

    if bcrypt.checkpw(senha.encode('utf-8'), senha_db[0][0]):
        cursor.execute("DELETE FROM cadastro WHERE login = :user", {'user':usuario})
        banco.commit()
        banco.close()

        print('Usuário removido com sucesso.')
        return True

    else:
        print('Senha incorreta.')

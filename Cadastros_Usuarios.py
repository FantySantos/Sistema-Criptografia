import sqlite3
import bcrypt

def cadastro_de_usuario():
    nome = input('Nome completo: ')
    login = input('Nome de usuário: ')
    senha = input('Senha: ')
    confirmacao_senha = input('Confirme a senha: ')

    if (senha == confirmacao_senha):
        try:
            hash_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
            banco = sqlite3.connect('banco_cadastro.db')
            cursor = banco.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS cadastro (nome, login, senha)")
            cursor.execute("INSERT INTO cadastro VALUES (?, ?, ?)", (nome, login, hash_senha))
            banco.commit()
            banco.close()

            print("Usuario cadastrado com sucesso.")

        except sqlite3.Error as erro:
            print("Erro ao inserir os dados.", erro)
    else:
        print("As senhas digitadas estão diferentes.")


def login():
    usuario = input('Nome de usuário: ')
    senha = input('Senha: ')

    
    try:
        banco = sqlite3.connect('banco_cadastro.db') 
        cursor = banco.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS cadastro (nome, login, senha)")
        cursor.execute("SELECT senha FROM cadastro WHERE login = :user", {'user':usuario})
        senha_db = cursor.fetchall()
        banco.close()

        if bcrypt.checkpw(senha.encode('utf-8'), senha_db[0][0]):
            print('Você está logado!')
        else:
            print('Senha incorreta.')
    
    except:
        print('Nome de usuário não cadastrado.')
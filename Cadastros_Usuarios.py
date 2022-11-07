import sqlite3

def cadastro_de_usuario():
    nome = input('Nome completo: ')
    login = input('Nome de usuário: ')
    senha = input('Senha: ')
    confirmacao_senha = input('Confirme a senha: ')

    if (senha == confirmacao_senha):
        try:
            banco = sqlite3.connect('banco_cadastro.db')
            cursor = banco.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS cadastro (nome text,login text,senha text)")
            cursor.execute(f"INSERT INTO cadastro VALUES ('{nome}','{login}','{senha}')")
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
        cursor.execute("CREATE TABLE IF NOT EXISTS cadastro (nome text,login text,senha text)")
        cursor.execute(f"SELECT senha FROM cadastro WHERE (login='{usuario}')")
        senha_db = cursor.fetchall()
        banco.close()

        if senha == senha_db[0][0]:
            print('Você está logado!')
        else:
            print('Senha incorreta.')
    
    except:
        print('Nome de usuário não cadastrado.')
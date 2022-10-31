import sqlite3

def cadastro():
    nome = input('Nome completo: ')
    login = input('Nome de usuário: ')
    senha = input('Senha: ')
    c_senha = input('Confirme a senha: ')

    if (senha == c_senha):
        try:
            banco = sqlite3.connect('banco_cadastro.db') 
            cursor = banco.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS cadastro (nome text,login text,senha text)")
            cursor.execute("INSERT INTO cadastro VALUES ('"+nome+"','"+login+"','"+senha+"')")

            banco.commit() 
            banco.close()
            print("Usuario cadastrado com sucesso")

        except sqlite3.Error as erro:
            print("Erro ao inserir os dados.", erro)
    else:
        print("As senhas digitadas estão diferentes")


def menu():
    op = int(input('''
            Bem vinde!!

        Escolha uma opção:
    [1] Cadastrar usuário.
    [2] Fazer login.
    [3] Sair.
        
    '''))
    return op

def controle():
    controle = menu()

    while controle != 3:
        if controle == 1:
            cadastro()

        elif controle == 2:
            pass

        else:
            print('Valor inválido.')
        
        controle = menu()
    
    print('Programa finalizado!')

controle()
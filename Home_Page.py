from Cadastros_Usuarios import cadastro_de_usuario, login



def menu():
    op = int(input('''
            Bem vindo!!
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
            cadastro_de_usuario()
        elif controle == 2:
            login()
        else:
            print('Valor inválido.')
        controle = menu()

    print('Programa finalizado!')
    
controle()
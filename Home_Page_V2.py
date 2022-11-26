from menu import menu, em_construção, cabecalho
from Cadastros_Usuarios import cadastro_usuario, login, remove_usuario
from time import sleep

op_inicial = ['Cadastrar usuário', 'Fazer login', 'Recuperar senha', 'Sair do sistema']
op_login = ['Criptografar', 'Descriptografar', 'Conta', 'Voltar']
op_conta = ['Editar usuário', 'Excluir usuário', 'Voltar']

def menu_inicial():
    while True: 
        controle = menu('SISTEMA DE CRIPTOGRAFIA', op_inicial)
        if controle == 1:
            cadastro_usuario()
        elif controle == 2:
            login_user, user = login()
            if login_user:
                menu_login(user)
        elif controle == 3:
            em_construção()
        elif controle == 4:
            cabecalho('Saindo do sistema... Até logo!')
            break
        else:
            print('\033[31ERRO! Digite uma opção válida!\033[m')
        sleep(2)

def menu_login(user):
    while True:
        controle = menu(f'BEM VINDO {user}', op_login)
        if controle == 1:
            em_construção()
        elif controle == 2:
            em_construção()
        elif controle == 3:
            menu_conta()
            break
        elif controle == 4:
            break
        else:
            print('\033[31ERRO! Digite uma opção válida!\033[m')
        sleep(2)

def menu_conta():
    while True:
        controle = menu('CONTA', op_conta)
        if controle == 1:
            em_construção()
        elif controle == 2:
            if remove_usuario():
                break
        elif controle == 3:
            break
        else:
            print('\033[31ERRO! Digite uma opção válida!\033[m')
        sleep(2)
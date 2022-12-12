from Interface.Menu import menu, cabecalho
from Gerenciamento_Usuário.Cadastros_Usuarios import cadastro_usuario, login, remove_usuario, editar_usuario, recuperar_senha
from Sistema_Criptografia.Criptografia import run_encrypt, run_decrypt
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
            login_user, user, key = login()
            if login_user:
                menu_login(user, key)
        elif controle == 3:
            recuperar_senha()
        elif controle == 4:
            cabecalho('Saindo do sistema... Até logo!')
            break
        else:
            print('\n\033[31mERRO! Digite uma opção válida!\033[m')
        sleep(2)

def menu_login(user, key):
    while True:
        controle = menu(f'BEM VINDO {user}', op_login)
        if controle == 1:
            run_encrypt(key)
        elif controle == 2:
            run_decrypt()
        elif controle == 3:
            if menu_conta(user):
                break
        elif controle == 4:
            break
        else:
            print('\n\033[31mERRO! Digite uma opção válida!\033[m')
        sleep(2)

def menu_conta(user):
    while True:
        controle = menu('CONTA', op_conta)
        if controle == 1:
            if editar_usuario(user):
                return True
        elif controle == 2:
            if remove_usuario(user):
                return True
        elif controle == 3:
            return False
        else:
            print('\n\033[31mERRO! Digite uma opção válida!\033[m')
        sleep(2)
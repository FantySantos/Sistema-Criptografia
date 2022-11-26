from Cadastros_Usuarios import cadastro_usuario, login, remove_usuario

def em_construção():
    return print('''

    Em construção...

                             ___
                     /======/
            ____    //      \___       ,/
             | \\  //           :,   ./
     |_______|__|_//            ;:; /
    _L_____________\o           ;;;/
____(CCCCCCCCCCCCCC)____________-/_______________

    ''')

def menu_inicial():
    return int(input('''
            Bem vindo!!
        
    [1] Cadastrar usuário.
    [2] Fazer login.
    [3] Recuperar senha.
    [0] Sair.

    Escolha uma opção: '''))

def menu_login(user):
    return int(input(f'''
            Olá, {user}!
        
    [1] Criptografar.
    [2] Descriptografar.
    [3] Configurações.
    [0] Voltar.
    
    Escolha uma opção: '''))

def menu_confirguracao():
    return int(input('''
            Configurações.
        Escolha uma opção:
    [1] Editar usuário.
    [2] Excluir usuário.
    [0] Voltar.
    
    Escolha uma opção: '''))


def controle_menu_inicial():
    controle = menu_inicial()

    while True:
        if controle == 1:
            cadastro_usuario()
        elif controle == 2:
            login_user, user = login()
            if login_user:
                controle_menu_login(user)
        elif controle == 3:
            em_construção()
        else:
            print('Valor inválido.')

    print('Programa finalizado!')


def controle_menu_login(user):
    controle = menu_login(user)

    while True:
        if controle == 1:
            em_construção()
        elif controle == 2:
            em_construção()
        elif controle == 3:
            controle_menu_login()
        else:
            print('Valor inválido.')
        controle = menu_login(user)

def controle_configuracao():
    controle = menu_confirguracao()

    if controle == 1:
        em_construção()
        controle_configuracao()

    elif controle == 2:
        if not remove_usuario():
            controle_configuracao()
    else:
        print('Valor inválido.')
        controle_configuracao()
from Cadastros_Usuarios import cadastro_usuario, login, remove_usuario

def em_construção():
    return print(
    '''

    Em construção...

                             ___
                     /======/
            ____    //      \___       ,/
             | \\  //           :,   ./
     |_______|__|_//            ;:; /
    _L_____________\o           ;;;/
____(CCCCCCCCCCCCCC)____________-/_____________________

    '''
    )

def menu_inicial():
    return input('''
            Bem vindo!!
        Escolha uma opção:
    [1] Cadastrar usuário.
    [2] Fazer login.
    [3] Recuperar senha.
    [4] Sair.
        
    ''')

def menu_login(user):
    return input(f'''
            Olá, {user}!
        Escolha uma opção:
    [1] Criptografar.
    [2] Descriptografar.
    [3] Configurações.
    [4] Voltar.
        
    ''')

def menu_confirguracao():
    return input('''
            Configurações.
        Escolha uma opção:
    [1] Editar usuário.
    [2] Excluir usuário.
    [3] Voltar.
        
    ''')


def controle_menu_inicial():
    controle = menu_inicial()

    while controle != '4':
        if controle == '1':
            if cadastro_usuario():
                controle_menu_inicial()
        elif controle == '2':
            login_user, user = login()
            if login_user:
                controle_menu_login(user)
        elif controle == '3':
            em_construção()
        else:
            print('Valor inválido.')
        controle = menu_inicial()
    
    print('Programa finalizado!')


def controle_menu_login(user):
    controle = menu_login(user)

    while controle != '4':
        if controle == '1':
            em_construção()
        elif controle == '2':
            em_construção()
        elif controle == '3':
            controle_configuracao()
        else:
            print('Valor inválido.')

        controle = menu_login(user)

def controle_configuracao():
    controle = menu_confirguracao()

    while controle != '3':
        if controle == '1':
            em_construção()
        elif controle == '2':
            if remove_usuario():
                controle_menu_inicial()
        else:
            print('Valor inválido.')

        controle = menu_confirguracao()
import flet
import Gerenciamento_Usuário.Cadastros_Usuarios as user
import time
import Cryptography.Criptografia as cripto
# Como prática de programação em python principalmente, importar as funções mais repetidas e chamá-las 
#   avulsamente no código, evite chamá-las com a lib colada nela (flet.Row, flet.Column, flet.ElevatedButton...)
from flet.buttons import RoundedRectangleBorder
from flet import ( Page, ElevatedButton, TextField, Column, Row, View, Container, AppBar, AlertDialog, icons, TextButton, Text, colors, ButtonStyle, IconButton
)

def main(page: Page):
    page.title = "Dory"
    page.theme_mode = "light"
    page.window_width = 800
    page.window_height = 650
    page.window_resizable = False   # Permite ou não o usuário de expandir a tela
    page.window_maximizable = False
    # Alinhamento dos elementos em relação à pagina
    page.vertical_alignment = "center" 
    page.horizontal_alignment = "center"
    page.window_center()

    def change_theme(e):
        """Quando o theme_icon_button é clicado, o tema é alterado,
        o ícone é modificado e a página é atualizada.

        Args:
            e: O evento que acionou a função.
        """
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        theme_icon_button.selected = not theme_icon_button.selected
        page.update()

    def btn_login(e):
        usuario_email = text_vazio(usuario_login)
        senha = text_vazio(senha_login)
        verifica_text = all([usuario_email, senha])

        if user.valid_email(usuario_email):
            verifica_login = user.verifica_senha_code(usuario_email, senha, where="email")
        else:
            verifica_login = user.verifica_senha_code(usuario_email, senha)

        if verifica_text and verifica_login:
            page.go("/criptografia")
            page.update()
        
        if usuario_email and senha and not verifica_login:
            showDialog(e, 'Usuário/Senha incorreta.')
        limpar("criptografia")
        email_usuario_att_value()
    
    def btn_cadastro(e):
        usuario  = text_vazio(usuario_cadastro)
        email = text_vazio(email_cadastro)
        senha = text_vazio(senha_cadastro)
        confirm_senha = text_vazio(confirm_senha_cadastro)
        erros = text_erros(usuario_cadastro, email_cadastro, senha_cadastro, confirm_senha_cadastro)
        verifica_user, verifica_email = user.verifica(usuario, 'login'), user.verifica(email, 'email')

        verifica_text = all([usuario, email, senha, confirm_senha, erros, verifica_user, verifica_email])

        if verifica_text:
            if user.cadastro_usuario(usuario, email, senha, confirm_senha):
                showDialog(e, 'Usuário cadastrado com sucesso!')
                limpar("cadastro")
                senha_cadastro.error_text = None
                confirm_senha_cadastro.error_text = None
                page.update()

            elif senha == confirm_senha:
                senha_cadastro.error_text = None
                confirm_senha_cadastro.error_text = None
                page.update()
        else:
            if usuario and not verifica_user:
                usuario_cadastro.error_text = "Nome de usuário já existe."
                page.update()
            if email and not verifica_email:
                email_cadastro.error_text = "Email já cadastrado"
                page.update()
    
    def btn_cifrar(e):
        usuario = usuario_login.value
        cifrar = text_vazio(mensagem_cifrar)
        if cifrar and usuario:
            chave_user = user.dado(usuario, "key", "login")
            ciphertext, key_iv = cripto.run_encrypt(cifrar, chave_user)
            mensagem_cifrar.value = None
            mensagem_cifrada.value = ciphertext
            chave.value = key_iv
            page.update()
    
    def btn_decifrar(e):
        decifrar = text_vazio(mensagem_cifrada)
        chave_decifrar = text_vazio(chave)

        if decifrar and chave_decifrar:
            plaintext = cripto.run_decrypt(decifrar, chave_decifrar)
            if plaintext:
                mensagem_cifrar.value = plaintext
                mensagem_cifrada.value = None
                chave.value = None
            else:
                showDialog(e, "Chave e/ou Mensagem corrompida.\n\nCertifique se você inseriu a mensagem e/ou chave corretamente.\nCaso ambas estejam corretas e o erro persista, entre em contato\ncom o emissor da mensagem.")
            page.update()

    def btn_atualizar(e):
        usuario, email, senha = text_vazio(usuario_cadastro), text_vazio(email_cadastro), text_vazio(senha_atual)
        senha_att, confirm_senha_att = text_vazio(senha_nova), text_vazio(confirm_senha_nova)
        erros = text_erros(usuario_cadastro, email_cadastro, senha_nova, confirm_senha_nova)
        verifica_login = user.verifica_senha_code(usuario_login.value, senha)
        email_user = user.dado(usuario_login.value, "email", "login")
        verifica_user_att = user.verifica_usuario_att(usuario_login.value, usuario)
        verifica_email_att = user.verifica_usuario_att(email_user, email, "email")

        verifica_text = all([usuario, email, senha_att, confirm_senha_att, erros, verifica_user_att, verifica_login, verifica_email_att])

        if verifica_text:
            if user.editar_usuario(usuario_login.value, usuario, senha_att, email):
                showDialog(e, "Usuário editado com sucesso.")
                limpar("editar")
                senha_nova.error_text = None
                confirm_senha_nova.error_text = None
                page.update()

            elif senha_att == confirm_senha_att:
                limpar("editar")
                senha_nova.error_text = None
                confirm_senha_nova.error_text = None
                page.update()
        else:
            if usuario and not verifica_user_att:
                usuario_cadastro.error_text = "Nome de usuário já existe."
                page.update()

            if senha and not verifica_login:
                senha_atual.error_text = "Senha incorreta."
                page.update()
            
            if email and not verifica_email_att:
                email_cadastro.error_text = "Email já cadastrado."
                page.update()
    
    def btn_send_code(e):
        def gocode():
            user_email.error_text = None
            page.go("/verificaCode")
            page.update()

        email_usuario = text_vazio(user_email)

        if email_usuario:
            if user.valid_email(email_usuario) and not user.verifica(email_usuario, "email"):
                usuario = user.dado(email_usuario, "login", "email")
                gocode()
                user.code_email(usuario, email_usuario)

            elif not user.verifica(email_usuario, "login"):
                email = user.dado(email_usuario, "email", "login")
                if email:
                    gocode()
                    user.code_email(email_usuario, email)
            else:
                user_email.error_text = "Usuário ou email não cadastrado."
                page.update()
    
    def verify_code(e):
        codigo_user = text_vazio(code)
        email_login = user_email.value
        
        if codigo_user:
            if user.valid_email(email_login):
                if user.verifica_senha_code(email_login, codigo_user, "code", "email"):
                    code.error_text = None
                    user.atualiza_db(email_login, None)
                    page.go("/redefinirsenha")
                    page.update()
                else:
                    code.error_text = "Código inválido."
                    page.update()
            else:
                if user.verifica_senha_code(email_login, codigo_user, "code", "login"):
                    code.error_text = None
                    user.atualiza_db(email_login, None)
                    page.go("/redefinirsenha")
                    page.update()
                else:
                    code.error_text = "Código inválido."
                    page.update()

    def redefinir_senha(e):
        senha_att = text_vazio(senha_nova)
        confirm_senha_att = text_vazio(confirm_senha_nova)
        email_usuario = user_email.value

        if senha_att and confirm_senha_att:
            if senha_att == confirm_senha_att:
                senha_nova.error_text = None
                confirm_senha_cadastro.error_text = None
                if user.valid_email(email_usuario):
                    usuario = user.dado(email_usuario, "login", "email")
                else:
                    usuario = email_usuario
                user.atualiza_db(usuario, senha_att, "senha")
                page.go("/")
                showDialog(e, "Senha redefinida com sucesso.")
            else:
                senha_nova.error_text = "As senhas digitadas estão diferentes."
                confirm_senha_nova.error_text = "As senhas digitadas estão diferentes."
                page.update()


    def text_vazio(txt_name):
        if not txt_name.value:
            txt_name.error_text = "Este campo é obrigatório."
            page.update()
            return ''
        return txt_name.value
    
    def verifica_vazio(txt_name):
        if txt_name:
            txt_name.error_text = None
            page.update()
    
    def text_erros(usuario, email, senha, confirm_senha):
        lista_bool = [1, 1, 1]

        if usuario.value and ' ' in usuario.value:
            usuario.error_text = "Nome de usuário não deve conter espaço."
            page.update()
            lista_bool.insert(0, 0)

        if senha.value and confirm_senha.value and senha.value != confirm_senha.value:
            senha.error_text = "As senhas digitadas estão diferentes."
            confirm_senha.error_text = "As senhas digitadas estão diferentes."
            page.update()
            lista_bool.insert(1, 0)
        
        if email.value and not user.valid_email(email.value):
            email.error_text = "Digite um email válido."
            page.update()
            lista_bool.insert(2, 0)
        return all(lista_bool)
    
    def btn_cadastre_se(e):
        limpar("cadastro")
        page.go("/cadastro")
        page.update()
    
    def email_usuario_att_value():
        if user.valid_email(usuario_login.value):
            email_cadastro.value = usuario_login.value
            usuario = user.dado(usuario_login.value, "login", "email")
            usuario_cadastro.value = usuario
        
        else:
            usuario_cadastro.value = usuario_login.value
            email_cadastro.value = user.dado(usuario_login.value, "email", "login")
            page.update()

    def showDialog(e, alerta):
        def close_dialog(e):
            show_dlg.open = False
            page.update()

        def open_dialog(e):
            page.dialog = show_dlg
            show_dlg.open = True
            page.update()

        show_dlg = AlertDialog(
            modal=True,
            content=Text(alerta, text_align="center"),
            actions=[ElevatedButton("OK", on_click=close_dialog)],
            actions_alignment="center"
            )
        open_dialog(e)
    
    def showDialogExcluir(e):
        usuario = usuario_login.value
        senha = text_vazio(senha_excluir)

        def close_dialog(e):
            show_dlg_excluir.open = False
            page.update()

        def open_dialog(e):
            page.dialog = show_dlg_excluir
            show_dlg_excluir.open = True
            page.update()
        
        def run_excluir(e):
            close_dialog(e)
            bool_remove = user.remove_usuario(usuario)
            if bool_remove:
                limpar("criptografia")
                page.go("/voltartelainicial")
                page.update()
            else:
                showDialog(e, "Erro ao remover usuário.")

        show_dlg_excluir = AlertDialog(
            modal=True,
            content=Text("Tem certeza de que deseja excluir sua conta?", text_align="center"),
            actions=[
                        Row(
                            [
                                ElevatedButton("CANCELAR", on_click=close_dialog,bgcolor=colors.RED, color=colors.WHITE),
                                ElevatedButton("CONFIRMAR", on_click=run_excluir, bgcolor=colors.GREEN, color=colors.WHITE)
                            ], alignment="center"
                        )
                    ],
            actions_alignment="center"
            )

        if (senha and user.verifica_senha_code(usuario, senha)) or (senha and user.verifica_senha_code(usuario, senha, where="email")):
            open_dialog(e)
        else:
            if senha:
                senha_excluir.error_text = "Senha incorreta."
                page.update()
    
    def limpar(pag):
        criptografia = [senha_login, chave, mensagem_cifrada, mensagem_cifrar, senha_excluir]
        cadastro = [usuario_cadastro, senha_cadastro, confirm_senha_cadastro, email_cadastro]
        editar = [senha_atual, senha_nova, confirm_senha_nova]
        if pag == "criptografia":
            botoes = criptografia
        elif pag == "cadastro":
            botoes = cadastro
        else:
            botoes = editar

        for botao in botoes:
            botao.value = None

    usuario_cadastro = TextField(
        label="Nome de Usuário", autofocus=True,
        prefix_icon=icons.PERSON, width=page.window_width/2,
        on_change=lambda _:verifica_vazio(usuario_cadastro)
        )

    senha_cadastro = TextField(
        label="Senha", width=page.window_width/2,
        prefix_icon=icons.LOCK_PERSON, password=True,
        can_reveal_password=True, on_change=lambda _:verifica_vazio(senha_cadastro)
        )

    confirm_senha_cadastro = TextField(
        label="Confirmação de senha", prefix_icon=icons.LOCK_PERSON,
        width=page.window_width/2, password=True,
        can_reveal_password=True,
        on_change=lambda _:verifica_vazio(confirm_senha_cadastro),
        on_submit=btn_cadastro
        )

    email_cadastro = TextField(
        label="E-mail", prefix_icon=icons.EMAIL,
        width=page.window_width/2,
        on_change=lambda _:verifica_vazio(email_cadastro)
        )

    usuario_login = TextField(
        label="Usuário", autofocus=True,
        prefix_icon=icons.PERSON,width=page.window_width/2,
        on_change=lambda _:verifica_vazio(usuario_login)
        )

    senha_login = TextField(
        label="Senha", prefix_icon=icons.LOCK_PERSON,
        password=True, can_reveal_password=True,
        width=page.window_width/2,
        on_change=lambda _:verifica_vazio(senha_login),
        on_submit=btn_login
        )

    mensagem_cifrar = TextField(
        autofocus=True, width=350,
        multiline=True, min_lines=8, max_lines=8,
        on_change=lambda _: verifica_vazio(mensagem_cifrar)
        )

    mensagem_cifrada = TextField(
        width=350, multiline=True, min_lines=8, max_lines=8,
        on_change=lambda _: verifica_vazio(mensagem_cifrada)
        )

    chave = TextField(
        hint_text="Chave:", width=265,
        border="none", filled=True,
        on_change=lambda _: verifica_vazio(chave)
        )
    
    senha_excluir = TextField(
        label="Senha", prefix_icon=icons.LOCK_PERSON,
        password=True, can_reveal_password=True,
        width=page.window_width/2,
        on_change=lambda _:verifica_vazio(senha_excluir),
        on_submit=showDialogExcluir,
        autofocus=True
        )
    
    senha_atual = TextField(
        label="Senha atual", width=page.window_width/2,
        prefix_icon=icons.LOCK_PERSON, password=True,
        can_reveal_password=True, on_change=lambda _:verifica_vazio(senha_atual)
        )
    
    senha_nova = TextField(
        label="Nova senha", width=page.window_width/2,
        prefix_icon=icons.LOCK_PERSON, password=True,
        can_reveal_password=True, on_change=lambda _:verifica_vazio(senha_nova)
        )

    confirm_senha_nova = TextField(
        label="Confirme sua nova senha", prefix_icon=icons.LOCK_PERSON,
        width=page.window_width/2, password=True,
        can_reveal_password=True, on_submit=btn_atualizar,
        on_change=lambda _:verifica_vazio(confirm_senha_nova)
        )
    
    user_email = TextField(
        label="Digite seu email ou nome de usuário",
        prefix_icon=icons.EMAIL, width=page.window_width/2,
        on_change=lambda _:verifica_vazio(user_email),
        autofocus=True, on_submit=btn_send_code
        )
    
    code = TextField(
        label="Código", width=page.window_width/2,
        prefix_icon=icons.LOCK_PERSON, password=True,
        can_reveal_password=True, on_change=lambda _:verifica_vazio(code),
        autofocus=True, on_submit=verify_code
        )

    # button to change theme_mode (from dark to light mode, or the reverse)
    theme_icon_button = flet.IconButton(icons.DARK_MODE, selected_icon=icons.LIGHT_MODE, icon_color=colors.BLACK,
    icon_size=25, tooltip="Mudar tema",
    on_click=change_theme,
    style=ButtonStyle(color={"": colors.BLACK, "selected": colors.WHITE},), )

    def route_change(e):
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    AppBar(
                        title=Text("Sistema de Criptografia"), center_title=True,
                        bgcolor=flet.colors.SURFACE_VARIANT, actions=[theme_icon_button]
                    ),
                    Container(content=Column(
                            [
                                flet.Image(src="/img_login.png",
                                width=page.window_width/2.5),

                                usuario_login, senha_login,

                                Row(
                                    [
                                        TextButton(text="Esqueceu sua senha?", on_click= lambda _: page.go("/esqueceuSenha")),
                                        ElevatedButton(text="Login", on_click = btn_login, width=200, icon=icons.LOGIN)
                                    ], spacing=20, alignment="center"
                                ),

                                Container(width=400, bgcolor="black",height=0.5),

                                Row(
                                    [
                                        Text('Não é cadastrado?'),
                                        TextButton(text="Cadastre-se", on_click = btn_cadastre_se)
                                    ], spacing=0, alignment="center"
                                )
                            ], horizontal_alignment="center"
                        )
                    )
                ], vertical_alignment="center"
            )
        )

        if page.route == "/cadastro":
            page.views.append(
                View(
                    "/cadastro",
                    [
                        AppBar(
                            title=Text("Cadastro Usuário"), center_title=True,
                            bgcolor=flet.colors.SURFACE_VARIANT, actions=[theme_icon_button]
                        ),
                        Container(content=Column(
                                [
                                    usuario_cadastro, email_cadastro, senha_cadastro, confirm_senha_cadastro,
                                    ElevatedButton(text="Cadastrar Usuário", on_click = btn_cadastro, width=page.window_width/2),

                                    Row(
                                        [
                                            Text('Já é cadastrado?'),
                                            TextButton(text="Faça login", on_click = lambda _: page.go("/"))
                                        ], spacing=0, alignment="center"
                                    )
                                ], horizontal_alignment="center"
                            )
                        )
                    ], vertical_alignment="center"
                )
            )

        if page.route == "/esqueceuSenha":
            page.views.append(
                View(
                    "/esqueceuSenha",
                    [
                        AppBar(
                        title=Text("Recuperar Senha"), center_title=True,
                        bgcolor=flet.colors.SURFACE_VARIANT, actions=[theme_icon_button]
                        ),
                        Container(content = Column(
                                [
                                    Text("Digite seu email ou nome de usuário abaixo para receber o código de redefinição de senha:\n", style="bodyLarge", text_align="center", width=page.window_width/2, size=17),
                                    user_email,
                                    ElevatedButton(text="Enviar código", on_click = btn_send_code, width=page.window_width/2)
                                ], alignment="center"
                            )
                        )
                    ], vertical_alignment="center", horizontal_alignment="center"
                )
            )
            
        if page.route == "/verificaCode":
            page.views.append(
                View(
                    "/verificaCode",
                    [
                        AppBar(
                        title=Text("Código de verificação"), center_title=True,
                        bgcolor=flet.colors.SURFACE_VARIANT, actions=[theme_icon_button],
                        leading=IconButton(icon=icons.ARROW_BACK, tooltip="Voltar",
                        on_click=lambda _: page.go("/esqueceuSenha"))
                        ),
                        Container(content = Column(
                                [
                                    Text("Digite abaixo o código enviado por email:\n", style="bodyLarge", text_align="center", width=page.window_width/2, size=17),
                                    code,
                                    ElevatedButton(text="Verificar", on_click=verify_code, width=page.window_width/2),
                                    Text("\n Seu código expirará em 40 segundos."),
                                    TextButton(text="Reenviar código", on_click=btn_send_code)
                                ], alignment="center"
                            )
                        )
                    ], vertical_alignment="center", horizontal_alignment="center"
                )
            )
        
        if page.route == "/redefinirsenha":
            page.views.append(
                View(
                    "/redefinirsenha",
                    [
                        AppBar(
                        title=Text("Código de verificação"), center_title=True,
                        bgcolor=flet.colors.SURFACE_VARIANT, actions=[theme_icon_button],
                        leading=IconButton(icon=icons.ARROW_BACK, tooltip="Voltar",
                        on_click=lambda _: page.go("/verificaCode"))
                        ),
                        Container(content = Column(
                                [
                                    Text("Digite sua nova senha:\n", style="bodyLarge", text_align="center", width=page.window_width/2, size=17),
                                    senha_nova, confirm_senha_nova,
                                    ElevatedButton(text="Redefinir senha", width=page.window_width/2, on_click=redefinir_senha)
                                ], alignment="center"
                            )
                        )
                    ], vertical_alignment="center", horizontal_alignment="center"
                )
            )
        
        if page.route == "/criptografia":
            page.views.append(
                View(
                    "/criptografia",
                    [
                        AppBar(
                            title=Text("Sistema de Criptografia"),
                            center_title=True, bgcolor=flet.colors.SURFACE_VARIANT, automatically_imply_leading=False,
                            actions=[
                                theme_icon_button,
                                flet.PopupMenuButton(icon=icons.SETTINGS,tooltip="Menu",
                                items=[
                                    flet.PopupMenuItem(text='Editar usuário', icon=icons.EDIT, on_click=lambda _: page.go("/editar")),
                                    flet.PopupMenuItem(text='Excluir usuário', icon=icons.CLOSE, on_click=lambda _: page.go("/excluir")),
                                    flet.PopupMenuItem(text='Logout', icon=icons.LOGOUT, on_click=lambda _: page.go("/"))
                                    ]
                                )
                            ]
                        ),
                        Container(content=Row(
                                [
                                    Column(
                                        [
                                            Text("Texto para criptografar:", style="titleMedium"),
                                            mensagem_cifrar,
                                            ElevatedButton("Cifrar", on_click=btn_cifrar, width=350, height=45, style=ButtonStyle(shape=RoundedRectangleBorder(radius=0)))
                                        ]
                                    ),

                                    Column(
                                        [
                                            Text("Código para descriptografar:", style="titleMedium"),
                                            mensagem_cifrada,

                                            Row(
                                                [
                                                    chave,
                                                    ElevatedButton("Decifrar", on_click=btn_decifrar, width=85, height=45, style=ButtonStyle(shape=RoundedRectangleBorder(radius=0))),
                                                ], spacing=0
                                            )
                                        ]

                                    )
                                ], alignment="center"
                            )
                        )
                    ], vertical_alignment="center"
                )
            )
        if page.route == "/editar":
            page.views.append(
                View(
                    "/editar",
                    [
                        AppBar(
                        title=Text("Editar usuário"), center_title=True,
                        bgcolor=flet.colors.SURFACE_VARIANT, actions=[theme_icon_button],
                        leading=IconButton(icon=icons.ARROW_BACK, tooltip="Voltar",
                        on_click=lambda _: page.go("/criptografia"))
                        ),

                        Container(content=Column(
                                [
                                    usuario_cadastro, email_cadastro, senha_atual, senha_nova, confirm_senha_nova,
                                    ElevatedButton("Atualizar", width = page.window_width/2, on_click=btn_atualizar)
                                ]
                            )
                        )
                    ], vertical_alignment="center", horizontal_alignment="center"
                )
            )
        if page.route == "/excluir":
            page.views.append(
                View(
                    "/excluir",
                    [
                        AppBar(
                        title=Text("Sistema de Criptografia"), center_title=True,
                        bgcolor=flet.colors.SURFACE_VARIANT, actions=[theme_icon_button],
                        leading=IconButton(icon=icons.ARROW_BACK, tooltip="Voltar",
                        on_click=lambda _: page.go("/criptografia"))
                        ),

                        Container(content=Column(
                                [
                                    Text("Excluir seu usuário", style="headlineSmall", weight="bold"),
                                    Text("Quando você pressionar o botão abaixo todos os seus dados serão removidos permanentemente e não poderão ser recuperados.\n\n", width=400),
                                    Text("Para continuar, insira sua senha:"),
                                    senha_excluir,
                                    Text("\n"),
                                    ElevatedButton("Excluir minha conta permanentemente", bgcolor=colors.RED, color=colors.WHITE,
                                    style=ButtonStyle(shape=RoundedRectangleBorder(radius=0)), on_click=showDialogExcluir)
                                ]
                            )
                        )
                    ], vertical_alignment="center", horizontal_alignment="center"
                )
            )
        if page.route == "/voltartelainicial":
            page.views.append(
                View(
                    "/voltartelainicial",
                    [
                        AppBar(
                        title=Text("Tchau..."), center_title=True,
                        bgcolor=flet.colors.SURFACE_VARIANT, actions=[theme_icon_button]
                        ),

                        Container(content=Row(
                                [
                                    Column(
                                        [
                                            Text("Usuário removido com sucesso.", style="headlineSmall", weight="bold"),
                                            Text("Até a próxima :-(\n\n", style="titleMedium"),
                                            ElevatedButton("Ir para tela de login.", on_click=lambda _:page.go("/"), icon=icons.LOGIN)
                                        ]
                                    ),

                                    flet.Image(src="delete.png",height=200)
                                ], alignment="center"
                            )
                        )
                    ], vertical_alignment="center", horizontal_alignment="center"
                )
            )
        page.update()

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

user.creat_db()
flet.app(target=main, assets_dir='../Sistema-Criptografia/Images')
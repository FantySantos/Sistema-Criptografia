import flet
from flet import ElevatedButton, Text, TextField

def main(page):
    def btn_click(e):
        if not txt_name.value:
            txt_name.error_text = "Por favor, insira seu nome."
            page.update()
        else:
            name = txt_name.value
            page.clean()
            page.add(Text(f"Oi, {name}!"))

    txt_name = TextField(label="Nome completo")

    page.add(txt_name, ElevatedButton("CADASTRAR", on_click=btn_click))

flet.app(target=main)
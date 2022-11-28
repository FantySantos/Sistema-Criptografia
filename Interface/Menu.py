def linha(tam=42):
    return '-' * tam

def cabecalho(txt):
    print(linha())
    print(txt.center(42))
    print(linha())

def leiaint(msg):
    while True:
        try:
            n = int(input(msg))
        except (ValueError, TypeError, KeyboardInterrupt):
            print('\n\033[31mERRO: Por favor, digite um número  válido.\033[m')
        else:
            return n

def menu(nome, op):
    cabecalho(nome)
    for idx, item in enumerate(op):
        print(f'\033[33m[{idx+1}]\033[m \033[34m{item}.\033[m')
    print(linha())
    opc = leiaint('\033[32mSua opção: \033[m')
    return opc
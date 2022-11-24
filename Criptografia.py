from Crypto.Cipher import AES
from secrets import token_bytes
from base64 import b64encode, b64decode

# key = token_bytes(16)
key = b'5\x1c\xa1\xe7\\:\xfb\x12_\x8b13\x12\xc9\xf7h'

def encrypt(mensagem):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(mensagem.encode())
    return ciphertext, nonce+tag

def decrypt(ciphertext, nonce_tag):
    cipher = AES.new(key, AES.MODE_EAX, nonce_tag[0:16])
    plaintext = cipher.decrypt_and_verify(ciphertext, nonce_tag[16:])
    return plaintext.decode()

def run_encrypt():
    ciphertext, nonce_tag = encrypt(input('\nInsira a mensagem: '))
    ciphertext = b64encode(ciphertext).decode('utf-8')
    nonce_tag =  b64encode(nonce_tag).decode('utf-8')
    print(f'\nTexto criptografado: {ciphertext}\nChave: {nonce_tag}')

def run_decrypt():
    ciphertext = b64decode(input('\nDigite a mensagem criptografada: '))
    nonce_tag = b64decode(input('\nDigite a chave: '))
    plaintext = decrypt(ciphertext, nonce_tag)
    if not plaintext:
        print('\nMensagem comrrompida.')
    else:
        print(f'\nTexto descriptografado: {plaintext}')

def menu():
    return input('''
    [1] Criptografar.
    [2] Descriptografar.
    [3] Sair.

    Escolha sua opção: ''')

def controle_menu():
    controle = menu()
    while controle != '3':
        if controle == '1':
            run_encrypt()
        elif controle == '2':
            run_decrypt()
        else:
            print('\nOpção inválida.')
        controle = menu()
    print('\nPrograma finalizado!')

controle_menu()
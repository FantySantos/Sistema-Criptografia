from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from Interface.Menu import cabecalho

def encrypt(mensagem, key):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(mensagem.encode())
    return ciphertext, key+nonce+tag

def decrypt(ciphertext, key_nonce_tag):
    cipher = AES.new(key_nonce_tag[0:16], AES.MODE_EAX, key_nonce_tag[16:32])
    plaintext = cipher.decrypt_and_verify(ciphertext, key_nonce_tag[32:])
    return plaintext.decode()

def run_encrypt(key):
    ciphertext, key_nonce_tag = encrypt(input('\n\033[32mInsira a mensagem: \033[m'), key)
    ciphertext = b64encode(ciphertext).decode()
    key_nonce_tag =  b64encode(key_nonce_tag).decode()
    cabecalho('Texto Criptografado')
    print(f'\033[36m{ciphertext}\033[m')
    cabecalho('Chave')
    print(f'\033[36m{key_nonce_tag}\033[m')

def run_decrypt():
    ciphertext = b64decode(input('\n\033[32mDigite a mensagem criptografada: \033[m'))
    key_nonce_tag = b64decode(input('\033[32mDigite a chave: \033[m'))
    plaintext = decrypt(ciphertext, key_nonce_tag)
    if not plaintext:
        print('\n\033[31mMensagem comrrompida.\033[m')
    else:
        cabecalho('Texto Descriptografado')
        print(f'\033[36m{plaintext}\033[m')
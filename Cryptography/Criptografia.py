from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from Crypto.Util.Padding import pad, unpad

def encrypt(mensagem, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext_bytes = cipher.encrypt(pad(mensagem.encode(), AES.block_size))
    iv = cipher.iv
    return ciphertext_bytes, iv+key

def decrypt(ciphertext, iv_key):
    cipher = AES.new(iv_key[16:], AES.MODE_CBC, iv_key[0:16])
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode()

def run_encrypt(mensagem, key):
    ciphertext, iv_key = encrypt(mensagem, key)
    ciphertext = b64encode(ciphertext).decode()
    iv_key =  b64encode(iv_key).decode()
    return ciphertext, iv_key

def run_decrypt(ciphertext_b64, iv_key_b64):
    try:
        ciphertext = b64decode(ciphertext_b64)
        iv_key = b64decode(iv_key_b64)
        plaintext = decrypt(ciphertext, iv_key)
        return plaintext

    except (ValueError, KeyError):
        return ''
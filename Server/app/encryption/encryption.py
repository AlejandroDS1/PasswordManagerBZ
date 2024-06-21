from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os

# Derivar clave desde la contraseña maestra
def derive_key(master_password: str, salt : bytes = None) -> (bytes, bytes):
    '''
        Hash the users password using the master_password.
        returns: key, salt
    '''

    if not salt: salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = kdf.derive(master_password.encode('utf-8'))
    return key, salt  # TODO retorna / almacena salt

# Encriptar una contraseña
def encrypt_password(plaintext_password: str, key: bytes) -> (bytes, bytes):
    chacha = ChaCha20Poly1305(key)
    nonce = os.urandom(12)
    ciphertext = chacha.encrypt(nonce, plaintext_password.encode('utf-8'), None)
    return nonce, ciphertext

# Desencriptar una contraseña
def decrypt_password(nonce : bytes, data: bytes, key: bytes) -> str:
    chacha = ChaCha20Poly1305(key)
    plaintext_password = chacha.decrypt(nonce, data, None)
    return plaintext_password.decode('utf-8') # TODO retorna nonce
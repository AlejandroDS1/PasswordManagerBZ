from app.encryption.encryption import (
    derive_key,
    decrypt_password,
    encrypt_password as enc_password
)

from sqlalchemy import select

from app.models.user import User
from app.models.db import db
from app.models.passwords import Password, PasswordCreate

def create_password(master_password : str) -> (bytes, bytes):
    '''
        returns hashed_password, salt
    '''
    return derive_key(master_password)

def check_password(users_password : str, hashed_password : bytes, salt : bytes) -> bool:
    return derive_key(users_password, salt=salt)[0] == hashed_password

def encrypt_password(password : PasswordCreate, user : User) -> None:
    '''
        Encrypts a password and stores it in db.
    '''
    nonce, hash_psswd = enc_password(password.password, user.hashed_password)

    psswd : Password = Password(nonce=nonce, encrypted_password=hash_psswd, user_id=user.id, title=password.title, website=password.website)

    psswd = Password.model_validate(psswd)
    
    db.add(psswd)
    db.commit()

def decrypt_users_passwords(user : User) -> list[str]:

    passwords = db.exec(select(Password).where(Password.user_id == user.id))

    # Por cada password que tenga el usuario vamos desencriptandolas.
    decrypted_passwords = []
    for psswd in passwords:
        psswd : Password = psswd[0]
        decrypted_passwords.append(decrypt_password(psswd.nonce, psswd.encrypted_password, key=user.hashed_password))

    return decrypted_passwords
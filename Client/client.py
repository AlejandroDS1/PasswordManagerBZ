from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from base64 import b64encode

import requests
req = requests.get("http://localhost:5000/public_key")

public_key = '\n' +  dict(req.json())['public_key'] # Add \n to avoid error

DATA= {"email": "test@test.com", "username": "Alejandro Cantero", "password" : "Si", "public_key": "algo"}

public_key = serialization.load_pem_public_key(
            data=public_key.encode(),
            backend=default_backend()
        )

password = 'Testing password # - ()!\'"·'.replace(r'"', r'\"') # replace the " to \"

DATA["password"] = password
enc = public_key.encrypt(
    str(DATA).encode("utf-16"),
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

encrypted_message_base64 = b64encode(enc).decode('utf-8')

# DATA["password"] = encrypted_message_base64


print(f"Vamos a enviar: {str(DATA)}")

msj = requests.post("http://localhost:5000/register", 
                    data=encrypted_message_base64,
                    headers={"Content-type": "application/json", "Accept" : "application/json"})

print(msj.text)

"""
# Generar clave privada del servidor
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=4096
)

pem_private_key = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,  # o PrivateFormat.PKCS8
    encryption_algorithm=serialization.NoEncryption()  # O utiliza BestAvailableEncryption(b"password") para cifrar
)

# Serializar la clave pública a formato PEM
pem_public_key = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

"""
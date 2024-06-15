import socket
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
    s.connect(('127.0.0.1', 65432))

    msj = s.recv(4096)

    print(f"Clave publica {msj}")

    MSJ = "Esto es lo que deberia poder desencriptar el"

    encr = serialization.load_pem_public_key(msj).encrypt(MSJ.encode(), 
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
        ))

    s.sendall(encr)

    print(f"MSJ encriptado: {encr}")
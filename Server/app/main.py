from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

# Generar clave privada del servidor
server_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=4096
)

# Clave publica a compartir.
server_public_key = server_private_key.public_key()


# Test init socket
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.bind(('127.0.0.1', 65432))

    s.listen(1)

    conn, addr = s.accept()

    conn.sendall(server_public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

    mensaje = conn.recv(4096)

    print(f"Mensaje encriptado {mensaje}")

    decripted = server_private_key.decrypt(
        mensaje,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
    ))

    print(f"desencripted: {decripted}")

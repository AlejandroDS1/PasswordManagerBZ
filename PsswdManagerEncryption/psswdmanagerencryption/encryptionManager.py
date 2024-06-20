from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

from dotenv import get_key

PRIVATE_KEY = None # Object to decrypy users conversation
PUBLIC_KEY : str = None # Key to share with client

# Generate pair private-public key if does not exists
def generate_private_key(): # TODO
    server_private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096
    )

    pem_private_key = server_private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,  # o PrivateFormat.PKCS8
        encryption_algorithm=serialization.NoEncryption()  # O utiliza BestAvailableEncryption(b'password') para cifrar
    )
    

    # Obtener la clave pública del servidor
    server_public_key = server_private_key.public_key()

    # Serializar la clave pública a formato PEM
    pem_public_key = server_public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return pem_private_key


def get_public_key_pem(*env_path : str) -> str:

    global PUBLIC_KEY
    # TODO: Control de errores. Puede que no exista la calve publica en el .env (crearla, try)
    if not PUBLIC_KEY and env_path: 
        PUBLIC_KEY = get_key(dotenv_path=env_path, key_to_get="PUBLIC_KEY")
    
    return PUBLIC_KEY

def get_private_key(*env_path : str):

    global PRIVATE_KEY
    # TODO: Control de errores. Puede que no exista la calve en el .env (crearla, try)
    if not PRIVATE_KEY and env_path:
        PRIVATE_KEY = serialization.load_pem_private_key(
            get_key(dotenv_path=env_path, key_to_get="PRIVATE_KEY"),
            password=None,
        )

    return PRIVATE_KEY

def decrypt(msj : bytes) -> str:
    get_private_key()

    unencrypted = PRIVATE_KEY.decrypt(
        msj,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return unencrypted.decode()


""" API with FLASK"""
import json
from flask import (
    Flask,
    request, 
    jsonify,
    session
)
from app.models.passwords import PasswordCreate
from app.models.db import db
from app.models.user import User, create_user, ErrorCode_DATA
from app.config import get_env_file

from sqlmodel import select

from secrets import token_hex # Generate random token
#from psswdmanagerencryption.encryptionManager import get_public_key_pem, decrypt #, setkeys

from app.encryption.encryptionManager import *

app = Flask(__name__)
app.secret_key = token_hex()

#setkeys(get_env_file())

@app.route("/login")
def login():
    # TODO: Maybe implementar session
    users = db.exec(select(User)).all()

    jsonUsers = [user.toDict() for user in users]

    return {"Users": jsonUsers, "msj" : "Dummy Method"}

@app.route("/register", methods=["POST"])
def register():
    
    # If no data has been sent, return Bad Request
    if not request.json:
        return {"msj" : "json not recived, json must include the following fields [email, username, password]."}, 400

    data = request.json

    # Check if all the fields are filled
    if "email" not in data or \
       "username" not in data or \
       "password" not in data:
        return {"msj" : "There is a field missing, fields must be [email, username, password, public_key]."}, 400

    # Create user in data base
    user = create_user(db, data)

    # TODO mejorar codigo de estado o mensaje personalizado
    if not isinstance(user, User): return {"msj": user.value}, 400 # If object is not created send err msj

    return {"user" : user.toDict(), "msj" : f"User created succesfully [Username : {user.name}] |  [Email: {user.email}]"}, 200

    # TODO Finalmente devuelve un token entre otras cosas -> https://flask.palletsprojects.com/en/3.0.x/quickstart/#sessions

@app.route("/password/get", methods=["GET", "POST"])
def getPasswords():
    '''
    Returns the selected passwords to the users.
    TODO
    For Client porpuses, will be posible to select by id.
    Normal user probably is going to select by title
    '''

    # TODO: GET method only for sessions.
    # At the moment shows all
    if request.method == "GET":
        user : User = db.exec(select(User)).one()[0]

        passwords = db.exec(select(Password).where(Password.user_id == user.id))

        allPswd = []

        for i in passwords:
            i : Password = i[0]
            iD = i.toDict()

            iD["password"] = decrypt_password(i.nonce, i.encrypted_password, user.hashed_password)
            allPswd.append(str(iD))

        return jsonify({"User" : user.name, "Passwords" : str(allPswd)})
    
    # POST method will require autentication, meaning email and password

    if not request.json: return {"msj" : "User not autenticated!"}, 400

    auth = request.json

    if "email" not in auth or "password" not in auth: return {"msj": "Field missing, fields must be [email, password]"}, 400

    user : User = db.exec(select(User).where(User.email == auth["email"])).one()[0]

    if not check_password(auth["password"], user.hashed_password, user.salt): return {"msj" : "Password incorrect"}, 400

    passwords = db.exec(select(Password).where(Password.user_id == user.id))

    allPswd = []

    for i in passwords:
        i : Password = i[0]
        iD = i.toDict()

        iD["password"] = decrypt_password(i.nonce, i.encrypted_password, user.hashed_password)
        allPswd.append(str(iD))

    return jsonify({"User" : user.name, "Passwords" : str(allPswd)})

@app.route("/password/create", methods=["POST"])
def create_password():

    '''
    TODO Create extense json data to recive
    {
        password:{
            password: str "password to encrypt and store"
            title : str | None "Tile of the password"
            website : str | None  "Website of the password"
        }

        user : {
            email : str "Email that belongs to the user"
            master_password: str "master_password of users account"
        }
    }
    '''
    if not request.json: return {"msj" : "No content recived, data must be format json and must include [password], optionals: [title, website]"}, 400

    data = request.json

    if "password" not in data: return {"msj" : "Json must include password field"}, 400

    # TODO extends json....
    if "email" not in data or "master_password" not in data: return {"msj" : "user credentials needed"}, 400

    # Check optional parameters
    if "title" not in data: data["title"] = None
    if "website" not in data: data["website"] = None

    user = db.exec(select(User).where(User.email == data["email"])).one()[0]

    encrypt_password(password=PasswordCreate(password=data["password"], title=data["title"], website=data["website"]), user=user)

    return {"msj" : "Password stored succesfully!"}
""" API with FLASK"""
import json
from flask import (
    Flask,
    request, 
    jsonify,
    session
)
from app.models.db import db
from app.models.user import User, create_user, ErrorCode_DATA
from app.config import get_env_file

from sqlmodel import select

from secrets import token_hex # Generate random token
from psswdmanagerencryption.encryptionManager import get_public_key_pem, decrypt #, setkeys

app = Flask(__name__)
app.secret_key = token_hex()

#setkeys(get_env_file())

@app.route("/login")
def login():
    
    users = db.exec(select(User)).all()

    jsonUsers = [user.toDict() for user in users]

    return {"Users": jsonUsers}


@app.route("/register", methods=["POST"])
def register():

    try:    
        print(f"[DATA : ] {str(request.data)}")
    except: print("[DATA failed]")

    # If no data has been sent, return Bad Request
    if not request.data:
        return {"msj" : "No Data"}, 400

    data = decrypt(request.data)

    # Process data to parse json
    data = data.replace("'", r'"').replace("\\\\", "\\")

    print(f"El mensaje es:  {data}")

    data = json.loads(data)

    print(f"password:  {data['password']}")

    # Check if all the fields are filled
    if "email" not in data or \
       "username" not in data or \
       "password" not in data or \
       "public_key" not in data:
        return {"msj" : "There is a field missing, fields must be [email, username, password, public_key]."}

    # Create user in data base
    user = create_user(db, data)

    # TODO mejorar codigo de estado o mensaje personalizado
    if not isinstance(user, User): return {"msj": user.value}, 400 # If object is not created send err msj

    return {"user" : user.toDict(), "msj" : "User created succesfully"}, 200

    # TODO Finalmente devuelve un token entre otras cosas -> https://flask.palletsprojects.com/en/3.0.x/quickstart/#sessions


@app.route("/public_key", methods=["POST"])
def share_keys():
    
    """
    With this methods, Server will send its public key to user

    This is the only method who is not encrypted.
    """

    session['username'] = "Alejandro"
    print(f"session {str(session)}, username: {session['username']}")
    
    print(f"json = {request.data}")

    return "Working"
    #return jsonify({"public_key" : get_public_key_pem()})

@app.route("/a", methods=["GET"])
def a():
    
    print(f"session: {str(session)}")

    if 'username' in session:
        return f"Logged + {session['username']} + \n Key = {app.secret_key}"
        
    return "Not logged !!"

# if __name__ == "__main__":
#      app.run(host='0.0.0.0', port=443, ssl_context=('../cert.pem', '../key.pem'))

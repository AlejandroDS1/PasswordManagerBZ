""" API with FLASK"""
from flask import Flask, request, jsonify
from app.models.db import db
from app.models.user import User, create_user
from sqlmodel import select

app = Flask(__name__)

@app.route("/login")
def login():
    
    users = db.exec(select(User)).all()

    jsonUsers = [user.toDict() for user in users]

    return {"Users": jsonUsers}


@app.route("/register", methods=["POST"])
def register():

    data = request.json

    # If no data has been sent, return Bad Request
    if not data:
        return {"msj" : "No Data"}, 400

    # Check if all the fields are filled
    if "email" not in data or \
       "username" not in data or \
       "password" not in data or \
       "public_key" not in data:
        return {"msj" : "There is a field missing, fields must be [email, username, password, public_key]."}

    # Create user in data base
    user = create_user(db, data)

    return {"user" : user.toDict()}    

    # TODO Finalmente devuelve un token entre otras cosas -> https://flask.palletsprojects.com/en/3.0.x/quickstart/#sessions
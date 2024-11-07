from . import db

import bcrypt
import re

_accounts = db["accounts"]

def find_account(username: str) -> dict:
    return _accounts.find_one({'username': username}, {'_id': False})

def find_account_by_email(email: str) -> dict:
    return _accounts.find_one({'email': email}, {'_id': False})

def create_account(email: str, username: str, password: str) -> bool:
    if find_account(username) is not None:
        return False

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    _accounts.insert_one({
        'email': email,
        'username': username,
        'password': hashed,
    })
    
    return True
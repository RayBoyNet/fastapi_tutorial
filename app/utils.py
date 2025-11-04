from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()

def create_password_hash(password:str):
    return pwd_context.hash(password)

def verify_password_hash(password:str,password_hash:str):
    return pwd_context.verify(password,password_hash)

import keyring
import bcrypt
import getpass
import uuid

def pass_is_set():
    if keyring.get_password("system", "passman-salt") is None or \
                    keyring.get_password("system", "passman-cipher") is None or \
                    keyring.get_password("system", "passman-userkey") is None:
        return False
    else:
        return True

def set_password():
    keyring.set_password("system", "passman-salt", bcrypt.gensalt(12).decode('utf-8'))
    keyring.set_password("system", "passman-cipher", str(uuid.uuid4()).replace('-', ''))
    keyring.set_password("system", "passman-userkey", bcrypt.hashpw(str(getpass.getpass("Set access password: ")).encode('utf-8'),
                                                      keyring.get_password("system", "passman-salt").encode('utf-8')).decode('utf-8'))

def pass_is_correct(user_pass):
    if bcrypt.hashpw(user_pass.encode('utf-8'), keyring.get_password("system", "passman-userkey").encode("utf-8")).decode('utf-8') == \
                                                    keyring.get_password("system", "passman-userkey"):
        return True
    else:
        return False
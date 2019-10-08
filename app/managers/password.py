
from hashlib import sha1

def generate_hash_pass(username, password):
    hash = sha1()
    hash.update(b'%s:%s' % (str(username).encode().upper(), str(password).encode().upper()))
    return hash.hexdigest().upper()


def validate_hash_pass(username, password, hash):
    hash = sha1()
    hash.update(b'%s:%s' % (str(username).encode().upper(), str(password).encode().upper()))
    return hash.hexdigest().upper() == hash

    
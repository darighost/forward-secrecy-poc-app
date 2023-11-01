import random

def diffie_hellman(server_pub_key, p=17, g=3):
    # these values are cryptographically weak
    # used only for example
    secret_key = random.randint(10, 100)
    public_key = g ** secret_key % p # 6
    shared_secret = server_pub_key ** secret_key % p
    
    return public_key, shared_secret
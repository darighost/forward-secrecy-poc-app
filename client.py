import requests
import random
import argparse
import binascii
from Crypto.Cipher import AES
import sys

recipient = sys.argv[-1]

p = 17
g = 3
secret_key = random.randint(10, 100)
public_key = g ** secret_key % p # 6
r = requests.post(f'{recipient}/handshake', json={
    "p": p,
    "g": g,
    "key": public_key
})
shared_secret = int(r.text) ** secret_key % p
key = shared_secret.to_bytes(32)
cipher = AES.new(key, AES.MODE_EAX)
nonce = cipher.nonce
ciphertext = cipher.encrypt(bytes(input('> '), 'utf8'))
requests.post(f'{recipient}/notification', json={
    "message": binascii.hexlify(ciphertext).decode('utf-8'),
    "nonce": binascii.hexlify(nonce).decode('utf-8'),
})
from flask import Flask, request
import subprocess
from binascii import unhexlify as unhex
import random
from Crypto.Cipher import AES

app = Flask(__name__)

# 
pfs_session = {
    'secret': None
}

@app.route("/handshake", methods=["POST"])
def handshake():
    req = request.json
    print(dict(req))
    p = req['p']
    g = req['g']
    foreign_key = req['key']
    secret_key = random.randint(10, 100)
    pubkey = g ** secret_key % p # 6
    shared_secret = foreign_key ** secret_key % p
    pfs_session['secret'] = shared_secret
    print(shared_secret)
    return str(pubkey), 200

@app.route("/notification", methods=["POST"])
def notification():
    ciphertext = unhex(request.json['message'])
    nonce = unhex(request.json['nonce'])
    key = pfs_session['secret'].to_bytes(32)
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    msg = cipher.decrypt(ciphertext).decode("utf-8")
    subprocess.run([
        "osascript", 
        "-e", 
        f'display notification "{msg}" with title "Alert"'])
    return "ok", 200

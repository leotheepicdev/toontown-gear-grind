# Python implementation of Fernet because cryptography is being a pain in the ass.

import base64, binascii, hmac, time, os, struct
from .FernetGlobals import *
from pyaes import AESModeOfOperationCBC, Encrypter, Decrypter

def b64decodeKey(key):
    # Check if our key is bytes
    if not isinstance(key, bytes):
        raise TypeError('Key must be bytes.')
    # Check if our key is its proper length
    key = base64.urlsafe_b64decode(key)
    if len(key) != MAX_KEY_LENGTH:
        raise ValueError("Fernet key must be {0} url-safe base64-encoded bytes.".format(MAX_KEY_LENGTH))
    return key

def b64DecryptToken(token):
    try:
        data = base64.urlsafe_b64decode(token)
    except (TypeError, binascii.Error):
        raise Exception('Invalid Token.')
    if not data or data[0] != 0x80:
        raise Exception('Invalid Token.')
    return data
    
def retrieveTimestamp(data):
    try:
        timestamp, = struct.unpack(">Q", data[1:9])
    except struct.error:
        raise Exception('Invalid Token.')

def checkForValidTime(timestamp, ttl, currentTime):
    if ttl != None:
        if timestamp + ttl < currentTime or currentTime + MAX_CLOCK_SKEW < timestamp:
            raise Exception('Invalid Token.')
            
def hmacDecrypt(signingKey, data):
    h = hmac.new(signingKey, digestmod='sha256')
    h.update(data[:-32])
    if not hmac.compare_digest(h.digest(), data[-32:]):
        raise Exception('Invalid Token.')   

class Fernet:

    def __init__(self, key):
        key = b64decodeKey(key)
        
        # Half of our key is our signingKey, the other half is our encryptionKey
        self.signingKey = key[:HALF_KEY_LENGTH]
        self.encryptionKey = key[HALF_KEY_LENGTH:]

    def encrypt(self, data):
        currentTime = int(time.time())
        iv = os.urandom(16)
        return self.encryptFromParts(data, currentTime, iv)

    def encryptFromParts(self, data, currentTime, iv):
        encrypter = Encrypter(AESModeOfOperationCBC(self.encryptionKey, iv))
        ciphertext = encrypter.feed(data)
        ciphertext += encrypter.feed()
        basicParts = (b"\x80" + struct.pack(">Q", currentTime) + iv + ciphertext)
        h = hmac.new(self.signingKey, digestmod='sha256')
        h.update(basicParts)
        return base64.urlsafe_b64encode(basicParts + h.digest())

    def decrypt(self, token, ttl=None):
        if not isinstance(token, bytes):
            raise TypeError("Token must be bytes.")
            
        currentTime = int(time.time())
        data = b64DecryptToken(token)

        # Is our timestamp valid?
        timestamp = retrieveTimestamp(data)
        checkForValidTime(timestamp, ttl, currentTime)

        # Is our hmac valid?
        hmacDecrypt(self.signingKey, data)

        iv = data[9:25]
        ciphertext = data[25:-32]
        decryptor = Decrypter(AESModeOfOperationCBC(self.encryptionKey, iv))

        try:
            plaintext = decryptor.feed(ciphertext)
            plaintext += decryptor.feed()
        except ValueError:
            raise Exception('Invalid Token.')
            
        return plaintext
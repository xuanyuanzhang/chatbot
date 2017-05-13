import os
from Crypto.Cipher import AES
import hashlib

key = hashlib.sha256("abcdefghijklmnop".encode()).digest()

def EncodeAES(raw):
    iv = os.urandom(16)
    cipher = AES.new( key, AES.MODE_CFB, iv )
    return iv + cipher.encrypt( raw ) 

def DecodeAES(enc):
    iv = enc[:16]
    if not len(iv) == 16:
        return None
    cipher = AES.new(key, AES.MODE_CFB, iv )
    return cipher.decrypt( enc[16:] )

if __name__ == '__main__':
    message = 'This is a message of no particular length.'
    ciphertext = EncodeAES(message)
    print 'Ciphertext: %s' %(ciphertext,)
    text = DecodeAES(ciphertext)
    print 'Decoded: %s' %(text,)
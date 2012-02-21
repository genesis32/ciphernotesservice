#!/usr/bin/env python

from ctypes import *
import base64

cncrypto = CDLL('libcncrypto.so')

aeskey = create_string_buffer('\000' * 256)
cncrypto.generate_aeskey(aeskey, 256)
print "AES Key:",base64.b64encode(aeskey)
print ""

plaintext = create_string_buffer('test')

ciphertext = create_string_buffer('\000' * 512)
ctlen = c_int() 
cncrypto.aes_encrypt(aeskey, plaintext, byref(ciphertext), byref(ctlen))
print "AES ciphertext ", base64.b64encode(ciphertext[0:ctlen.value])
print ""

decryptedpt = create_string_buffer('\000' * 512)
ptlen = c_int()
cncrypto.aes_decrypt(aeskey, ciphertext, ctlen.value, byref(decryptedpt), byref(ptlen)) 
print "AES plaintext", decryptedpt[0:ptlen.value]
print ""

with open('pubkey.pem') as f:
    key = f.read()
    plaintext = create_string_buffer('test')
    ciphertext = create_string_buffer('\000' * 512)
    ctlen = c_int() 
    cncrypto.rsa_encrypt(key, plaintext, byref(ciphertext), byref(ctlen))
    print "RSA ciphertext", base64.b64encode(ciphertext[0:ctlen.value])


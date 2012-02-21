from ctypes import *
from django.conf import settings
import base64

def aes_encrypt_authcode(authcode):
    cncrypto = CDLL(settings.CNCRYPTO_LIB)

    aeskey = create_string_buffer('\000' * 256)
    cncrypto.generate_aeskey(aeskey, 256)

    plaintext = create_string_buffer(authcode)

    ciphertext = create_string_buffer('\000' * 1024)
    ctlen = c_int() 

    cncrypto.aes_encrypt(aeskey, plaintext, byref(ciphertext), byref(ctlen))

    return base64.b64encode(aeskey), base64.b64encode(ciphertext[0:ctlen.value])


def rsa_encrypt_aeskey(pubkeypem, aeskey):
    print pubkeypem, aeskey
    cncrypto = CDLL(settings.CNCRYPTO_LIB)

    c_plaintext = create_string_buffer(aeskey)
    c_pubkeypem = create_string_buffer(pubkeypem)

    ciphertext = create_string_buffer('\000' * 1024)
    ctlen = c_int()

    cncrypto.rsa_encrypt(c_pubkeypem, c_plaintext, byref(ciphertext), byref(ctlen))

    return base64.b64encode(ciphertext[0:ctlen.value])


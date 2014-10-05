# noinspection PyPackageRequirements
from Crypto.Cipher import AES
import base64

#AES256
BLOCK_SIZE = 32
PADDING = '{'
DECRYPTION_CHECK = "|PASSMON|"

def aes_encrypt(word, key):
	"""Encrypts password"""
	pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
	encode_aes = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
	cipher = AES.new(key)
	encoded = encode_aes(cipher, DECRYPTION_CHECK + str(word))
	return encoded

def aes_decrypt(encrypted_string, key):
    """Decrypts password"""
    try:
        decode_aes = lambda c, e: c.decrypt(base64.b64decode(e)).decode('utf-8').rstrip(PADDING)
        cipher = AES.new(key)
        decoded = decode_aes(cipher, encrypted_string)
        if decoded[0:int(len(DECRYPTION_CHECK))] == DECRYPTION_CHECK:
            return decoded[len(DECRYPTION_CHECK):len(decoded)]
        else:
            return "Wrong Cipher"
    except:
        return "Cipher needs to be 32 bytes long"

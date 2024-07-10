from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os

# Parameter für den Key-Derivation-Function (KDF)
KDF_SALT = b'\x00'*16
KDF_ITERATIONS = 100000

def derive_key(password):
    """Erzeugt einen Schlüssel aus dem Passwort"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=KDF_SALT,
        iterations=KDF_ITERATIONS,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt(data, password):
    """Verschlüsselt die Daten mit dem angegebenen Passwort"""
    key = derive_key(password)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Padding der Daten
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()

    encrypted_data = iv + encryptor.update(padded_data) + encryptor.finalize()
    return encrypted_data

def decrypt(encrypted_data, password):
    """Entschlüsselt die Daten mit dem angegebenen Passwort"""
    key = derive_key(password)
    iv = encrypted_data[:16]
    encrypted_data = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Entfernen des Paddings
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()

    return data

#!/usr/bin/env python3
"""Clipper – tiny CLI clipboard helper with optional encryption.

Usage:
    clipper [-e|-d] "text"
    -e : encrypt before copying (prompts for password)
    -d : decrypt current clipboard content (prompts for password)
    without flags copies the plain text.
"""
import argparse, sys, getpass, os

try:
    import pyperclip
except ImportError:
    sys.stderr.write('pyperclip not found. Run setup.sh first.\n')
    sys.exit(1)

try:
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    import base64
except ImportError:
    sys.stderr.write('cryptography not found. Run setup.sh first.\n')
    sys.exit(1)

backend = default_backend()

def _derive_key(password: bytes, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=backend,
    )
    return kdf.derive(password)

def encrypt(plaintext: str, password: str) -> str:
    salt = os.urandom(16)
    key = _derive_key(password.encode(), salt)
    iv = os.urandom(12)
    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv),
        backend=backend,
    ).encryptor()
    ct = encryptor.update(plaintext.encode()) + encryptor.finalize()
    data = b"|".join([
        base64.b64encode(salt),
        base64.b64encode(iv),
        base64.b64encode(ct),
        base64.b64encode(encryptor.tag),
    ])
    return data.decode()

def decrypt(ciphertext: str, password: str) -> str:
    try:
        salt_b, iv_b, ct_b, tag_b = ciphertext.split('|')
    except ValueError:
        raise ValueError('Malformed encrypted data')
    salt, iv, ct, tag = map(base64.b64decode, (salt_b, iv_b, ct_b, tag_b))
    key = _derive_key(password.encode(), salt)
    decryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv, tag),
        backend=backend,
    ).decryptor()
    pt = decryptor.update(ct) + decryptor.finalize()
    return pt.decode()

def main():
    parser = argparse.ArgumentParser(description='Clipper – clipboard helper')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-e', '--encrypt', action='store_true', help='encrypt before copying')
    group.add_argument('-d', '--decrypt', action='store_true', help='decrypt clipboard content')
    parser.add_argument('text', nargs='?', help='text to copy (ignored with --decrypt)')
    args = parser.parse_args()

    if args.decrypt:
        cipher = pyperclip.paste()
        pwd = getpass.getpass('Password: ')
        try:
            plain = decrypt(cipher, pwd)
        except Exception as exc:
            sys.stderr.write(f'Decryption failed: {exc}\n')
            sys.exit(1)
        pyperclip.copy(plain)
        print('Clipboard decrypted and replaced with plain text.')
        return

    if args.text is None:
        parser.print_help()
        sys.exit(1)

    data = args.text
    if args.encrypt:
        pwd = getpass.getpass('Password: ')
        data = encrypt(data, pwd)
    pyperclip.copy(data)
    print('Text copied to clipboard.')

if __name__ == '__main__':
    main()

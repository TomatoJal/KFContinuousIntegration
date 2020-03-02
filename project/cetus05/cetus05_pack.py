from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

cipher = Cipher(
    algorithms.AES(bytes.fromhex('0C8823438360CB78002B04D1C3680C88')),
    modes.ECB(),
    backend=default_backend()
)

decryptor = cipher.decryptor()
encryptor = cipher.encryptor()


message = encryptor.update(bytes.fromhex('FF8E0365FF01FFFF'))
print(message.hex().upper())
message = decryptor.update(message)
print(message.hex().upper())


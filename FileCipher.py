import os, struct
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

class AESCipher(object):

    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, in_filename, out_filename=None, chunksize=64*1024):

        if not out_filename:
            out_filename = in_filename + '.crypt'

        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        filesize = os.path.getsize(in_filename)

        with open(in_filename, 'rb') as infile:
            with open(out_filename, 'wb') as outfile:
                outfile.write(struct.pack('<Q', filesize))
                outfile.write(iv)
                #test
                outfile.write(cipher.encrypt(self.key))

                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += b' ' * (16 - len(chunk) % 16)

                    outfile.write(cipher.encrypt(chunk))

        os.remove(in_filename)

    def decrypt(self, in_filename, out_filename=None, chunksize=24*1024):

        if not out_filename:
            out_filename = os.path.splitext(in_filename)[0]

        with open(in_filename, 'rb') as infile:
            origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
            iv = infile.read(16)
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            key = infile.read(self.bs)
            key = cipher.decrypt(key)
            if key != self.key:
                raise WrongKey('Dat not di right key mon!')

            with open(out_filename, 'wb') as outfile:
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    outfile.write(cipher.decrypt(chunk))

                outfile.truncate(origsize)

        os.system('"%s"' % out_filename)
        self.encrypt(out_filename)

class WrongKey(Exception):
    pass
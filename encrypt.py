# coding=UTF-8
import AESCipher
import sys, os, getpass
import subprocess as sp

class WrongKey(Exception):
    pass

class AlreadyEncrypted(Exception):
    pass

class AlreadyDecrypted(Exception):
    pass

class NotProperOP(Exception):
    pass

class EncryptionNotWanted(Exception):
    pass

def sysarg(i):
    try:
        return sys.argv[i]
    except:
        return None

INPUT_OP = sysarg(1)
INPUT_FILE = sysarg(2)
INPUT_KEY = sysarg(3)

def encrypt(key, data):
    #TODO: Man skulle kuunna pröva dekryptera här och om det går
    #TODO: meddela att filen redan är krypterad och fråga om vill forts.
    #TODO: MEN!! det går förståss bara om man försöker krypter med samma lsn
    #TODO: Potentiellt också en onödig funktion
    #TODO: Ksnk finns andra sätt att kolla om fil är krypterad
    #TODO: Egentligen är det felaktig använding av programmet då det inte är tänkt
    #TODO: Som ett cmd program längre

    # if key is 0 this will fail
    key_chk = 0
    while key_chk != key:
        while not key:
            key = input('Provide password for decryption: ')
            if not key: print('Password can not be empty.')
        key_chk = input('Please Confirm password: ')

    cipher = AESCipher.AESCipher(key)
    print('About to encrypt file: %s' % INPUT_FILE)
    k = input('press y to continue or any other key to abort: ')
    if k.lower() == 'y':
        return cipher.encrypt(data).decode("utf-8"), key
    else:
        raise EncryptionNotWanted("Encrytpion aborted, WHY U CHNG UR MIND FOOL???.")

def decrypt(key, data):

    while not key:
        key = input('Provide password for decryption: ')

    cipher = AESCipher.AESCipher(key)

    try:
        result = cipher.decrypt(str.encode(data))
    except:
        raise AlreadyDecrypted('This file is already decrypted')
    else:
        if not result:
            print("The password is incorrect, pls try agn: ")
            return decrypt(None, data)
        else:
            return result, key

do = {'-e':encrypt, '-d': decrypt}

def main():

    if not INPUT_OP in do:
        print('No proper MO flag, please use -e or -d. Aborting.')
        return

    if not os.path.isfile(INPUT_FILE):
        print('%s does not appear to be a valid file. Aborting.' % INPUT_FILE)
        return
    elif INPUT_OP == '-d':
        file_name, ext = os.path.splitext(INPUT_FILE)
        if ext != '.crpt':
            print('Not a valid CryptIt-file. Aborting')
            return

    with open (INPUT_FILE, 'r') as f:
        data = f.read()
    try:
        # Asign tuple directly with var1, var2 = do()
        result = do[INPUT_OP](INPUT_KEY, data)
        encrypted = result[0]
        key = result[1]
    except Exception as e:
        print(str(e))
    else:
        if INPUT_OP == '-d':
            tmp_file = INPUT_FILE + '.tmp'
            with open (tmp_file, 'w+') as f:
                f.write(encrypted)
            programName = "notepad.exe"
            sp.Popen([programName, tmp_file]).wait()
            with open (tmp_file, 'r') as f:
                data = f.read()
            cipher = AESCipher.AESCipher(key)
            encrypted = cipher.encrypt(data).decode("utf-8")
            os.remove(tmp_file)
            output_file = INPUT_FILE
        elif INPUT_OP == '-e':
            os.remove(INPUT_FILE)
            output_file = INPUT_FILE + '.crpt'

        with open (output_file, 'w+') as f:
            f.write(encrypted)

if __name__ == '__main__':
    main()
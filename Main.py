# coding=utf-8
import FileCipher
import sys, os, getpass
#import subprocess as sp

def sysarg(i):
    try:
        return sys.argv[i]
    except:
        return None

INPUT_OP = sysarg(1)
INPUT_FILE = sysarg(2)
INPUT_KEY = sysarg(3)

def encrypt(key):

    # if key is 0 this will fail
    # TODO: make a better sol.
    key_chk = 0
    while key_chk != key:
        while not key:
            key = input('Provide password for encryption: ')
            if not key: print('Password can not be empty.')
        key_chk = input('Please Confirm password: ')

    print('About to encrypt file: %s' % INPUT_FILE)
    k = input('Confirm with y or press any other key to abort: ')
    if k.lower() == 'y':
        cipher = FileCipher.AESCipher(key)
        cipher.encrypt(INPUT_FILE)
        return key
    else:
        print("Encrytpion aborted, WHY U CHNG UR MIND FOOL???.")

def decrypt(key):

    while not key:
        key = input('Provide password for decryption: ')

    cipher = FileCipher.AESCipher(key)

    try:
        cipher.decrypt(INPUT_FILE)
    except FileCipher.WrongKey:
        print('wrong password, please try again')
        decrypt(None)
    else:
        return key

do = {'-e':encrypt, '-d': decrypt}

if __name__ == '__main__':

    if not INPUT_OP in do:
        print('No proper MO flag, please use -e or -d. Aborting.')
        sys.exit()

    if not INPUT_FILE:
        print('Please provide full path to a file')
        sys.exit()

    if not os.path.isfile(INPUT_FILE):
        print('%s does not appear to be a valid file. Aborting.' % INPUT_FILE)
        sys.exit()

    elif INPUT_OP == '-d':
        #file_name, ext = os.path.splitext(INPUT_FILE)
        if os.path.splitext(INPUT_FILE)[1] != '.crpt':
            print('Not a valid CryptIt-file. Aborting')
            sys.exit()

    key = do[INPUT_OP](INPUT_KEY)


import hashlib
import getpass
from tkinter import Tk

''' SECRET_KEY is a personal key to use as an extra salt that should be different for everyone.
Change this to some other sufficiently high-entropy string.
WARNING: Changing the secret key will generate completely different passwords, so do not change
it after you first set it unless you want to reset all of your passwords. '''
SECRET_KEY = "me1chioRsho3(k5s$S"

CLIPBOARD_FLAG = False     # Automated copying initially disabled
LENGTH = 16                # Length of generated passwords

ALPHABET = ('abcdefghijklmnopqrstuvwxyz'
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            '0123456789!@#$%^&*()-_')


''' Returns the raw hex of a salt+password combination'''


def get_hexdigest(salt, password):
    return hashlib.sha256((salt + password).encode('utf-8')).hexdigest()


''' Adds some extra salt'''


def genPassword(plaintext, service):
    salt = get_hexdigest(SECRET_KEY, service)
    hsh = get_hexdigest(salt, plaintext)
    return ''.join(salt + hsh)


''' Coverts the raw hex into a usable password.'''


def password(plaintext, service, length=LENGTH, alphabet=ALPHABET):

    # Converts the hexdigest into a decimal
    num = int(genPassword(plaintext, service), 16)

    # Determines the base that num will be converted to
    # Base-74 with the default alphabet
    num_chars = len(alphabet)

    # Generates a password by character, using numbers and math and things
    chars = []
    while len(chars) < length:
        num, rem = divmod(num, num_chars)
        chars.append(alphabet[rem])

    return ''.join(chars)


'''Copies a string to the clipboard using tkinter. This functionality is initially disabled
in the preferences for security reasons. '''


def to_clipboard(string_to_copy):
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.update()
    r.clipboard_append(string_to_copy)
    r.update()


def main():
    flag = True
    while flag:
        service = input(
            "Enter the service name and iteration, or 'exit' to stop: ")
        if service == 'exit':
            flag = False
            break
        service.replace(" ", "")
        master = getpass.getpass()
        print()
        pw = password(master, service)
        print(pw)
        if CLIPBOARD_FLAG:
            to_clipboard(pw)
            print("(Copied To Clipboard)" + '\n')


main()

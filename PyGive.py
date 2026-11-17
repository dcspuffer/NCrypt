import os
from cryptography.exceptions import InvalidTag # type: ignore
from cryptography.hazmat.primitives.ciphers.aead import AESGCM # type: ignore

#file giving back (decrypting) for files secured by PyGrab

KEY_NAME = "encrfile.key"
FUN = b"NCRYPT1"   #must match PyGrab
NONCE_SIZE = 12

#Looks for key(FUN) and decrypts only those with the same key
def decrypt_file(path, aesgcm):
    with open(path, "rb") as thefile:
        contents = thefile.read()

    if not contents.startswith(FUN):
        return False #finds any file not encrypted and branded by the PyGrab script false or unnecessary

    body = contents[len(FUN):]
    nonce, ciphertext = body[:NONCE_SIZE], body[NONCE_SIZE:]
    plaintext = aesgcm.decrypt(nonce, ciphertext, None) #gives back an Inval-tag on the wrong key/tampering

    #Writes to a temp file to write the readable one in case of a crash that would leave the files unreadable... Which wouldn't be good :(
    tmp_path = path + ".tmp"
    with open(tmp_path, "wb") as thefile:
        thefile.write(plaintext)
    os.replace(tmp_path, path)
    return True


def main(Desired_path=None):
    #Terminal: no folder given, so ask for one. PyGUI passes the folder in and skips the prompts.
    ask = Desired_path is None
    if ask:
        print("==========NCrypt Restore Software==========")
        print("This software will decrypt files secured by PyGrab in the directory you specify.")
        Desired_path = input("Please, enter the path to the directory you want to restore: ").strip().strip('"')

        if not os.path.isdir(Desired_path):
            print(f"'{Desired_path}' is not a directory.")
            input("Press Enter to exit.")
            return

    key_path = os.path.join(Desired_path, KEY_NAME)
    if not os.path.isfile(key_path):
        if not ask:
            print(f"No {KEY_NAME} found in {Desired_path}. Nothing was changed...")
            return
        key_path = input(f"No {KEY_NAME} found there. Enter the full path to the key file: ").strip().strip('"')
        if not os.path.isfile(key_path):
            print("Key file not found. Nothing was changed.")
            input("Press Enter to exit.")
            return

    with open(key_path, "rb") as key_file:
        aesgcm = AESGCM(key_file.read())

    restored = 0
    for file in os.listdir(Desired_path):
        path = os.path.join(Desired_path, file)
        if file == KEY_NAME or not os.path.isfile(path):
            continue
        try:
            if decrypt_file(path, aesgcm):
                restored += 1
                print(f"---{file} has been restored.---")
        except InvalidTag:
            print(f"!!! {file}: wrong key or file was modified. Left unchanged.")
        except OSError as e:
            print(f"!!! Could not restore {file}: {e}")

    print(f"Done. {restored} file(s) restored.")


if __name__ == "__main__":
    main()

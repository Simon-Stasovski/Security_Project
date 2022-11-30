text = input("prompt")
import sys
import hashlib

# print(sys.argv)

from wallet.wallet import Owner, Transaction
from simon import username as simon_username
from jacob import username as jacob_username
from chase import username as chase_username
from jacob import hash_pass as jacob_hash
from simon import hash_pass as simon_hash
from chase import hash_pass as chase_hash

array = [sys.argv[1], sys.argv[2]]
print(array)
while True:
    userArray = [simon_username, jacob_username, chase_username]
    userPass = [simon_hash, jacob_hash, chase_hash]

    prompt = input("Please enter Username")

    # Print the message digest
    containsUser = False
    index = -1
    for i in userArray:
        index += 1
        if array[0].lower() == i:
            containsUser = True

    if containsUser:
        print("Username Found")

    byte_input = array[1].encode()
    hash_pass = hashlib.sha256(byte_input)
    containsPass = False
    for j in userPass:
        if hash_pass == j:
            containsPass = True

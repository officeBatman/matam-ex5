import os
import json

ABC = ord('Z')-ord('A') + 1

"""
this function shifts a letter with cycling(a after z and vice versa)
Input: the character to shift, the amount  to shift and if the letter is uppercase
Output: the shifted letter
"""
def shiftLetter(char, amount, upper):
    letter_offset = ord('A') if upper else ord('a')
    return chr(((ord(char) - letter_offset + amount) % ABC) + letter_offset)


def getVigenereFromStr(key):
    key_arr = []
    for c in key:
        if c.isalpha():
            key_arr.append(ord(c) - (ord('A') if c.isupper() else ord('a')))
    return VigenereCipher(key_arr)


ENCRYPT_MODE = 1
DECRYPT_MODE = -1


class CaesarCipher:
    def __init__(self, key):
        self.key = key

    def useCipher(self, str, mode):
        result = ""
        for c in str:
            if c.isalpha():
                result += shiftLetter(c, mode * self.key, c.isupper())
            else:  # ignore if not a letter
                result += c
        return result

    def encrypt(self, str):
        return self.useCipher(str, ENCRYPT_MODE)

    def decrypt(self, str):#encrypt(M,K) = decrypt(M,-K)
        return self.useCipher(str, DECRYPT_MODE)


class VigenereCipher:
    def __init__(self, key):
        self.key = key

    def useCipher(self, str, mode):
        result = ""
        index = 0
        for c in str:
            if c.isalpha():
                result += shiftLetter(c, mode * self.key[index % len(self.key)], c.isupper())
                index += 1
            else:  # ignore if not a letter
                result += c
        return result

    def encrypt(self, str):
        return self.useCipher(str, ENCRYPT_MODE)

    def decrypt(self, str):#encrypt(M,K) = decrypt(M,-K)
        return self.useCipher(str, DECRYPT_MODE)


def setPathExtension(path, new_extension):
    return path[:path.rfind(".")] + new_extension


def newVigenereCipher(key):
    if isinstance(key, str):
        return getVigenereFromStr(key)
    return VigenereCipher(key)


def loadEncryptionSystem(dir_path):
    with open(dir_path + "/config.json") as file:
        data = json.load(file)

    encrypt_mode = (data["encrypt"] == "True")
    cipher = CaesarCipher(data["key"]) if data["type"] == "Caesar" else newVigenereCipher(data["key"])

    input_extension = '.txt' if encrypt_mode else '.enc'
    output_extension = '.enc' if encrypt_mode else '.txt'
    cipher_func = cipher.encrypt if encrypt_mode else cipher.decrypt

    for file_name in os.listdir(dir_path):
        if file_name.endswith(input_extension):
            file_path = dir_path + "/" + file_name

            with open(file_path, "r") as src:
                content = src.read()

            file_path = setPathExtension(file_path, output_extension)
            with open(file_path, "w") as dest:
                dest.write(cipher_func(content))


def main():
    loadEncryptionSystem("C:/temp")

if __name__ == '__main__':
    main()

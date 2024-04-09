# -*- coding:utf-8 -*-
import os
import os.path
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

class AES256:

    def __init__(self, key):
        self.key = key #key es lo que se usa para la conversion al encriptar y desencriptar.
        self.hash = SHA256.new()

    def pad(self, s):     
        return s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)

    def unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]

    def encrypt(self, message, key): 
        key = self.hash.digest() 

        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def encrypt_file(self, path,destiny = None):    
        with open(path, 'rb') as fo: # aqui abrimos el "path/archivo" como read binary.
            plaintext = fo.read() # hacemos que el "path/archivo" sea un texto plano
        
        self.hash.update(self.key) #Crear cadena de 32 bytes en hexadecimal
        key = self.hash.digest() 
        enc = self.encrypt(plaintext, key) # nos apoyamos en recursividad y encriptamos.     
        
        self.hash.update("AES256")
        codeEncrypt = self.hash.digest()

        if not os.path.exists(destiny):
        	os.mkdir(destiny)

        name = path.split("/").pop()
        with open(destiny + name + ".enc", 'wb') as fo: #aqui abrimos el "path/archivo" donde le ponemos la extension .enc y hacemos write binary
            fo.write(enc + key + codeEncrypt) #se reescribe el archivo existente
        os.remove(path) 


    def decrypt(self, ciphertext, key):
        iv = ciphertext[:16]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(ciphertext[16:]))

    def decrypt_file(self, path,destiny = None):
        with open(path, 'rb') as fo:
            ciphertext = fo.read()

        self.hash.update(self.key) #Crear cadena de 32 bytes en hexadecimal
        key = self.hash.digest() 
        
        self.hash.update("AES256")
        codeEncrypt = self.hash.digest()

        comprobation = key + codeEncrypt
        length = len(key) + len(codeEncrypt)

        if comprobation == ciphertext[-(length):]:

            dec = self.decrypt(ciphertext[:-(length)], key)
            if not os.path.exists(destiny):
            	os.mkdir(destiny)

            name = path.split("/").pop()
            with open(destiny + name[:-4], 'wb') as fo:
                fo.write(dec)
            os.remove(path)
            

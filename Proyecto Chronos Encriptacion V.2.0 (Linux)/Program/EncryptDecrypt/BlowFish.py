import os
import os.path
from Crypto.Cipher import Blowfish
from Crypto import Random
from Crypto.Hash import SHA256
from struct import pack

class BlowFish:
	def __init__(self,key):
		self.key = key
		self.hash = SHA256.new()

	def encrypt(self,plaintext, key):
		bs = Blowfish.block_size
		iv = Random.new().read(bs)
		bf = Blowfish.new(key, Blowfish.MODE_CBC, iv)

		plen = bs - (len(plaintext) % bs)
		padding = [plen]*plen
		padding = pack('b'*plen, *padding)
		message = iv + bf.encrypt(plaintext + padding)
		
		return message
  
	def encrypt_file(self, path,destiny = None):
		with open(path, 'rb') as fo: # aqui abrimos el "path/archivo" como read binary.
			plaintext = fo.read() # hacemos que el "path/archivo" sea un texto plano

		self.hash.update(self.key) # Actualizamos el hash
		key = self.hash.digest() # Crear cadena de 32 bytes en hexadecimal
		enc = self.encrypt(plaintext, key) # nos apoyamos en recursividad y encriptamos.
        
		self.hash.update("Blowfish")
		codeEncrypt = self.hash.digest()

		if not os.path.exists(destiny):
			os.mkdir(destiny)

		name = path.split("/").pop()
		with open(destiny + name + ".enc", 'wb') as fo: #aqui abrimos el "path/archivo" donde le ponemos la extension .enc y hacemos write binary
			fo.write(enc + key + codeEncrypt) #se reescribe el archivo existente
		os.remove(path) 

	def decrypt(self,ciphertext,key):
		bs = Blowfish.block_size
		iv = ciphertext[:bs]
		
		ciphertext = ciphertext[bs:]
		uncipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
		ciphertext = uncipher.decrypt(ciphertext)
		last_byte = ciphertext[-1]
		# La funcion convierte una cadena en entero en representaicon unicode
		last = last_byte if type(last_byte) is int else ord(last_byte)
		ciphertext = ciphertext[:-last].strip()
		
		return ciphertext

	def decrypt_file(self, path,destiny = None):
		with open(path, 'rb') as fo:
			ciphertext = fo.read()

		self.hash.update(self.key) #Crear cadena de 32 bytes en hexadecimal
		key = self.hash.digest() 
		
		self.hash.update("Blowfish")
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


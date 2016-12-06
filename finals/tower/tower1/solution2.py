import binascii
import base64
import hashlib
import struct
from pwn import *

table = {
	'0':'0000',	'1':'0001',
	'2':'0010',	'3':'0011',
	'4':'0100',	'5':'0101',
	'6':'0110',	'7':'0111',
	'8':'1000',	'9':'1001',
	'a':'1010',	'b':'1011',
	'c':'1100',	'd':'1101',
	'e':'1110',	'f':'1111',
}

def convertOffset(array):
	res = ''
	for i in array:
		res += table[i]
	return res

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
url = 'tower1.svattt.org'
port = 31331

def stripCiphertext(data,carry):
	if data[0:28] != '4c5a57494f7f0000000000040000':
		raise Exception('error padding')
	if data[-8:] != 'ffffffff':
		raise Exception('error padding')
	# Strip prefix & postfix
	data = data[28:-8]
	in_len = struct.unpack('<h',data[0:4].decode('hex'))[0]
	key_len =  struct.unpack('<h',data[4:8].decode('hex'))[0]
	if data[8:10].decode('hex') != carry:
		raise Exception('error padding')
	data = data[10:]
	if 'addeedfe01db5400' in data:
		data = data.replace('addeedfe01db5400',' ')
		return data.split()
	else:
		raise Exception('error padding')

res = {}
length = 1369

for p in alphabet:
	payload = p*127
	r = remote(url,port)
	r.recvuntil(':')
	r.send(payload)
	ciphertext = r.recvuntil('\n')[1:-1]
	r.close()
	offset, data = stripCiphertext(ciphertext,p)
	offset = convertOffset(offset)
	tmp = ''
	for i in range(length):
		if offset[i] == '1':
			tmp += p
		else:
			tmp += '?'
	res[p] = tmp

plaintext = ''

for i in range(length):
	for p in alphabet:
		if res[p][i] != '?':
			plaintext += res[p][i]
			continue

flag = hashlib.sha1(base64.b64decode(plaintext)).hexdigest()

print 'SVATTT{' + flag + '}'

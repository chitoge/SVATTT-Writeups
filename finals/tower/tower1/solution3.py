from pwn import *
import base64
import hashlib

url = 'tower1.svattt.org'
port = 31331

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

def unpad(s,carry):
	while True:
		l = len(s)-1
		if s[l] == chr(0) or s[l] == carry:
			s = s[:-1]	
		else:
			return s

payload = 'A'*127
r = remote(url,port)
r.recvuntil(':')
r.send(payload)
ciphertext = r.recvuntil('\n')[1:-1]
r.close()

offset, data = stripCiphertext(ciphertext,'A')
offset = convertOffset(offset)
data = data.decode('hex')

x = 0
buf = ''
for i in range(len(offset)):
	if offset[i] == '0':
		buf += chr(ord(data[x]) ^ 0xfe)
		x += 1
	else:
		buf += 'A'

print buf
res = unpad(buf,'A')
res = base64.b64decode(res)
res = hashlib.sha1(res).hexdigest()

print 'SVATTT{' + res + '}'
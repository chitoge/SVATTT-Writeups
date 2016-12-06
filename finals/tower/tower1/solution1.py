from pwn import *
import base64
import hashlib

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

payload = '$'*127
r = remote(url,port)
r.recvuntil(':')
r.send(payload)
ciphertext = r.recvuntil('\n')[1:-1]
r.close()

ciphertext = stripCiphertext(ciphertext,'$')[1].decode('hex')

res = ''
for i in ciphertext:
	res += chr(ord(i)^0xfe)

res = base64.b64decode(res)
res = hashlib.sha1(res).hexdigest()

print 'SVATTT{' + res + '}'
def parse(data):
	return int(data,16)

if __name__ == '__main__':
	f = open('chal','rb')
	file = f.read()
	f.close()
	#print file.encode('hex')
	cursor = 0
	res = ''

	while True:
		try:
			size = parse(file[cursor])
		except:
			break
		cursor += 3
		chunk = file[cursor:cursor+size]
		cursor += size + 2
		res += chunk
		#print size, chunk.encode('hex')
	print res.encode('hex')
	f = open('output','wb')
	f.write(res)
	f.close()

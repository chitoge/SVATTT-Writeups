from pwn import *
from string import printable
from itertools import product

flag = 'SVATTT{'
res = 'ffc309e61f2ac3df48d3b9b64fd1720bfb95b460a1235f5d91c4f92ce90dfa516e1b8c49225b808560a9d853980662dc26984e'
context.log_level = 'error'

while True:
    ok = False
    for i in printable:
        temp = flag + i
        f = open('input.txt', 'wb')
        f.write(temp)
        f.close()
        p = process(['./mrc_1f856d2a199b4cbf010c491dfa4efb424b9deed2', 'input.txt'])
        l = p.recvline()[:-1]
        pref = l[:-8]
        suff = l[-8:]
        print pref, suff
        if (len(flag) > 1):
            l = pref + suff[-2:]
        else:
            l = suff[-2:]
        p.close()
        print l
        if (l == res): break
        if (res.startswith(l)):
            flag = temp
            ok = True
            break
    if (ok):
        log.info(flag)
    else:
        print 'Not found'
        break
print flag
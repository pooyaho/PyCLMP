__author__ = 'PHo'


import bluetooth
import sys
import threading

uuid = "fa87c0d0-afac-11de-8a39-0800200c9a66"
addr = None

if len(sys.argv) < 2:
    print "No device specified. Searching all nearby bluetooth devices for"
    print "the BluetoothChat service"
else:
    addr = sys.argv[1]
    print "Searching for BluetoothChat on %s" % addr

# search for the BluetoothChat service
service_matches = bluetooth.find_service( uuid = uuid, address = addr )

if len(service_matches) == 0:
    print "couldn't find the BluetoothChat service =("
    sys.exit(0)

first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]

print "connecting to \"%s\" on %s" % (name, host)

# Create the client socket
sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((host, port))

class receiverThread(threading.Thread):
    def __init__ (self,sock):
        threading.Thread.__init__(self)
        self.sock = sock
    def run(self):
        while True:
            data = self.sock.recv(1024)
            if len(data) == 0: break
            print "received [%s]" % data

receiver = receiverThread(sock)
receiver.setDaemon(True)
receiver.start()
print "connected - type stuff:"
while True:
    data = raw_input()
    if len(data) == 0: break
    sock.send(data)
    print "sent [%s]" % data

sock.close()
from twisted.internet.protocol import ClientFactory,Protocol
from twisted.internet import reactor
from sys import stdout
from struct import *

class BTLogic(object):

	def __init__(self):
		self.peer_ip = 'test'
		self.peer_port = 'test'

	def doSomething(self):
		return "Hi, this is a placeholder string!"	


class HandShake(object):

	def __init__(self):
		self.pstrlen = pack('B',19)
		self.pstr = 'BitTorrent protocol'
		self.reserved = pack('xxxxxxxx')
		self.info_hash = ''
		self.peer_id = '-ZZ0001-123456789012'


	def makeStr(self):
		return self.pstrlen+self.pstr+self.reserved+self.info_hash+self.peer_id

class Echo(Protocol):

    def connectionMade(self):
    	self.app = BTLogic()
    	self.transport.write("Hello, server!")

	def dataReceived(self,data):
			print data

class EchoClientFactory(ClientFactory):
	def startedConnecting(self,connector):
		print 'Starting to connect'
	def buildProtocol(self,addr):
		print 'Connected!'
		return Echo()

	def clientConnectionLost(self,connector,reason):
		print 'Lost Connection. Reason:', reason
	def clientConnectionFailed(self,connector,reason):
		print 'Connection Failed. Reason', reason	

hs = HandShake()
print hs.makeStr()

reactor.connectTCP("localhost",9999,EchoClientFactory())
reactor.run()
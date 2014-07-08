# mock server

from twisted.internet import protocol,reactor

class Echo(protocol.Protocol):
	def dataReceived(self,data):
		self.transport.write(data)
		print data

class EchoFactory(protocol.Factory):
	def buildProtocol(self,addr):
		return Echo()

reactor.listenTCP(9999,EchoFactory())
reactor.run()
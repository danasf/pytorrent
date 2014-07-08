import requests
import hashlib
import bencode
import socket
from struct import *


class Tracker(object):

	def __init__(self):
		print "Initialized"

		self.DEBUG = False
		self.tracker_params = ''
		self.peer_id = '-ZZ0001-123456789012'
		self.port = 6889
		self.infohash = ''
		self.file_len = 0
		self.peers = []


	def readTorrent(self,myFile):
		'''Reads the torrent file, decodes, returns tracker announce'''
		print "Reading torrent..."
		data = bencode.bdecode(myFile)
		self.infohash = hashlib.sha1(bencode.bencode(data['info'])).digest()
		
		# if single file
		if 'length' in data['info']:
			self.file_len += data['info']['length']

		# if multiple files
		else:
			for file in data['info']['files']:
				self.file_len +=file['length'] 
		
		
		# iterate through until one matches http

		# otherwise use announce

		# build params	
		if self.DEBUG:
			print data
		
		self.tracker_params = {'peer_id':self.peer_id  , 'port':self.port ,'info_hash': self.infohash, 'left':self.file_len, 'uploaded': 0, 'downloaded': 0, 'numwant':15, 'supportcrypto':0,'compact':1, 'event':'started' }
		return data['announce']

	def getPeers(self,url):
	 	'''Sends request to tracker, returns peers bytestring'''
		print url
		r = requests.get(url, params=self.tracker_params)
		res = r.text
		res = bencode.bdecode(res)
		if self.DEBUG:
			print r.status_code
			print r.headers
			print res
		return res['peers']

	# every 6 bytes is a new peer
	# first 4 bytes are the ip address, 
	# last 2 are port number char*256+char	
	def parsePeers(self,peer_list):
		'''Parses peers bytestring, returns list of peers'''
		for i,char in enumerate(peer_list):
			# when a new peer reset
			if i%6 == 0:
				peer_ip = ""
				peer_port = ""
			# when pos < 4 add to ip
			if i%6 < 4:
				peer_ip+=str(ord(char))+'.'
			# when post == 4 start recording the port and save the peer_ip
			elif i%6 == 4:
				peer_port=ord(char)*256
			elif i%6 == 5:
				peer_port+=ord(char)
				self.peers.append([peer_ip[:-1],peer_port])
		return self.peers

class HandShake(object):

	def __init__(self,infohash):
		self.pstrlen = chr(19)
		self.pstr = "BitTorrent protocol"
		self.reserved = "\x00\x00\x00\x00\x00\x00\x00\x00"
		self.info_hash = infohash
		self.peer_id = "-ZZ0001-123456789012"


	def makeStr(self):
		return self.pstrlen+self.pstr+self.reserved+self.info_hash+self.peer_id

class Message(object):

	def __init__(self,data):
		self.types = { 0:'choke',
					   1:'unchoke',
					   2:'interested',
					   3:'not interested',
					   4:'have',
					   5:'bitfield',
					   6:'request'
					   }
		self.data = data

	def parse(self):
		print self.data
		if len(self.data) > 68:
			ints = map(ord,self.data[69:])
			print ints

	def send(self,message):
		pass


tor = Tracker()
myFile = open("ubuntu.iso.torrent","rb").read()
loc = tor.readTorrent(myFile)
peers = tor.parsePeers(tor.getPeers(loc))

hs = HandShake(tor.infohash)
hs_str = hs.makeStr()

for i,peer in enumerate(peers):
	print peer[0], peer[1]
	try:
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.connect((peer[0],peer[1]))
		s.send(hs_str)
		msg = Message(s.recv(2048))
		msg.parse()
		#s.write()
		s.close()
		# if data is longer than 68 chars there's a message
		#print "from peer:", data
	except socket.error:
		print socket.error

import requests
import hashlib
import bencode
import sys
from struct import *

class Torrent(object):

	def __init__(self):
		print "Initialized"

		self.DEBUG = False
		self.peer_id = '-ZZ0001-123456789012'
		self.port = 6889
		self.infohash = ''
		self.file_len = 0
		self.peers = []

	def readTorrent(self,myFile):
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
		
		tracker_params = {'peer_id':self.peer_id  , 'port':self.port ,'info_hash': self.infohash, 'left':self.file_len, 'uploaded': 0, 'downloaded': 0, 'numwant':5, 'supportcrypto':0,'compact':1, 'event':'started' }
		return self.getPeers(data['announce'],tracker_params)

	def getPeers(self,url,params):
		print "Sending reqest to tracker"
		print url
		r = requests.get(url, params=params)
		res = r.text
		res = bencode.bdecode(res)
		if self.DEBUG:
			print r.status_code
			print r.headers
			print res

		return self.parsePeers(res['peers'])

	# first 4 bytes are the ip address, 
	# last 2 are port number char*256+char	
	def parsePeers(self,peer_list):
		for i,char in enumerate(peer_list):
			# when pos == 0 reset
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
				#print peer_port
				self.peers.append([peer_ip[:-1],peer_port])

		return self.peers

tor = Torrent()
myFile = open("ubuntu.iso.torrent","rb").read()
print tor.readTorrent(myFile)

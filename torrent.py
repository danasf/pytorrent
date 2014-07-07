import requests
import hashlib
import bencode
import sys
import binascii

class Torrent(object):

	def __init__(self):
		print "Initialized"

	def readTorrent(self,myFile):
		print "Reading torrent..."
		data = bencode.bdecode(myFile)
		infohash = hashlib.sha1(bencode.bencode(data['info'])).digest()
		file_len = 0
		#
		if data['info']['files']:
			for file in data['info']['files']:
				file_len +=file['length'] 
		else:
			file_len += data['info']['length']

		# build params	
		params = {'peer_id': '-ZZ0001-123456789012' , 'info_hash': infohash, 'left':file_len, 'uploaded': 0, 'downloaded': 0, 'numwant':50, 'supportcrypto':0, }
		self.getPeers(data['announce'],params)

	def getPeers(self,url,params):
		print "Sending reqest to tracker"
		print url,params
		r = requests.get(url, params=params)
		print r.status_code
		print r.headers
		res = r.text
		res = bencode.bdecode(res)
		print res
		print res['peers']
		print res['interval']
		#print binascii.b2a_uu(res["peers"])

tor = Torrent()
myFile = open("ebook.torrent","rb").read()
tor.readTorrent(myFile)



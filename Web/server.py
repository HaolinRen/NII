
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep, path

from server.dataProcessor import dataProcessor
from server.topicServer import myTopicServer

import cgi

PORT_NUMBER = 8282

myts = myTopicServer()

class myHandler(BaseHTTPRequestHandler):

	#Handler for the GET requests
	def do_GET(self):
		if self.path=="/":
			self.path = "/index.html"
			# self.path = '/FaceCloud.html'
		try:
			#Check the file extension required and
			#set the right mime type
			sendReply = False

			# if '?' in self.path:
			# 	args = self.path.split('?')[1:]
			# 	self.path = self.path.split('?')[0]

			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			elif self.path.endswith(".jpg"):
				mimetype='image/jpg'
				self.path = self.path.replace('%20', ' ')
				sendReply = True
			elif self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			elif self.path.endswith(".png"):
				mimetype='image/png'
				if not path.isfile(curdir + "/client" + self.path):
					self.path = "/data/thumbnails/default-topic.png"
				sendReply = True
			elif self.path.endswith(".webm"):
				mimetype='video/webm'
				sendReply = True
				default_video = "/data/videos/2006_06_19_19_00.webm"
				video_location = "/Volumes/ABC/NHK/" + self.path.split('/')[-1]
				if path.isfile(video_location):
					f = open(video_location)
					self.send_response(200)
					self.send_header('Content-type',mimetype)
					self.end_headers()
					self.wfile.write(f.read())
					f.close()
					return
				else:
					print self.path
					self.path = default_video

			elif self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			elif self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True

			elif self.path.endswith(".eot"):
				mimetype = 'application/vnd.ms-fontobject'
				sendReply = True
			elif self.path.endswith(".otf"):
				mimetype = 'application/font-sfnt'
				sendReply = True
			elif self.path.endswith(".svg"):
				mimetype = 'image/svg+xml'
				sendReply = True
			elif self.path.endswith(".ttf"):
				mimetype = 'application/font-sfnt'
				sendReply = True
			elif self.path.endswith(".woff"):
				mimetype = 'application/font-woff'
				sendReply = True
			elif self.path.endswith(".woff2"):
				mimetype = 'application/font-woff2'
				sendReply = True
			elif self.path.endswith(".ico"):
				mimetype = 'image/x-icon'
				sendReply = True

			if sendReply == True:
				#Open the static file requested and send it
				f = open(curdir + "/client" + self.path)
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
			return

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

	#Handler for the POST requests
	def do_POST(self):
		try:
			ctype, pdict = cgi.parse_header(self.headers.getheader("Content-type"))	
			if ctype == "application/json":
				length = int(self.headers.getheader('content-length'))
				data = self.rfile.read(length)
				dp = dataProcessor(data)

				if self.path=="/get":
					dp.getEigValue()

				elif self.path == "/ben":
					para = dp.data
					dp.res = myts.analyseRequest(para)
					
				elif self.path == "/face":
					dp.res = myts.getFaceList()

				rep = dp.getJsonData()
				self.send_response(200)
				self.end_headers()
				self.wfile.write(rep)
		except Exception as e:
			print e
			self.send_error(404, "bad request")
			
			
try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()




	
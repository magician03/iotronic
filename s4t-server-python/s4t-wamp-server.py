#########################################################################################
##
## The MIT License (MIT)
##
## Copyright (c) 2014 Andrea Rocco Lotronto
##
## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this software and associated documentation files (the "Software"), to deal
## in the Software without restriction, including without limitation the rights
## to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
## copies of the Software, and to permit persons to whom the Software is
## furnished to do so, subject to the following conditions:
##
## The above copyright notice and this permission notice shall be included in all
## copies or substantial portions of the Software.
##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
## OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
## SOFTWARE.
########################################################################################

from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner
from twisted.internet.defer import inlineCallbacks

from twisted.internet import reactor


from flask import Flask
from flask.ext import restful

import threading

urlWampRouter = "ws://ip:port/ws"
realmWampRouter = "s4t"
topic = 'board.connection'

class restServer():
	class Wellcome(restful.Resource):
		def get(self):
			return{'Wellcome'}

	def __init__(self):
		self.app = Flask(__name__)
		self.api = restful.Api(self.app)
		self.api.add_resource(self.Wellcome, '/')

	def avvio(self):
		self.app.run(port=5566, debug=True)

@inlineCallbacks
def startREST():
	x = restServer()
	x.avvio()

class S4TWampServer(ApplicationSession):

	@inlineCallbacks
	def onJoin(self, details):

		self.connectedBoard = {}
		
		print("Connect to WAMP Router")

		def onMessage(*args):
			print args
			if args[1] == 'connection':
				print(args[0]+ " connessa")
				self.connectedBoard[args[0]] = args[0]
				print self.connectedBoard
				
			if args[1] == 'disconnect':
				print(args[0]+ " disconnessa")
				del self.connectedBoard[args[0]]
				print self.connectedBoard

			
		try:
			
			yield self.subscribe(onMessage, topic)
			print ("subscribed to topic:: "+topic)

		except Exception as e:
			print("could not subscribe to topic: {0}".format(e))


if __name__ == '__main__':
	#rest = serverRest()
	#rest.start()
	#t1 = threading.Thread(target=x.avvio())
	#t1.start()
	#t1.join()

	#wamp = wampT()
	#wamp.start()
	
	reactor.run(startREST())

	runner = ApplicationRunner(url = urlWampRouter, realm = realmWampRouter)
	runner.run(S4TWampServer)

	#serverRest().start()

	#runner = ApplicationRunner(url = urlWampRouter, realm = realmWampRouter)
	#runner.run(S4TWampServer)
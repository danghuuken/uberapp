import urllib2

class NextBusConnect: 

	route = ""
	stop = ""
	url_root = "http://webservices.nextbus.com/service/publicXMLFeed?"
	command = ""

	def setRoute(self, routeId):
		self.route  = routeId

	def setStop(self, stopId):
		self.stop = stopId

	def setCommand(self,command):
		self.command = command

	def buildUrl(self):
		url = self.url_root 
		#todo Create Error Handling if Command is not specified
		if self.command != "":
			url += "command=" + self.command
		
		url += "&a=sf-muni"

		if self.route != "":
			url = url + "&r=" + self.route

		if self.stop != "":
			url += "&s=" + self.stop



		return url

	def grabUrl(self):

		usock = urllib2.urlopen(self.buildUrl())
		data = usock.read()
		usock.close()
		return data
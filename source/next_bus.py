import urllib2

class NextBusConnect: 

	route = ""
	stop = ""
	url_root = "http://webservices.nextbus.com/service/publicXMLFeed?"
	command = ""
	# used to pull multiple stops 
	stops=[]

	def setRoute(self, routeId):
		self.route  = routeId

	def setStop(self,stopId):
		self.stop = stopId
		
	def setStops(self, stopIds):
		self.stops = stopIds

	def setCommand(self,command):
		self.command = command

	def buildUrl(self):
		url = self.url_root 
		#todo Create Error Handling if Command is not specified
		if self.command != "":
			url += "command=" + self.command
		
		url += "&a=sf-muni"

		if self.route != "" and len(self.stops) == 0:
			url = url + "&r=" + self.route

		if len(self.stops) != 0:
			for stop_tag in self.stops:
				url += "&stops=" + "%s|%s" %( self.route,stop_tag)



		return url

	def grabUrl(self):

		usock = urllib2.urlopen(self.buildUrl())
		data = usock.read()
		usock.close()
		return data
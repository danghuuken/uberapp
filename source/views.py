from django.shortcuts import render, get_object_or_404
from source.models import Post
import xml.etree.ElementTree as ET
import source.next_bus 

def index(request):
	next_connection = source.next_bus.NextBusConnect()
	next_connection.setCommand('predictions')
	next_connection.setRoute('N')
	next_connection.setStop('5200')
	data = next_connection.grabUrl()
	#print data
	root = ET.fromstring(data)
	
	#print root.tag
	departure_times = []
	for prediction in root.iter('prediction'):
		departure_times.append(prediction.get("minutes"))

	route_title = root.find('predictions').get('routeTitle')
	stop_title = root.find('predictions').get('stopTitle')
	print "Route Title: " + route_title
	print "Stop Title: " + stop_title

	post  = Post.objects.filter(published=True)

	context = {	'post':post,
				"route_title" : route_title,
				"stop_title" : stop_title,
				"departure_times" : ",".join(departure_times)
				}
	
	


	return render(request,'source/index.html',context)

def stoplist(request,stop_tag):

	next_connection = source.next_bus.NextBusConnect()

	next_connection.setCommand('routeConfig')
	next_connection.setRoute(stop_tag)

	data = next_connection.grabUrl()
	root = ET.fromstring(data)

	all_stops = []

	for stops in root.iter("stop"):
		stop_title = stops.get("title")

		if not stop_title in all_stops and stop_title != None:
			all_stops.append(stop_title)

	context = { "all_stops" : all_stops,
				"route_title" : root.find("route").get('title') }

	return render(request,"source/stoplist.html",context)



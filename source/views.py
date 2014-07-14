from django.shortcuts import render, get_object_or_404
from source.models import Post
import xml.etree.ElementTree as ET
import source.next_bus 
from source.models import Routes


def index(request):
	all_routes = getAllRoutes()

	sorted_tags = []
	for tag, title in all_routes.iteritems():
		sorted_tags.append(tag)




	context = {	
				"sorted_tags" : sorted(sorted_tags),
				"all_routes" : all_routes
				}
	
	


	return render(request,'source/index.html',context)

def stoplist(request):
	stop_tag = request.GET.get('tag')
	next_connection = source.next_bus.NextBusConnect()

	next_connection.setCommand('routeConfig')
	next_connection.setRoute(stop_tag)

	data = next_connection.grabUrl()
	root = ET.fromstring(data)

	all_stops = []
	stop_dict = {}


	for stops in root.iter("stop"):
		stop_title = stops.get("title")

		# Setting up a dictionary to help build a url that will send to the stop information list

		# making sure we dont access any null values
		if not stop_title in stop_dict and stop_title != None:
			stop_dict[stop_title] = stop_tag
		if stop_title != None:	
			#stop_dict[stop_title].append(stops.get('tag'))
			stop_dict[stop_title] =  '%s-%s' % (stop_dict[stop_title], stops.get('tag'))

	context = {
				"route_title" : Routes.objects.get(tag=stop_tag),
				"stop_dict" : stop_dict }

	return render(request,"source/stoplist.html",context)

def departures(request):
	context = {}
	tag = request.GET.get('tag')
	tag_comp = tag.split('-')

	route_predictions = []

	departure = grabMultiDepartures(tag_comp[0],tag_comp[1:])

	stop_title = departure[0]
	departure_info = departure[1]
	#Seting up empty arrays to store all stop information
	context['predictions'] = []
	context['destinations'] = []
	context['station'] = stop_title

	for direction, prediction in departure_info.iteritems():
		context['predictions'].append(prediction)
		context['destinations'].append(direction)

	context["route_title"] = Routes.objects.get(tag=tag_comp[0])
	context["length"] = range(len(departure_info))

	return render(request,"source/departures.html",context)		


def grabDeparture(route, tag):
	next_connection = source.next_bus.NextBusConnect()
	next_connection.setCommand('predictions')
	next_connection.setRoute(route)
	next_connection.setStop(tag)
	data = next_connection.grabUrl()
	root = ET.fromstring(data)
	departure_times = []
	for prediction in root.iter('prediction'):
		departure_times.append(prediction.get("minutes"))

	stop_title = root.find('predictions').get('stopTitle')

	return [stop_title,",".join(departure_times)]

def grabMultiDepartures(route,tags):

	next_connection = source.next_bus.NextBusConnect()
	next_connection.setCommand('predictionsForMultiStops')
	next_connection.setRoute(route)
	next_connection.setStops(tags)
	data = next_connection.grabUrl()
	root = ET.fromstring(data)

	stop_predictions = {}
	stop_title = root.find('predictions').get('stopTitle')

	for predictions in root.iter('predictions'):
		for direction in predictions.iter('direction'):
			departure_times = []
			for prediction in direction.iter('prediction'):
				departure_times.append(prediction.get('minutes'))

			stop_predictions[direction.get('title')] = ','.join(departure_times)
		
	return (stop_title, stop_predictions)


def getAllRoutes():
	all_routes = Routes.objects.all()
	
	routes = {} 

	for element in all_routes.values('tag','title'):
		tag = element['tag']
		title = element['title']
		routes[tag] = title

	return routes
	
import next_bus
import xml.etree.ElementTree as ET

next_connection = next_bus.NextBusConnect()

next_connection.setCommand('routeConfig')
next_connection.setRoute('N')

data = next_connection.grabUrl()
root = ET.fromstring(data)

all_stops = []

for stops in root.iter("stop"):
	stop_title = stops.get("title")

	if not stop_title in all_stops:
		all_stops.append(stop_title)

#print all_stops
print root.find("route").get('title')
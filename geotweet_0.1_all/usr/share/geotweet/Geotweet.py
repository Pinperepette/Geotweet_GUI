#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created: Sat Feb  7 17:41:23 2015
# by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!
from __future__ import print_function
from PyQt4 import QtCore, QtGui, QtWebKit
import tweepy, geopy, sys, os, time, ConfigParser, urllib, icon_qrc, webbrowser, ca_certs_locater
from geopy.geocoders import Nominatim
from instagram.client import InstagramAPI
import platform
from os.path import expanduser

#######################################################################
if platform.release() == 7:
	import ctypes
	from ctypes import wintypes

	lpBuffer = wintypes.LPWSTR()
	AppUserModelID = ctypes.windll.shell32.GetCurrentProcessExplicitAppUserModelID
	AppUserModelID(ctypes.cast(ctypes.byref(lpBuffer), wintypes.LPWSTR))
	appid = lpBuffer.value
	ctypes.windll.kernel32.LocalFree(lpBuffer)
	if appid is not None:
		print(appid)
	myappid = 'ciurma.Geotweet.1'  # arbitrary string
	ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
#######################################################################   for icon in task bar windows 7
if os.name == 'posix':
	separatore = "/"
else:
	separatore = """\\"""

if os.name == 'posix':
	dir_geotweet = expanduser("~") + separatore + ".Geotweet"
else:
	dir_geotweet = separatore + "Geotweet"

if os.path.exists(dir_geotweet):
	os.chdir(dir_geotweet)
else:
	os.mkdir(dir_geotweet)
	os.chdir(dir_geotweet)

#######################################################################

urllib.urlretrieve("http://curl.haxx.se/ca/cacert.pem ", "cacert.pem")
os.environ['REQUESTS_CA_BUNDLE'] = os.path.join('.', 'cacert.pem')

urllib.urlretrieve("http://www.geotweet.altervista.org/home/geotweet-icon.ico ", "geotweet-icon.ico")


def authentication():
	global config
	config = ConfigParser.ConfigParser()
	config.read(os.path.split(os.path.realpath(__file__))[0] + os.path.sep + "config.ini")
	global SCREEN_NAME
	SCREEN_NAME = config.get("twitter_keys", "SCREEN_NAME")
	global CONSUMER_KEY
	CONSUMER_KEY = config.get("twitter_keys", "CONSUMER_KEY")
	global CONSUMER_SECRET
	CONSUMER_SECRET = config.get("twitter_keys", "CONSUMER_SECRET")
	global ACCESS_TOKEN
	ACCESS_TOKEN = config.get("twitter_keys", "ACCESS_TOKEN")
	global ACCESS_TOKEN_SECRET
	ACCESS_TOKEN_SECRET = config.get("twitter_keys", "ACCESS_TOKEN_SECRET")
	global auth
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

	global api
	api = tweepy.API(auth)
	global geolocator
	geolocator = Nominatim()

	if SCREEN_NAME == '' or CONSUMER_KEY == '' or CONSUMER_SECRET == '' or ACCESS_TOKEN == '' or ACCESS_TOKEN_SECRET == '':
		ui2.see_keys()
		keys.show()
		sys.exit(app.exec_())

def autentikey():

	config_in = ConfigParser.ConfigParser()
	config_in.read(os.path.split(os.path.realpath(__file__))[0] + os.path.sep + "config_instagram.ini")

	
	CLIENT_ID = config_in.get("instagram_keys", "CONFIG_ID")
	CLIENT_SECRET = config_in.get("instagram_keys", "CONFIG_SECRET")
	REDIRECT_URI = config_in.get("instagram_keys", "REDIRECT_URI")
	scope = ["basic"]

	api = InstagramAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)
	redirect_uri = api.get_authorize_login_url(scope = scope)
	webbrowser.open_new(redirect_uri)


def authentication_instagram():
	global config_in
	config_in = ConfigParser.ConfigParser()
	config_in.read(os.path.split(os.path.realpath(__file__))[0] + os.path.sep + "config_instagram.ini")

	global CLIENT_ID
	CLIENT_ID = config_in.get("instagram_keys", "CONFIG_ID")
	global CLIENT_SECRET
	CLIENT_SECRET = config_in.get("instagram_keys", "CONFIG_SECRET")
	global REDIRECT_URI
	REDIRECT_URI = config_in.get("instagram_keys", "REDIRECT_URI")
	if CLIENT_ID == '' or CLIENT_SECRET == '' or REDIRECT_URI == '' :
		ui4.see_keys()
		Keys_instagram.show()
		sys.exit(app.exec_())


def insta_tline():
	indice = 0
	api = InstagramAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
	utente = api.user_search(q=insta_search)
	target = utente[0].id
	recent_media, next_ = api.user_recent_media(user_id=target, count=number_instagram)
	insta_out = '\n\
	<!DOCTYPE html>\n\
	<head>\n\
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />\n\
	<title>Test Figata</title>\
	<link href="http://www.geotweet.altervista.org/home/instagram.css" rel="stylesheet" type="text/css" />\n\
	</head>\n\
	<body>\n\
	<div id="instagram">'
	

	for media in recent_media:
		indice = indice + 1
		if indice == 1:
			insta_out += u'<div id="profilo_img">'
			insta_out += u'<img src="'+ media.user.profile_picture+ '"/>'
			insta_out += u'</div>'
			insta_out += u'<div id="profilo">'
			fn = str(media.user.full_name.encode('utf-8'))
			insta_out += u'<h1>'+ fn.decode('utf-8') + '</h1>'
			un = str(media.user.username.encode('utf-8'))
			insta_out += u'<h2>@'+ un.decode('utf-8') + '</h2>'
			insta_out += u'</div>'
			insta_out += u'<div id="spazio">'
			insta_out += u'</div>'
		insta_out += u'<div id="post">'
		insta_out += u'<t>' + str(media.created_time) + '</t>'
		insta_out += u'<div id="msg">'
		try:
			te = str(media.caption.text.encode('utf-8'))
			insta_out += u'<p>'+ te.decode('utf-8') + '</p>'
		except AttributeError:
			insta_out += u'<p>No Text</p>'
		insta_out += u'</div>'
		insta_out += u'<div id="foto">'
		insta_out += u'<a href="'+ media.link+ '"><img src="'+ media.images['low_resolution'].url+ '"/></a>'
		insta_out += u'</div>'
		insta_out += u'<div id="divisione">'
		insta_out += u'</div>'
		insta_out += u'</div>'
	insta_out += u'</div>'
	insta_out += u'</body>'
	insta_out += u'</html>'
	ui3.webView.setHtml(insta_out, QtCore.QUrl(u'file://localhost%s'))
	


def function_insta_tag():
	api = InstagramAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
	recent_media, next_ = api.tag_recent_media(number_instagram, 1, insta_tag)
	insta_out = '\n\
	<!DOCTYPE html>\n\
	<head>\n\
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />\n\
	<title>Test Figata</title>\n\
	<link href="http://www.geotweet.altervista.org/home/instagram_tag.css" rel="stylesheet" type="text/css" />\n\
	</head>\n\
	<body>\n\
	<div id="instagram">'
	for media in recent_media:

		insta_out += u'<div id="profilo_img">'
		insta_out += u'<img src="'+ media.user.profile_picture+ '"/>'
		insta_out += u'</div>'
		insta_out += u'<div id="profilo">'
		fn = str(media.user.full_name.encode('utf-8'))
		insta_out += u'<h1>'+ fn.decode('utf-8') + '</h1>'
		un = str(media.user.username.encode('utf-8'))
		insta_out += u'<h2>@'+ un.decode('utf-8') + '</h2>'
		insta_out += u'</div>'
		insta_out += u'<div id="spazio">'
		insta_out += u'</div>'
		insta_out += u'<div id="post">'
		insta_out += u'<t>'+ str(media.created_time)+ '</t>'
		insta_out += u'<div id="msg">'
		try:
			te = str(media.caption.text.encode('utf-8'))
			insta_out += u'<p>'+ te.decode('utf-8') + '</p>'
		except AttributeError:
			insta_out += u'<p>No Text</p>'
		insta_out += u'</div>'
		insta_out += u'<div id="foto">'
		insta_out += u'<a href="'+ media.link+ '"><img src="'+ media.images['low_resolution'].url+ '"/></a>'
		insta_out += u'</div>'
		insta_out += u'<div id="divisione">'
		insta_out += u'</div>'
		insta_out += u'</div>'

	insta_out += u'</div>'
	insta_out += u'</body>'
	insta_out += u'</html>'
	ui3.webView.setHtml(insta_out, QtCore.QUrl(u'file://localhost%s'))


def insta_tag_map():
	api = InstagramAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
	recent_media, next_ = api.tag_recent_media(number_instagram, 1, insta_tag)
	insta_map = '\n\
	<!DOCTYPE html>\n\
	<html> \n\
	<head> \n\
	<meta http-equiv="content-type" content="text/html; charset=UTF-8" /> \n\
	<title>Google Maps Multiple Markers</title>\n\
	<style>\n\
	html, body, #map {\n\
	height: 100%;\n\
	margin: 0px;\n\
	padding: 0px\n\
	}\n\
	</style> \n\
	<script src="https://maps.googleapis.com/maps/api/js?v=3?sensor=false"></script>\n\
	<script src="http://ajax.aspnetcdn.com/ajax/jQuery/jquery-1.10.1.min.js"></script>\n\
	</head> \n\
	<body>\n\
	<div id="map"></div>\n\
	<script type="text/javascript">\n\
	var locations = ['

	for media in recent_media:
		try:
			media.location
			fn = str(media.user.full_name.encode('utf-8'))
			un = str(media.user.username.encode('utf-8'))
			insta_map += u'["'+ '<h4>'+ fn.decode('utf-8')+ '- @'+ fn.decode('utf-8')+\
				  '</h4><p>'+ '</p><img src=\''+ media.images['low_resolution'].url+ '\'/>"'+ ','+\
				  str(media.location.point.latitude)+ ","+ str(media.location.point.longitude)+ '],'
		except AttributeError:
			print('No location')
	insta_map += u'];'

	insta_map += u'''\n\
	function initialize()\n\
{\n\
		var map = new google.maps.Map(document.getElementById('map'), {\n\
			zoom: 2,\n\
			center: new google.maps.LatLng(locations[0][1],locations[0][2]),\n\
			mapTypeId: google.maps.MapTypeId.HYBRID,\n\
			mapTypeControl: true,\n\
			streetViewControl: true,\n\
			panControl: false,\n\
			zoomControlOptions: {\n\
			position: google.maps.ControlPosition.LEFT_TOP\n\
			}\n\
			});\n\
\n\
	var infowindow = new google.maps.InfoWindow({\n\
		maxWidth: 320\n\
		});\n\
\n\
	var marker;\n\
	var markers = new Array();\n\
\n\
\n\
\n\
	// Add the markers and infowindows to the map\n\
	for (var i = 0; i < locations.length; i++) {  \n\
	marker = new google.maps.Marker({\n\
		position: new google.maps.LatLng(locations[i][1], locations[i][2]),\n\
		map: map,\n\
		//icon : locations[i][3],\n\
\n\
		});\n\
\n\
	markers.push(marker);\n\
\n\
	google.maps.event.addListener(marker, 'click', (function(marker, i) {\n\
		return function() {\n\
		infowindow.setContent(locations[i][0]);\n\
		infowindow.open(map, marker);\n\
		}\n\
		})(marker, i));\n\
\n\
\n\
	}\n\
\n\
	\n\
	map.fitBounds(bounds);\n\
	}\n\
	google.maps.event.addDomListener(window, 'load', initialize);\n\
	</script> \n\
	</body>\n\
	</html>'''
	ui.webView_2.setHtml(insta_map, QtCore.QUrl(u'file://localhost%s'))
	outfile = open('output_map.html', "w")
	outfile.write(insta_map.encode('utf-8'))


def insta_tline_map():
	api = InstagramAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
	utente = api.user_search(q=insta_search)
	target = utente[0].id
	recent_media, next_ = api.user_recent_media(user_id=target, count=number_instagram)
	insta_map = '''\n\
	<!DOCTYPE html>\n\
	<html> \n\
	<head> \n\
	<meta http-equiv="content-type" content="text/html; charset=UTF-8" /> \n\
	<title>Google Maps Multiple Markers</title>\n\
	<style>\n\
	html, body, #map {\n\
	height: 100%;\n\
	margin: 0px;\n\
	padding: 0px\n\
	}\n\
	</style> \n\
	<script src="https://maps.googleapis.com/maps/api/js?v=3?sensor=false"></script>\n\
	<script src="http://ajax.aspnetcdn.com/ajax/jQuery/jquery-1.10.1.min.js"></script>\n\
	</head> \n\
	<body>\n\
	<div id="map"></div>\n\

	<script type="text/javascript">\n\
	// Define your locations: HTML content for the info window, latitude, longitude\n\
	var locations = ['''

	for media in recent_media:
		try:
			media.location
			fn = str(media.user.full_name.encode('utf-8'))
			un = str(media.user.username.encode('utf-8'))
			insta_map += u'["'+ '<h4>'+ fn.decode('utf-8')+ '- @'+ fn.decode('utf-8')+\
				  '</h4><p>'+ '</p><img src=\''+ media.images['low_resolution'].url+ '\'/>"'+ ','+\
				  str(media.location.point.latitude)+ ","+ str(media.location.point.longitude)+ '],'

		except AttributeError:
			#print('No location')
			pass
	insta_map += '];'

	insta_map += '''\n\
	function initialize()\n\
{\n\
		var map = new google.maps.Map(document.getElementById('map'), {\n\
			zoom: 2,\n\
			center: new google.maps.LatLng(locations[0][1],locations[0][2]),\n\
			mapTypeId: google.maps.MapTypeId.HYBRID,\n\
			mapTypeControl: true,\n\
			streetViewControl: true,\n\
			panControl: false,\n\
			zoomControlOptions: {\n\
			position: google.maps.ControlPosition.LEFT_TOP\n\
			}\n\
			});\n\
\n\
	var infowindow = new google.maps.InfoWindow({\n\
		maxWidth: 320\n\
		});\n\
\n\
	var marker;\n\
	var markers = new Array();\n\
\n\
\n\
\n\
	// Add the markers and infowindows to the map\n\
	for (var i = 0; i < locations.length; i++) {  \n\
	marker = new google.maps.Marker({\n\
		position: new google.maps.LatLng(locations[i][1], locations[i][2]),\n\
		map: map,\n\
		//icon : locations[i][3],\n\
\n\
		});\n\
\n\
	markers.push(marker);\n\
\n\
	google.maps.event.addListener(marker, 'click', (function(marker, i) {\n\
		return function() {\n\
		infowindow.setContent(locations[i][0]);\n\
		infowindow.open(map, marker);\n\
		}\n\
		})(marker, i));\n\
\n\
\n\
	}\n\
\n\
	\n\
	map.fitBounds(bounds);\n\
	}\n\
	google.maps.event.addDomListener(window, 'load', initialize);\n\
	</script> \n\
	</body>\n\
	</html>'''
	ui.webView_2.setHtml(insta_map, QtCore.QUrl(u'file://localhost%s'))
	outfile = open('output_map.html', "w")
	outfile.write(insta_map.encode('utf-8'))


def create_map():
	places = api.geo_search(query=ZONE, granularity="country")
	place_id = places[0].id
	tweets = api.search(q="place:%s" % place_id, count=number)

	outfile = open('output_map.html', "w")
	outfile.write("""\
	<!DOCTYPE html>
	<html> 
	<head> 
	  <meta http-equiv="content-type" content="text/html; charset=UTF-8" /> 
	  <title>Google Maps Multiple Markers</title> 
	  <style>
	  html, body, #map {
		height: 100%;
		margin: 0px;
		padding: 0px
	  }
	</style>
	  <script src="https://maps.googleapis.com/maps/api/js?v=3?sensor=false"></script>
	  <script src="http://ajax.aspnetcdn.com/ajax/jQuery/jquery-1.10.1.min.js"></script>
	</head> 
	<body>
	  <div id="map"></div>

	  <script type="text/javascript">
		// Define your locations: HTML content for the info window, latitude, longitude
	   
		var locations = [  
		""")
	for tweet in tweets:
		if tweet.geo != None:
			lat = tweet.geo['coordinates'][0]
			lng = tweet.geo['coordinates'][1]
			tweettext = tweet.text.replace('"', "'").replace('\n', ' ')
			print('["', '<h4>', tweet.user.name.encode('utf-8'), '- @', tweet.user.screen_name.encode('utf-8'),
				  '</h4><p>', tweettext.replace("'", "\'").encode('utf-8'), '</p>",', tweet.geo['coordinates'][0], ",",
				  tweet.geo['coordinates'][1], ",", '"', tweet.user.profile_image_url, '"', '],', file=outfile)
	print('];', file=outfile)

	outfile.write("""\
	function initialize()
{
		var map = new google.maps.Map(document.getElementById('map'), {
			zoom: 2,
			center: new google.maps.LatLng(locations[0][1],locations[0][2]),
			mapTypeId: google.maps.MapTypeId.HYBRID,
			mapTypeControl: true,
			streetViewControl: true,
			panControl: false,
			zoomControlOptions: {
			position: google.maps.ControlPosition.LEFT_TOP
			}
			});

	var infowindow = new google.maps.InfoWindow({
		maxWidth: 320
		});

	var marker;
	var markers = new Array();



	// Add the markers and infowindows to the map
	for (var i = 0; i < locations.length; i++) {  
	marker = new google.maps.Marker({
		position: new google.maps.LatLng(locations[i][1], locations[i][2]),
		map: map,
		icon : locations[i][3],

		});

	markers.push(marker);

	google.maps.event.addListener(marker, 'click', (function(marker, i) {
		return function() {
		infowindow.setContent(locations[i][0]);
		infowindow.open(map, marker);
		}
		})(marker, i));


	}

	
	map.fitBounds(bounds);
	}
	google.maps.event.addDomListener(window, 'load', initialize);
	</script> 
	</body>
	</html>
	""")


def create_map_tl():
	num = 0
	nume = 0
	user = api.user_timeline(screen_name, count=number)
	outfile = open('output_map.html', "w")
	outfile.write("""\
	<!DOCTYPE html>
	<html> 
	<head> 
	  <meta http-equiv="content-type" content="text/html; charset=UTF-8" /> 
	  <title>Google Maps Multiple Markers</title>
	  <style>
	  html, body, #map {
		height: 100%;
		margin: 0px;
		padding: 0px
	  }
	</style> 
	  <script src="https://maps.googleapis.com/maps/api/js?v=3?sensor=false"></script>
	  <script src="http://ajax.aspnetcdn.com/ajax/jQuery/jquery-1.10.1.min.js"></script>
	</head> 
	<body>
	  <div id="map"></div>

	  <script type="text/javascript">
		// Define your locations: HTML content for the info window, latitude, longitude
		var locations = [  
		""")

	for tweet in user:
		if tweet.geo != None:
			tweettext = tweet.text.replace('"', "'").replace('\n', ' ')
			print('["', '<h4>', tweet.user.name.encode('utf-8'), '- @', tweet.user.screen_name.encode('utf-8'),
				  '</h4><p>', tweettext.replace("'", "\'").encode('utf-8'), '</p>",', tweet.geo['coordinates'][0], ",",
				  tweet.geo['coordinates'][1], ",", '"', tweet.user.profile_image_url, '"', '],', file=outfile)
	print('];', file=outfile)

	outfile.write("""\
	function initialize()
{
		var map = new google.maps.Map(document.getElementById('map'), {
			zoom: 2,
			center: new google.maps.LatLng(locations[0][1],locations[0][2]),
			mapTypeId: google.maps.MapTypeId.HYBRID,
			mapTypeControl: true,
			streetViewControl: true,
			panControl: false,
			zoomControlOptions: {
			position: google.maps.ControlPosition.LEFT_TOP
			}
			});

	var infowindow = new google.maps.InfoWindow({
		maxWidth: 320
		});

	var marker;
	var markers = new Array();



	// Add the markers and infowindows to the map
	for (var i = 0; i < locations.length; i++) {  
	marker = new google.maps.Marker({
		position: new google.maps.LatLng(locations[i][1], locations[i][2]),
		map: map,
		//icon : locations[i][3],

		});

	markers.push(marker);

	google.maps.event.addListener(marker, 'click', (function(marker, i) {
		return function() {
		infowindow.setContent(locations[i][0]);
		infowindow.open(map, marker);
		}
		})(marker, i));


	}

	
	map.fitBounds(bounds);
	}
	google.maps.event.addDomListener(window, 'load', initialize);
	</script> 
	</body>
	</html>
	""")


def timeline_user():
	indice = 0
	outfile = open('output.html', "w")
	user = api.user_timeline(screen_name, count=number)
	outfile.write("""\
		<!DOCTYPE html>
		<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
		<title>Test Figata</title>
		<link href="http://www.geotweet.altervista.org/home/general.css" rel="stylesheet" type="text/css" />
		</head>
		<body>
		<div id="twitter">
		""")

	for tweet in user:
		indice = indice + 1
		print("""<div id="tw">""", file=outfile)
		print("""<div id="tweet">""", file=outfile)
		print('<img src="', tweet.user.profile_image_url, '"/>', file=outfile)
		print('<h1>', tweet.user.name.encode('utf-8'), '</h1>', file=outfile)
		print('<h2>@', tweet.user.screen_name.encode('utf-8'), '</h2>', file=outfile)
		print('<p>', tweet.text.encode('utf-8'), '</p>', file=outfile)
		print("</div>", file=outfile)
		print("""<div id="info">""", file=outfile)
		print("Source: ", tweet.source.encode('utf-8'), '<br>', file=outfile)
		print("Date: ", tweet.created_at, '<br>', file=outfile)
		print("Rt: ", tweet.retweet_count, '<br>', file=outfile)
		print("Fav: ", tweet.favorite_count, '<br>', file=outfile)
		if tweet.geo == None:
			print("Geolocation: ", tweet.geo, '<br>', file=outfile)
		else:
			print("Geolocation: ", tweet.geo['coordinates'], '<br>', file=outfile)

		print("</div>", file=outfile)
		print("</div>", file=outfile)

	outfile.write('</div>')
	outfile.write("""</body>
	</html>
	""")


def search_tag():
	indice = 0
	c = tweepy.Cursor(api.search, q=TAG)
	outfile = open('output.html', "w")
	outfile.write("""\
		<!DOCTYPE html>
		<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
		<title>Test Figata</title>
		<link href="http://www.geotweet.altervista.org/home/general.css" rel="stylesheet" type="text/css" />
		</head>
		<body>
		<div id="twitter">
		""")

	for tweet in c.items(int(number)):
		indice = indice + 1
		print("""<div id="tw">""", file=outfile)
		print("""<div id="tweet">""", file=outfile)
		print('<img src="', tweet.user.profile_image_url, '"/>', file=outfile)
		print('<h1>', tweet.user.name.encode('utf-8'), '</h1>', file=outfile)
		print('<h2>@', tweet.user.screen_name.encode('utf-8'), '</h2>', file=outfile)
		print('<p>', tweet.text.encode('utf-8'), '</p>', file=outfile)
		print("</div>", file=outfile)
		print("""<div id="info">""", file=outfile)
		print("Source: ", tweet.source.encode('utf-8'), '<br>', file=outfile)
		print("Id: ", tweet.user.id, '<br>', file=outfile)
		print("Date: ", tweet.created_at, '<br>', file=outfile)
		print("Rt: ", tweet.retweet_count, '<br>', file=outfile)
		print("Tweet Id: ", tweet.id, '<br>', file=outfile)
		print("Fav: ", tweet.favorite_count, '<br>', file=outfile)
		if tweet.geo == None:
			print("Geolocation: ", tweet.geo, '<br>', file=outfile)
		else:
			print("Geolocation: ", tweet.geo['coordinates'], '<br>', file=outfile)

		print("</div>", file=outfile)
		print("</div>", file=outfile)

	outfile.write('</div>')
	outfile.write("""</body>
	</html>
	""")


def search_zone_map():
	indice = 0
	places = api.geo_search(query=ZONE, granularity="country")
	place_id = places[0].id
	tweets = api.search(q="place:%s" % place_id, count=number)
	outfile = open('output.html', "w")
	outfile.write("""\
		<!DOCTYPE html>
		<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
		<title>Test Figata</title>
		<link href="http://www.geotweet.altervista.org/home/general.css" rel="stylesheet" type="text/css" />
		</head>
		<body>
		<div id="twitter">
		""")

	for tweet in tweets:
		indice = indice + 1
		print("""<div id="tw">""", file=outfile)
		print("""<div id="tweet">""", file=outfile)
		print('<img src="', tweet.user.profile_image_url, '"/>', file=outfile)
		print('<h1>', tweet.user.name.encode('utf-8'), '</h1>', file=outfile)
		print('<h2>@', tweet.user.screen_name.encode('utf-8'), '</h2>', file=outfile)
		print('<p>', tweet.text.encode('utf-8'), '</p>', file=outfile)
		print("</div>", file=outfile)
		print("""<div id="info">""", file=outfile)
		print("Source: ", tweet.source.encode('utf-8'), '<br>', file=outfile)
		print("Id: ", tweet.user.id, '<br>', file=outfile)
		print("Date: ", tweet.created_at, '<br>', file=outfile)
		print("Rt: ", tweet.retweet_count, '<br>', file=outfile)
		print("Tweet Id: ", tweet.id, '<br>', file=outfile)
		print("Fav: ", tweet.favorite_count, '<br>', file=outfile)
		if tweet.geo == None:
			print("Geolocation: ", tweet.geo, '<br>', file=outfile)
		else:
			print("Geolocation: ", tweet.geo['coordinates'], '<br>', file=outfile)

		print("</div>", file=outfile)
		print("</div>", file=outfile)

	outfile.write('</div>')
	outfile.write("""</body>
	</html>
	""")


def search_user():
	user = api.get_user(arg_user_search, include_entities=1)
	outfile = open('output.html', "w")
	outfile.write("""\
		<!DOCTYPE html>
		<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
		<title>Test Figata</title>
		<link href="http://www.geotweet.altervista.org/home/user.css" rel="stylesheet" type="text/css" />
		</head>
		<body>
		<div id="twitter">
		""")
	print("""<div id="tw">""", file=outfile)
	print("""<div id="tweet">""", file=outfile)
	print('<img src="', user.profile_image_url, '"/>', file=outfile)
	print('<h1>', user.name.encode('utf-8'), '</h1>', file=outfile)
	print('<h2>@', user.screen_name.encode('utf-8'), '</h2>', file=outfile)
	print("</div>", file=outfile)
	print("""<div id="info">""", file=outfile)
	print("ID: ", user.id, '<br>', file=outfile)
	print("URL: ", user.url, '<br>', file=outfile)
	if user.status.geo == None:
		print("Geolocation: ", user.status.geo, '<br>', file=outfile)
	else:
		print("Geolocation: ", user.status.geo['coordinates'], '<br>', file=outfile)

	print("Followers: ", user.followers_count, '<br>', file=outfile)
	print("Following: ", user.friends_count, '<br>', file=outfile)
	print("ID: ", user.id, '<br>', file=outfile)
	print('<br>', file=outfile)
	print("Description: ", '<br>', file=outfile)
	print(user.description.encode('utf-8'), file=outfile)
	print("</div>", file=outfile)
	print("</div>", file=outfile)
	outfile.write('</div>')
	outfile.write("""</body>
	</html>
	""")


################################################################################################

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QtGui.QApplication.UnicodeUTF8

	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig)


class Ui_keys(object):
	def setupUi(self, keys):
		keys.setObjectName(_fromUtf8("keys"))
		keys.resize(500, 400)
		keys.setMinimumSize(QtCore.QSize(500, 400))
		keys.setMaximumSize(QtCore.QSize(500, 400))
		self.horizontalLayoutWidget = QtGui.QWidget(keys)
		self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 40, 441, 51))
		self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
		self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
		self.horizontalLayout.setMargin(0)
		self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
		self.label = QtGui.QLabel(self.horizontalLayoutWidget)
		self.label.setObjectName(_fromUtf8("label"))
		self.horizontalLayout.addWidget(self.label)
		self.screen_name = QtGui.QLineEdit(self.horizontalLayoutWidget)
		self.screen_name.setObjectName(_fromUtf8("screen_name"))
		self.horizontalLayout.addWidget(self.screen_name)
		self.horizontalLayoutWidget_2 = QtGui.QWidget(keys)
		self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(30, 100, 441, 51))
		self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
		self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
		self.horizontalLayout_2.setMargin(0)
		self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
		self.label_2 = QtGui.QLabel(self.horizontalLayoutWidget_2)
		self.label_2.setObjectName(_fromUtf8("label_2"))
		self.horizontalLayout_2.addWidget(self.label_2)
		self.consumer_key = QtGui.QLineEdit(self.horizontalLayoutWidget_2)
		self.consumer_key.setObjectName(_fromUtf8("consumer_key"))
		self.horizontalLayout_2.addWidget(self.consumer_key)
		self.horizontalLayoutWidget_3 = QtGui.QWidget(keys)
		self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(30, 160, 441, 51))
		self.horizontalLayoutWidget_3.setObjectName(_fromUtf8("horizontalLayoutWidget_3"))
		self.horizontalLayout_3 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_3)
		self.horizontalLayout_3.setMargin(0)
		self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
		self.label_3 = QtGui.QLabel(self.horizontalLayoutWidget_3)
		self.label_3.setObjectName(_fromUtf8("label_3"))
		self.horizontalLayout_3.addWidget(self.label_3)
		self.consumer_secret = QtGui.QLineEdit(self.horizontalLayoutWidget_3)
		self.consumer_secret.setObjectName(_fromUtf8("consumer_secret"))
		self.horizontalLayout_3.addWidget(self.consumer_secret)
		self.horizontalLayoutWidget_4 = QtGui.QWidget(keys)
		self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(30, 220, 441, 51))
		self.horizontalLayoutWidget_4.setObjectName(_fromUtf8("horizontalLayoutWidget_4"))
		self.horizontalLayout_4 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_4)
		self.horizontalLayout_4.setMargin(0)
		self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
		self.label_4 = QtGui.QLabel(self.horizontalLayoutWidget_4)
		self.label_4.setObjectName(_fromUtf8("label_4"))
		self.horizontalLayout_4.addWidget(self.label_4)
		self.access_token = QtGui.QLineEdit(self.horizontalLayoutWidget_4)
		self.access_token.setObjectName(_fromUtf8("access_token"))
		self.horizontalLayout_4.addWidget(self.access_token)
		self.horizontalLayoutWidget_5 = QtGui.QWidget(keys)
		self.horizontalLayoutWidget_5.setGeometry(QtCore.QRect(30, 280, 441, 51))
		self.horizontalLayoutWidget_5.setObjectName(_fromUtf8("horizontalLayoutWidget_5"))
		self.horizontalLayout_5 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_5)
		self.horizontalLayout_5.setMargin(0)
		self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
		self.label_5 = QtGui.QLabel(self.horizontalLayoutWidget_5)
		self.label_5.setObjectName(_fromUtf8("label_5"))
		self.horizontalLayout_5.addWidget(self.label_5)
		self.access_token_secret = QtGui.QLineEdit(self.horizontalLayoutWidget_5)
		self.access_token_secret.setObjectName(_fromUtf8("access_token_secret"))
		self.horizontalLayout_5.addWidget(self.access_token_secret)
		self.pushButton = QtGui.QPushButton(keys)
		self.pushButton.setGeometry(QtCore.QRect(400, 350, 75, 23))
		self.pushButton.clicked.connect(self.save_config_clicked)
		self.pushButton.setObjectName(_fromUtf8("pushButton"))
		self.label_6 = QtGui.QLabel(keys)
		self.label_6.setGeometry(QtCore.QRect(30, 340, 341, 41))
		self.label_6.setTextFormat(QtCore.Qt.AutoText)
		self.label_6.setOpenExternalLinks(True)
		self.label_6.setObjectName(_fromUtf8("label_6"))
		self.label_7 = QtGui.QLabel(keys)
		self.label_7.setGeometry(QtCore.QRect(120, 10, 261, 31))
		font = QtGui.QFont()
		font.setPointSize(20)
		font.setBold(True)
		font.setWeight(75)
		self.label_7.setFont(font)
		self.label_7.setLayoutDirection(QtCore.Qt.LeftToRight)
		self.label_7.setStyleSheet(_fromUtf8(""))
		self.label_7.setObjectName(_fromUtf8("label_7"))

		self.retranslateUi(keys)
		QtCore.QMetaObject.connectSlotsByName(keys)

	def retranslateUi(self, keys):
		keys.setWindowTitle(_translate("keys", "Keys", None))
		self.label.setText(_translate("keys", "screen_name           ", None))
		self.label_2.setText(_translate("keys", "consumer_key          ", None))
		self.label_3.setText(_translate("keys", "consumer_secret      ", None))
		self.label_4.setText(_translate("keys", "access_token            ", None))
		self.label_5.setText(_translate("keys", "access_token_secret", None))
		self.pushButton.setText(_translate("keys", "Save", None))
		self.label_6.setText(_translate("keys",
										"Open <a href='http://apps.twitter.com'>apps.twitter.com</a>, create new app, paste yours keys here.",
										None))
		self.label_7.setText(_translate("keys", "CONFIGURATIONS", None))

	@QtCore.pyqtSlot()
	def save_config_clicked(self):
		fileconfig = open('config.ini', "w")
		print('[twitter_keys]', file=fileconfig)
		print('SCREEN_NAME =', str(self.screen_name.text()), file=fileconfig)
		print('CONSUMER_KEY =', str(self.consumer_key.text()), file=fileconfig)
		print('CONSUMER_SECRET =', str(self.consumer_secret.text()), file=fileconfig)
		print('ACCESS_TOKEN =', str(self.access_token.text()), file=fileconfig)
		print('ACCESS_TOKEN_SECRET =', str(self.access_token_secret.text()), file=fileconfig)
		fileconfig.close()
		#restart
		python = sys.executable
		os.execl(python, python, *sys.argv)

	def see_keys(self):
		self.screen_name.setText(SCREEN_NAME)
		self.consumer_key.setText(CONSUMER_KEY)
		self.consumer_secret.setText(CONSUMER_SECRET)
		self.access_token.setText(ACCESS_TOKEN)
		self.access_token_secret.setText(ACCESS_TOKEN_SECRET)


class Ui_Keys_instagram(object):
	def setupUi(self, Keys_instagram):
		Keys_instagram.setObjectName(_fromUtf8("Keys_instagram"))
		Keys_instagram.resize(500, 300)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(Keys_instagram.sizePolicy().hasHeightForWidth())
		Keys_instagram.setSizePolicy(sizePolicy)
		Keys_instagram.setMinimumSize(QtCore.QSize(500, 300))
		Keys_instagram.setMaximumSize(QtCore.QSize(500, 300))
		self.horizontalLayoutWidget = QtGui.QWidget(Keys_instagram)
		self.horizontalLayoutWidget.setGeometry(QtCore.QRect(9, 39, 481, 51))
		self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
		self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
		self.horizontalLayout.setMargin(0)
		self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
		self.label = QtGui.QLabel(self.horizontalLayoutWidget)
		self.label.setMinimumSize(QtCore.QSize(90, 0))
		self.label.setMaximumSize(QtCore.QSize(90, 16777215))
		self.label.setObjectName(_fromUtf8("label"))
		self.horizontalLayout.addWidget(self.label)
		self.lineEdit = QtGui.QLineEdit(self.horizontalLayoutWidget)
		self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
		self.horizontalLayout.addWidget(self.lineEdit)
		self.horizontalLayoutWidget_2 = QtGui.QWidget(Keys_instagram)
		self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 110, 481, 51))
		self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
		self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
		self.horizontalLayout_2.setMargin(0)
		self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
		self.label_2 = QtGui.QLabel(self.horizontalLayoutWidget_2)
		self.label_2.setMinimumSize(QtCore.QSize(90, 0))
		self.label_2.setMaximumSize(QtCore.QSize(90, 16777215))
		self.label_2.setObjectName(_fromUtf8("label_2"))
		self.horizontalLayout_2.addWidget(self.label_2)
		self.lineEdit_2 = QtGui.QLineEdit(self.horizontalLayoutWidget_2)
		self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
		self.horizontalLayout_2.addWidget(self.lineEdit_2)
		self.pushButton = QtGui.QPushButton(Keys_instagram)
		self.pushButton.setGeometry(QtCore.QRect(420, 260, 75, 23))
		self.pushButton.clicked.connect(self.save_config_clicked)
		self.pushButton.setObjectName(_fromUtf8("pushButton"))
		self.label_3 = QtGui.QLabel(Keys_instagram)
		self.label_3.setGeometry(QtCore.QRect(10, 260, 281, 16))
		self.label_3.setOpenExternalLinks(True)
		self.label_3.setObjectName(_fromUtf8("label_3"))
		self.label_4 = QtGui.QLabel(Keys_instagram)
		self.label_4.setGeometry(QtCore.QRect(10, 10, 481, 21))
		font = QtGui.QFont()
		font.setFamily(_fromUtf8("Segoe Marker"))
		font.setPointSize(14)
		font.setBold(True)
		font.setWeight(75)
		self.label_4.setFont(font)
		self.label_4.setStyleSheet(_fromUtf8(""))
		self.label_4.setScaledContents(False)
		self.label_4.setAlignment(QtCore.Qt.AlignCenter)
		self.label_4.setObjectName(_fromUtf8("label_4"))
		self.horizontalLayoutWidget_3 = QtGui.QWidget(Keys_instagram)
		self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, 180, 481, 51))
		self.horizontalLayoutWidget_3.setObjectName(_fromUtf8("horizontalLayoutWidget_3"))
		self.horizontalLayout_3 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_3)
		self.horizontalLayout_3.setMargin(0)
		self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
		self.label_5 = QtGui.QLabel(self.horizontalLayoutWidget_3)
		self.label_5.setMinimumSize(QtCore.QSize(90, 0))
		self.label_5.setMaximumSize(QtCore.QSize(90, 16777215))
		self.label_5.setObjectName(_fromUtf8("label_5"))
		self.horizontalLayout_3.addWidget(self.label_5)
		self.lineEdit_3 = QtGui.QLineEdit(self.horizontalLayoutWidget_3)
		self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
		self.horizontalLayout_3.addWidget(self.lineEdit_3)

		self.retranslateUi(Keys_instagram)
		QtCore.QMetaObject.connectSlotsByName(Keys_instagram)

	def retranslateUi(self, Keys_instagram):
		Keys_instagram.setWindowTitle(_translate("Keys_instagram", "Form", None))
		self.label.setText(_translate("Keys_instagram", "CLIENT_ID", None))
		self.label_2.setText(_translate("Keys_instagram", "CLIENT_SECRET", None))
		self.pushButton.setText(_translate("Keys_instagram", "Save", None))
		self.label_3.setText(_translate("Keys_instagram", "Open <a href='https://instagram.com/developer'>instagram.com/developer</a>, create new app, paste yours keys here.",None))        
		self.label_4.setText(_translate("Keys_instagram", "INSTAGRAM CONFIGURATIONS", None))
		self.label_5.setText(_translate("Keys_instagram", "REDIRECT_URI", None))

	@QtCore.pyqtSlot()
	def save_config_clicked(self):
		fileconfig = open('config_instagram.ini', "w")
		print('[instagram_keys]', file=fileconfig)
		print('CONFIG_ID =', str(self.lineEdit.text()), file=fileconfig)
		print('CONFIG_SECRET =', str(self.lineEdit_2.text()), file=fileconfig)
		print('REDIRECT_URI =', str(self.lineEdit_3.text()), file=fileconfig)
		fileconfig.close()
		autentikey()
		Keys_instagram.close()
		

	def see_keys(self):
		self.lineEdit.setText(CLIENT_ID)
		self.lineEdit_2.setText(CLIENT_SECRET)
		self.lineEdit_3.setText(REDIRECT_URI)


class Ui_Form(object):
	def setupUi(self, Form):
		Form.setObjectName(_fromUtf8("Form"))
		Form.resize(400, 601)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
		Form.setSizePolicy(sizePolicy)
		Form.setMinimumSize(QtCore.QSize(400, 600))
		Form.setMaximumSize(QtCore.QSize(400, 1080))
		self.gridLayout_2 = QtGui.QGridLayout(Form)
		self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
		self.horizontalLayout = QtGui.QHBoxLayout()
		self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
		self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
		self.lineEdit = QtGui.QLineEdit(Form)
		self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
		self.horizontalLayout.addWidget(self.lineEdit)

		self.pushButton = QtGui.QPushButton(Form)
		self.pushButton.setObjectName(_fromUtf8("pushButton"))
		self.pushButton.clicked.connect(self.tline_search_instagram)
		self.horizontalLayout.addWidget(self.pushButton)

		self.pushButton_1 = QtGui.QPushButton(Form)
		self.pushButton_1.setObjectName(_fromUtf8("pushButton"))
		self.pushButton_1.clicked.connect(self.tag_search_instagram)
		self.horizontalLayout.addWidget(self.pushButton_1)

		self.lcdNumber = QtGui.QLCDNumber(Form)
		self.lcdNumber.setMaximumSize(QtCore.QSize(50, 50))
		self.lcdNumber.setObjectName(_fromUtf8("lcdNumber"))
		self.horizontalLayout.addWidget(self.lcdNumber)
		self.dial = QtGui.QDial(Form)
		self.dial.setMaximumSize(QtCore.QSize(45, 45))
		self.dial.setObjectName(_fromUtf8("dial"))
		self.horizontalLayout.addWidget(self.dial)
		self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
		self.gridLayout = QtGui.QGridLayout()
		self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
		self.webView = QtWebKit.QWebView(Form)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.webView.sizePolicy().hasHeightForWidth())
		self.webView.setSizePolicy(sizePolicy)
		self.webView.setMaximumSize(QtCore.QSize(400, 16777215))
		self.webView.setUrl(QtCore.QUrl(_fromUtf8("http://www.geotweet.altervista.org/home/instagram.html")))
		self.webView.setObjectName(_fromUtf8("webView"))
		self.gridLayout.addWidget(self.webView, 0, 0, 1, 1)
		self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)

		self.retranslateUi(Form)
		QtCore.QObject.connect(self.dial, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.lcdNumber.display)
		QtCore.QMetaObject.connectSlotsByName(Form)

	def retranslateUi(self, Form):
		Form.setWindowTitle(_translate("Form", "Instagram", None))
		self.pushButton.setText(_translate("Form", "User", None))
		self.pushButton_1.setText(_translate("Form", "Tag", None))

	@QtCore.pyqtSlot()
	def tline_search_instagram(self):
		global insta_search
		insta_search = str(self.lineEdit.text())
		global number_instagram
		number_instagram = int(self.lcdNumber.value())
		insta_tline()
		insta_tline_map()
		

	def tag_search_instagram(self):
		global insta_tag
		insta_tag = str(self.lineEdit.text())
		global number_instagram
		number_instagram = int(self.lcdNumber.value())
		function_insta_tag()
		insta_tag_map()
		
		


class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName(_fromUtf8("MainWindow"))
		MainWindow.resize(1100, 700)
		MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
		self.centralwidget = QtGui.QWidget(MainWindow)
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
		self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
		self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
		self.tabWidget = QtGui.QTabWidget(self.centralwidget)
		self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
		self.tab = QtGui.QWidget()
		self.tab.setObjectName(_fromUtf8("tab"))
		self.gridLayout = QtGui.QGridLayout(self.tab)
		self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
		self.webView = QtWebKit.QWebView(self.tab)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.webView.sizePolicy().hasHeightForWidth())
		self.webView.setSizePolicy(sizePolicy)
		self.webView.setUrl(QtCore.QUrl(_fromUtf8("http://www.geotweet.altervista.org/home/index.html")))
		self.webView.setObjectName(_fromUtf8("webView"))
		self.gridLayout.addWidget(self.webView, 1, 0, 1, 1)
		self.widget = QtGui.QWidget(self.tab)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
		self.widget.setSizePolicy(sizePolicy)
		self.widget.setMaximumSize(QtCore.QSize(16777215, 60))
		self.widget.setLayoutDirection(QtCore.Qt.LeftToRight)
		self.widget.setAutoFillBackground(False)
		self.widget.setObjectName(_fromUtf8("widget"))
		self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
		self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
		self.horizontalLayout.setMargin(0)
		self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
		self.lineEdit = QtGui.QLineEdit(self.widget)
		self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
		self.horizontalLayout.addWidget(self.lineEdit)
		global maps
		self.radioButton = QtGui.QRadioButton(self.widget)
		self.radioButton.setObjectName(_fromUtf8("radioButton"))
		maps = self.radioButton
		self.horizontalLayout.addWidget(self.radioButton)
		self.verticalLayout_2 = QtGui.QVBoxLayout()
		self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))

		self.pushButton_4 = QtGui.QPushButton(self.widget)
		self.pushButton_4.clicked.connect(self.on_pushTLButtonPrint_clicked)
		icon3 = QtGui.QIcon()
		icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/Timeline-48.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.pushButton_4.setIcon(icon3)
		self.pushButton_4.setIconSize(QtCore.QSize(16, 16))
		self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
		self.verticalLayout_2.addWidget(self.pushButton_4)

		self.pushButton_3 = QtGui.QPushButton(self.widget)
		self.pushButton_3.clicked.connect(self.on_pushTagButtonPrint_clicked)
		icon2 = QtGui.QIcon()
		icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/Tag-48.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.pushButton_3.setIcon(icon2)
		self.pushButton_3.setIconSize(QtCore.QSize(16, 16))
		self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
		self.verticalLayout_2.addWidget(self.pushButton_3)
		self.horizontalLayout.addLayout(self.verticalLayout_2)
		self.verticalLayout = QtGui.QVBoxLayout()
		self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))

		self.pushButton_2 = QtGui.QPushButton(self.widget)
		self.pushButton_2.clicked.connect(self.on_pushZoneButtonPrint_clicked)
		icon1 = QtGui.QIcon()
		icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/Drop-Zone-48.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.pushButton_2.setIcon(icon1)
		self.pushButton_2.setIconSize(QtCore.QSize(16, 16))
		self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
		self.verticalLayout.addWidget(self.pushButton_2)

		self.pushButton = QtGui.QPushButton(self.widget)
		self.pushButton.clicked.connect(self.on_pushButtonPrint_clicked)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/User_48.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.pushButton.setIcon(icon)
		self.pushButton.setIconSize(QtCore.QSize(16, 16))
		self.pushButton.setObjectName(_fromUtf8("pushButton"))
		self.verticalLayout.addWidget(self.pushButton)
		self.horizontalLayout.addLayout(self.verticalLayout)
		self.lcdNumber = QtGui.QLCDNumber(self.widget)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.lcdNumber.sizePolicy().hasHeightForWidth())
		self.lcdNumber.setSizePolicy(sizePolicy)
		self.lcdNumber.setMaximumSize(QtCore.QSize(16777215, 40))
		self.lcdNumber.setObjectName(_fromUtf8("lcdNumber"))
		self.horizontalLayout.addWidget(self.lcdNumber)
		self.dial = QtGui.QDial(self.widget)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.dial.sizePolicy().hasHeightForWidth())
		self.dial.setSizePolicy(sizePolicy)
		self.dial.setMaximumSize(QtCore.QSize(16777215, 60))
		self.dial.setNotchTarget(13.7)
		self.dial.setRange(1, 200)
		self.dial.setObjectName(_fromUtf8("dial"))
		self.horizontalLayout.addWidget(self.dial)
		self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)
		self.tabWidget.addTab(self.tab, _fromUtf8(""))
		self.tab_2 = QtGui.QWidget()
		self.tab_2.setObjectName(_fromUtf8("tab_2"))
		self.gridLayout_3 = QtGui.QGridLayout(self.tab_2)
		self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
		self.webView_2 = QtWebKit.QWebView(self.tab_2)
		self.webView_2.setUrl(QtCore.QUrl(_fromUtf8("http://www.geotweet.altervista.org/home/map.html")))
		self.webView_2.setObjectName(_fromUtf8("webView_2"))
		self.gridLayout_3.addWidget(self.webView_2, 0, 0, 1, 1)
		self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
		self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
		MainWindow.setCentralWidget(self.centralwidget)

		self.menubar = QtGui.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
		self.menubar.setObjectName(_fromUtf8("menubar"))
		self.menuSettings = QtGui.QMenu(self.menubar)
		self.menuSettings.setObjectName(_fromUtf8("menuSettings"))
		self.menuInstagram = QtGui.QMenu(self.menubar)
		self.menuInstagram.setObjectName(_fromUtf8("menuInstagram"))
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtGui.QStatusBar(MainWindow)
		self.statusbar.setObjectName(_fromUtf8("statusbar"))
		MainWindow.setStatusBar(self.statusbar)
		self.actionSettings = QtGui.QAction(MainWindow)
		self.actionSettings.setObjectName(_fromUtf8("actionSettings"))
		self.actionExit = QtGui.QAction(MainWindow)
		self.actionExit.setObjectName(_fromUtf8("actionExit"))
		self.actionSettings_2 = QtGui.QAction(MainWindow)
		self.actionSettings_2.setObjectName(_fromUtf8("actionSettings_2"))
		self.actionStart_Module = QtGui.QAction(MainWindow)
		self.actionStart_Module.setObjectName(_fromUtf8("actionStart_Module"))
		self.menuSettings.addSeparator()
		self.menuSettings.addAction(self.actionSettings)
		self.menuSettings.addSeparator()
		self.menuSettings.addAction(self.actionExit)
		self.menuInstagram.addAction(self.actionSettings_2)
		self.menuInstagram.addAction(self.actionStart_Module)
		self.menubar.addAction(self.menuSettings.menuAction())
		self.menubar.addAction(self.menuInstagram.menuAction())

		self.retranslateUi(MainWindow)
		self.tabWidget.setCurrentIndex(0)
		QtCore.QObject.connect(self.dial, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.lcdNumber.display)
		QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.close)
		QtCore.QObject.connect(self.actionSettings, QtCore.SIGNAL(_fromUtf8("triggered()")), self.open_configurations)
		QtCore.QObject.connect(self.actionSettings_2, QtCore.SIGNAL(_fromUtf8("triggered()")),
							   self.open_insta_configuration)  #configuration instagram
		QtCore.QObject.connect(self.actionStart_Module, QtCore.SIGNAL(_fromUtf8("triggered()")), self.open_instagram)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(_translate("MainWindow", "Geo Tweet", None))
		self.radioButton.setText(_translate("MainWindow", "Create Maps", None))
		self.pushButton_4.setText(_translate("MainWindow", "TLINE", None))
		self.pushButton_3.setText(_translate("MainWindow", "TAG", None))
		self.pushButton_2.setText(_translate("MainWindow", "ZONE", None))
		self.pushButton.setText(_translate("MainWindow", "USER", None))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Twitter", None))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Maps", None))
		self.menuSettings.setTitle(_translate("MainWindow", "Geotweet", None))
		self.actionSettings.setText(_translate("MainWindow", "Settings", None))
		self.actionSettings.setShortcut(_translate("MainWindow", "Ctrl+S", None))
		self.actionExit.setText(_translate("MainWindow", "Exit", None))
		self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q", None))
		self.menuInstagram.setTitle(_translate("MainWindow", "Instagram", None))
		self.actionSettings_2.setText(_translate("MainWindow", "Settings", None))
		self.actionStart_Module.setText(_translate("MainWindow", "Start Module", None))


	def open_configurations(self):
		ui2.see_keys()
		keys.show()

	def open_insta_configuration(self):
		if not os.path.exists("config_instagram.ini"):
			Keys_instagram.show()
		else:
			authentication_instagram()
			ui4.see_keys()
			Keys_instagram.show()

	def open_instagram(self):
		if not os.path.exists("config_instagram.ini"):
			Keys_instagram.show()
		else:
			authentication_instagram()
			Form.show()

	@QtCore.pyqtSlot()
	def on_pushButtonPrint_clicked(self):
		global arg_user_search
		arg_user_search = str(self.lineEdit.text())
		search_user()
		self.webView.setUrl(QtCore.QUrl("output.html"))

	def on_pushTLButtonPrint_clicked(self):
		global screen_name
		global number
		screen_name = str(self.lineEdit.text())
		number = self.lcdNumber.value()
		if maps.isChecked():
			create_map_tl()
			self.webView_2.setUrl(QtCore.QUrl("output_map.html"))
		timeline_user()
		self.webView.setUrl(QtCore.QUrl("output.html"))

	def on_pushTagButtonPrint_clicked(self):
		global TAG
		global number
		TAG = str(self.lineEdit.text())
		number = self.lcdNumber.value()
		search_tag()
		self.webView.setUrl(QtCore.QUrl("output.html"))

	def on_pushZoneButtonPrint_clicked(self):
		global ZONE
		global number
		ZONE = str(self.lineEdit.text())
		number = self.lcdNumber.value()
		if maps.isChecked():
			create_map()
			self.webView_2.setUrl(QtCore.QUrl("output_map.html"))
		search_zone_map()
		self.webView.setUrl(QtCore.QUrl("output.html"))


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	MainWindow = QtGui.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	keys = QtGui.QWidget()
	ui2 = Ui_keys()
	ui2.setupUi(keys)

	Form = QtGui.QWidget()
	ui3 = Ui_Form()
	ui3.setupUi(Form)

	Keys_instagram = QtGui.QWidget()
	ui4 = Ui_Keys_instagram()
	ui4.setupUi(Keys_instagram)

	keys.setWindowIcon(QtGui.QIcon('geotweet-icon.ico'))
	Form.setWindowIcon(QtGui.QIcon('geotweet-icon.ico'))

	app.setWindowIcon(QtGui.QIcon('geotweet-icon.ico'))
	MainWindow.setWindowIcon(QtGui.QIcon('geotweet-icon.ico'))

if not os.path.exists("config.ini"):
	keys.show()
	sys.exit(app.exec_())
else:
	authentication()
	MainWindow.show()
	sys.exit(app.exec_())

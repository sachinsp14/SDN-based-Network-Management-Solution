import httplib2
import json
import sys
import os
import crypt,getpass
from collections import OrderedDict
import time

h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')

total_links = set()
alive_links = set()
total_nodes = set()
alive_nodes = set()


print "Monitoring OpenFlow Switches.."

################################################################################################

def topo():
	url = "http://localhost:8181/restconf/operational/network-topology:network-topology"
	resp, content = h.request(url, "GET")
	portStats = json.loads(content)
	topology = portStats['network-topology']['topology'][0]
	return topology

################################################################################################

def totalLinks():
	global total_links
	total_links = set()
	t1 = topo()
	for i in range(len(t1['link'])):
		total_links.add(json.dumps(t1['link'][i]['link-id']))
		i += 1
	print "Total links active - ", len(total_links)
	return

################################################################################################

def totalNodes():
	global total_nodes
	total_nodes = set()
	t1 = topo()
	for i in range(len(t1['node'])):
		total_nodes.add(json.dumps(t1['node'][i]['node-id']))
		i += 1
	print "Total nodes active - ", len(total_nodes)
	return

################################################################################################

def checkTopo():
	t2 = topo()

	no_nodes = len(t2['node'])

	no_links = len(t2['link'])
	
	return no_nodes,no_links

################################################################################################

def trackLinksUp():	
	global total_links,alive_links
	alive_links = set()
	return_links_up = set()
	t3 = topo()

	for i in range(len(t3['link'])):
		alive_links.add(json.dumps(t3['link'][i]['link-id']))
		i += 1
	
	return_links_up = list(alive_links - total_links)
	print "Links up : \n", return_links_up
	print
	

	return	

################################################################################################

def trackLinksDown():	
	global total_links,alive_links
	alive_links = set()
	return_links_down = set()
	t3 = topo()

	for i in range(len(t3['link'])):
		alive_links.add(json.dumps(t3['link'][i]['link-id']))
		i += 1
	
	return_links_down = list(total_links - alive_links)
	print "Links down : \n", return_links_down
	print

	return	

################################################################################################

def trackNodesUp():
	global total_nodes,alive_nodes
	alive_nodes = set()
	return_nodes_up = set()
	t3 = topo()
	
	for i in range(len(t3['node'])):
		alive_nodes.add(json.dumps(t3['node'][i]['node-id']))
		i += 1
	
	return_nodes_up = list(alive_nodes - total_nodes)
	print "New nodes added : \n", return_nodes_up
	print
	
	
	return

################################################################################################

def trackNodesDown():	
	global total_nodes,alive_nodes
	alive_nodes = set()
	return_nodes_down = set()
	t3 = topo()

	for i in range(len(t3['node'])):
		alive_nodes.add(json.dumps(t3['node'][i]['node-id']))
		i += 1
	
	return_nodes_down = list(total_nodes - alive_nodes)
	print "Nodes deleted : \n", return_nodes_down
	print
	
	return		

################################################################################################

def track():
	print
	totalNodes()
	totalLinks()
	print "#####################################################################################"
	print
	while(1):	
		node1,link1 = checkTopo()
	
		time.sleep(2)

		node2,link2 = checkTopo()
	
		if(node2 > node1):
			trackNodesUp()
			print									
		elif(node2 < node1):
			trackNodesDown()
			print 
		if(link2 > link1):
			trackLinksUp()
			totalNodes()
			totalLinks()
			print "#####################################################################################"
			print
		elif(link2 < link1):
			trackLinksDown()
			totalNodes()
			totalLinks()
			print "#####################################################################################"
			print
			

track()

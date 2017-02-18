from link import *
from probe import *
from math import radians, cos, sin, asin, sqrt

AVG_EARTH_RADIUS = 6371000  # in m


def probeToLinkDist(p_lat, p_long, ref, nref):
	ref_lat = ref[0]
	ref_long = ref[1]
	nref_lat = nref[0]
	nref_long = nref[1]

	y = sin(p_long - ref_long) * cos(p_lat)
	x = cos(ref_lat) * sin(p_lat) - sin(ref_lat) * cos(p_lat) * cos(p_lat - ref_lat)
	bearing1 = map(radians, atan2(y, x))
	bearing1 = 360 - ((bearing1 + 360) % 360)

	y2 = sin(nref_long - ref_long) * cos(nref_lat)
	x2 = cos(ref_lat) * sin(nref_lat) - sin(ref_lat) * cos(nref_lat) * cos(nref_lat - ref_lat)
	bearing2 = map(radians, atan2(y2, x2))
	bearing2 = 360 - ((bearing2 + 360) % 360)

	ref_Rads = map(radians, ref_lat);
	p_Rads = map(radians, p_lat)
	dLon = map(radians, p_long - ref_long)

	distanceAC = acos(sin(ref_Rads) * sin(p_Rads)+cos(ref_Rads)*cos(p_Rads)*cos(dLon)) * AVG_EARTH_RADIUS
	min_distance = fabs(asin(sin(distanceAC/AVG_EARTH_RADIUS)*sin(map(radians, bearing1)-map(radians, bearing2))) * AVG_EARTH_RADIUS)
	return min_distance


def getCandidates(probe_pt, link_list, r):
	candidate_list = list()
	probe_lat = probe_pt.latitude
	probe_long = probe_pt.longitude
	for x in link_list:
		ref_pt = x.RefNode
		nref_pt = x.NrefNode
		dist = probeToLinkDist(probe_lat, probe_long, ref_pt, nref_pt)
		if(dist < r):
			candidate_list.append(x)
	return candidate_list
		
if __name__ == "__main__":

	all_links = list()
	all_probes = list()
	link_file = "Partition6467LinkData.csv"
	probe_file = "Partition6467ProbePoints.csv"
	
	with open(probe_file) as f:
		for line in f:
			print line
			curr_probe = Probe(line)
			all_probes.append(curr_probe)
			
	with open(link_file) as f:
		for line in f:
			curr_link = Link(line)
			all_links.append(curr_link)
						
	print(all_links[0].RefNode[0])
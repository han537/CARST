#!/usr/bin/python


# highRezKML.py
# Author: Andrew Kenneth Melkonian
# All rights reserved

# Usage
# *****
# python highRezKML.py /path/to/browse_image-BROWSE.jpg
#	/path/to/browse_image-BROWSE.jpg - path to the browse image, must end in "-BROWSE"
# NOTE: xml file MUST be in same directory as the browse image and MUST have the same name (without the "-BROWSE" and with a "xml" extension)



def highRezKML(browse_jpg_path):

	import os;
	import re;
	import subprocess;

	# Check that browse image given actually exists

	assert os.path.exists(browse_jpg_path), "\n***** ERROR: " + browse_jpg_path + " does not exist\n";

	print(browse_jpg_path);

	# Get directory, name of image (without "-BROWSE", for finding xml)

	browse_dir = ".";

	index = browse_jpg_path.rfind("/");

	if index > -1:
		browse_dir = browse_jpg_path[ : index];

	name = browse_jpg_path[browse_jpg_path.rfind("/") + 1 : browse_jpg_path.rfind("-BROWSE")];


	# xml file should be in the same directory as the browse image, should be the name of the browse image without the "-BROWSE"

	xml_path = browse_dir + "/" + name + ".xml";

	# Check that xml file exists

#	assert os.path.exists(xml_path), "\n***** ERROR: " + xml_path + " does not exist\n";
	if os.path.exists(xml_path):

# 	Get corner coordinates from xml file

		xml_file = open(xml_path, "r");
		coords   = 8;
		ul_lon   = "";
		ul_lat   = "";
		ll_lon   = "";
		ll_lat   = "";
		ur_lon   = "";
		ur_lat   = "";
		lr_lon   = "";
		lr_lat   = "";

		for line in xml_file:

			if re.search("ULLAT",line):
				index1 = re.search("<ULLAT>",line).end(0);
				index2 = re.search("</ULLAT>",line).start(0);
				ul_lat = line[index1 : index2];
				coords -= 1;

			elif re.search("ULLON",line):
				index1 = re.search("<ULLON>",line).end(0);
				index2 = re.search("</ULLON>",line).start(0);
				ul_lon = line[index1 : index2];
				coords -= 1;

			elif re.search("URLAT",line):
				index1 = re.search("<URLAT>",line).end(0);
				index2 = re.search("</URLAT>",line).start(0);
				ur_lat = line[index1 : index2];
				coords -= 1;

			elif re.search("URLON",line):
				index1 = re.search("<URLON>",line).end(0);
				index2 = re.search("</URLON>",line).start(0);
				ur_lon = line[index1 : index2];
				coords -= 1;

			elif re.search("LRLAT",line):
				index1 = re.search("<LRLAT>",line).end(0);
				index2 = re.search("</LRLAT>",line).start(0);
				lr_lat = line[index1 : index2];
				coords -= 1;

			elif re.search("LRLON",line):
				index1 = re.search("<LRLON>",line).end(0);
				index2 = re.search("</LRLON>",line).start(0);
				lr_lon = line[index1 : index2];
				coords -= 1;

			elif re.search("LLLAT",line):
				index1 = re.search("<LLLAT>",line).end(0);
				index2 = re.search("</LLLAT>",line).start(0);
				ll_lat = line[index1 : index2];
				coords -= 1;

			elif re.search("LLLON",line):
				index1 = re.search("<LLLON>",line).end(0);
				index2 = re.search("</LLLON>",line).start(0);
				ll_lon = line[index1 : index2];
				coords -= 1;

			if coords  ==  0:
				break;

		xml_file.close();

	else:

#		Run gdalinfo on ntf file to find corner coordinates	
		ntf_path = xml_path.replace(".xml", ".ntf");

# 		Check that xml file exists
		assert os.path.exists(ntf_path), "\n***** ERROR: " + ntf_path + " does not exist\n";

		cmd  = "\ngdalinfo " + ntf_path + "\n";
		pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout;
		info = pipe.read();
		pipe.close();

		ul_lon_dms = info[re.search("Upper\s*Left\s*\(\s*\d+\.*\d*,\s*\d+\.*\d*\)\s*\(", info).end(0) : ];
		ul_lat_dms = ul_lon_dms[re.search(",", ul_lon_dms).start(0) + 1 : re.search("\)", ul_lon_dms).end(0) - 1];
		ul_lon_dms = ul_lon_dms[ : re.search(",", ul_lon_dms).end(0) - 1];
		ul_lon_d   = ul_lon_dms[ : re.search("\d+", ul_lon_dms).end(0)];
		ul_lon_m   = ul_lon_dms[re.search("d\s*", ul_lon_dms).end(0) : re.search("\d+'", ul_lon_dms).end(0) - 1];
		ul_lon_s   = ul_lon_dms[re.search("'", ul_lon_dms).end(0) : re.search("\"", ul_lon_dms).end(0) - 1];
		ul_lat_d   = ul_lat_dms[ : re.search("\s*\d*", ul_lat_dms).end(0)];
		ul_lat_m   = ul_lat_dms[re.search("d\s*", ul_lat_dms).end(0) : re.search("\d+'", ul_lat_dms).end(0) - 1];
		ul_lat_s   = ul_lat_dms[re.search("'", ul_lat_dms).end(0) : re.search("\"", ul_lat_dms).end(0) - 1];

		ll_lon_dms = info[re.search("Lower\s*Left\s*\(\s*\d+\.*\d*,\s*\d+\.*\d*\)\s*\(", info).end(0) : ];
		ll_lat_dms = ll_lon_dms[re.search(",", ll_lon_dms).start(0) + 1 : re.search("\)", ll_lon_dms).end(0) - 1];
		ll_lon_dms = ll_lon_dms[ : re.search(",", ll_lon_dms).end(0) - 1];
		ll_lon_d   = ll_lon_dms[ : re.search("\d+", ll_lon_dms).end(0)];
		ll_lon_m   = ll_lon_dms[re.search("d\s*", ll_lon_dms).end(0) : re.search("\d+'", ll_lon_dms).end(0) - 1];
		ll_lon_s   = ll_lon_dms[re.search("'", ll_lon_dms).end(0) : re.search("\"", ll_lon_dms).end(0) - 1];
		ll_lat_d   = ll_lat_dms[ : re.search("\s*\d*", ll_lat_dms).end(0)];
		ll_lat_m   = ll_lat_dms[re.search("d\s*", ll_lat_dms).end(0) : re.search("\d+'", ll_lat_dms).end(0) - 1];
		ll_lat_s   = ll_lat_dms[re.search("'", ll_lat_dms).end(0) : re.search("\"", ll_lat_dms).end(0) - 1];

		ur_lon_dms = info[re.search("Upper\s*Right\s*\(\s*\d+\.*\d*,\s*\d+\.*\d*\)\s*\(", info).end(0) : ];
		ur_lat_dms = ur_lon_dms[re.search(",", ur_lon_dms).start(0) + 1 : re.search("\)", ur_lon_dms).end(0) - 1];
		ur_lon_dms = ur_lon_dms[ : re.search(",", ur_lon_dms).end(0) - 1];
		ur_lon_d   = ur_lon_dms[ : re.search("\d+", ur_lon_dms).end(0)];
		ur_lon_m   = ur_lon_dms[re.search("d\s*", ur_lon_dms).end(0) : re.search("\d+'", ur_lon_dms).end(0) - 1];
		ur_lon_s   = ur_lon_dms[re.search("'", ur_lon_dms).end(0) : re.search("\"", ur_lon_dms).end(0) - 1];
		ur_lat_d   = ur_lat_dms[ : re.search("\s*\d*", ur_lat_dms).end(0)];
		ur_lat_m   = ur_lat_dms[re.search("d\s*", ur_lat_dms).end(0) : re.search("\d+'", ur_lat_dms).end(0) - 1];
		ur_lat_s   = ur_lat_dms[re.search("'", ur_lat_dms).end(0) : re.search("\"", ur_lat_dms).end(0) - 1];

		lr_lon_dms = info[re.search("Lower\s*Right\s*\(\s*\d+\.*\d*,\s*\d+\.*\d*\)\s*\(", info).end(0) : ];
		lr_lat_dms = lr_lon_dms[re.search(",", lr_lon_dms).start(0) + 1 : re.search("\)", lr_lon_dms).end(0) - 1];
		lr_lon_dms = lr_lon_dms[ : re.search(",", lr_lon_dms).end(0) - 1];
		lr_lon_d   = lr_lon_dms[ : re.search("\d+", lr_lon_dms).end(0)];
		lr_lon_m   = lr_lon_dms[re.search("d\s*", lr_lon_dms).end(0) : re.search("\d+'", lr_lon_dms).end(0) - 1];
		lr_lon_s   = lr_lon_dms[re.search("'", lr_lon_dms).end(0) : re.search("\"", lr_lon_dms).end(0) - 1];
		lr_lat_d   = lr_lat_dms[ : re.search("\s*\d*", lr_lat_dms).end(0)];
		lr_lat_m   = lr_lat_dms[re.search("d\s*", lr_lat_dms).end(0) : re.search("\d+'", lr_lat_dms).end(0) - 1];
		lr_lat_s   = lr_lat_dms[re.search("'", lr_lat_dms).end(0) : re.search("\"", lr_lat_dms).end(0) - 1];

		ul_lon = str(float(ul_lon_d) + float(ul_lon_m) / 60. + float(ul_lon_s) / 3600.); 

		if ul_lon_dms.find("W") > -1:
			ul_lon = "-" + ul_lon;

		ul_lat = str(float(ul_lat_d) + float(ul_lat_m) / 60. + float(ul_lat_s) / 3600.); 

		if ul_lat_dms.find("S") > -1:
			ul_lat = "-" + ul_lat;

		ll_lon = str(float(ll_lon_d) + float(ll_lon_m) / 60. + float(ll_lon_s) / 3600.); 

		if ll_lon_dms.find("W") > -1:
			ll_lon = "-" + ll_lon;

		ll_lat = str(float(ll_lat_d) + float(ll_lat_m) / 60. + float(ll_lat_s) / 3600.); 

		if ll_lat_dms.find("S") > -1:
			ll_lat = "-" + ll_lat;

		ur_lon = str(float(ur_lon_d) + float(ur_lon_m) / 60. + float(ur_lon_s) / 3600.); 

		if ur_lon_dms.find("W") > -1:
			ur_lon = "-" + ur_lon;

		ur_lat = str(float(ur_lat_d) + float(ur_lat_m) / 60. + float(ur_lat_s) / 3600.); 

		if ur_lat_dms.find("S") > -1:
			ur_lat = "-" + ur_lat;

		lr_lon = str(float(lr_lon_d) + float(lr_lon_m) / 60. + float(lr_lon_s) / 3600.); 

		if lr_lon_dms.find("W") > -1:
			lr_lon = "-" + lr_lon;

		lr_lat = str(float(lr_lat_d) + float(lr_lat_m) / 60. + float(lr_lat_s) / 3600.); 

		if lr_lat_dms.find("S") > -1:
			lr_lat = "-" + lr_lat;


#	***** Create trimmed browse image in current directory

#	***** Absolute path
#	jpg_trim_path = browse_dir + "/" + name + "-BROWSE_trimmed.jpg";
#	***** Relative Path
	jpg_trim_path = name + "-BROWSE_trimmed.jpg";

	if os.path.exists(jpg_trim_path):
		print("\n***** WARNING: \"" + jpg_trim_path + "\" already exists, skipping this image...\n");
		return;

	cmd = "\nconvert -trim " + browse_jpg_path + " " + jpg_trim_path + "\n";
	subprocess.call(cmd,shell=True);


	# Create kml file in current directory

	kml_file = open(browse_dir + "/" + name + ".kml" ,"w");
	kml_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n");
	kml_file.write("<kml xmlns=\"http://earth.google.com/kml/2.1\"\n");
	kml_file.write(" xmlns:gx=\"http://www.google.com/kml/ext/2.2\">\n");
	kml_file.write("<Document>\n");
	kml_file.write("<name>" + name + "</name>\n");
	kml_file.write("<open>1</open>\n");
	kml_file.write("<GroundOverlay>\n");
	kml_file.write("<name>" + name + "</name>\n");
	kml_file.write("<description>" + name + "</description>\n");
	kml_file.write("<Icon>\n");
	kml_file.write("<href>" + jpg_trim_path + "</href>\n");
	kml_file.write("<viewBoundScale>0.75</viewBoundScale>\n");
	kml_file.write("</Icon>\n");
	kml_file.write("<gx:LatLonQuad>\n");
	kml_file.write("<coordinates>" + ll_lon + "," + ll_lat + " " + lr_lon + "," + lr_lat + " " + ur_lon + "," + ur_lat + " " + ul_lon + "," + ul_lat + "</coordinates>\n");
	kml_file.write("</gx:LatLonQuad>\n");
	kml_file.write("</GroundOverlay>\n");
	kml_file.write("</Document>\n");
	kml_file.write("</kml>\n");
	kml_file.close();


	return;



if __name__ == "__main__":
	
	import os;
	import sys;
	
	assert len(sys.argv) > 1, "\n***** ERROR: highRezKML.py requires 1 argument, " + str(len(sys.argv) - 1) + " given\n";
	assert os.path.exists(sys.argv[1]), "\n***** ERROR: " + sys.argv[1] + " does not exist\n";
	
	highRezKML(sys.argv[1]);

	exit();




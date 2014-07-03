from lxml import etree
from flask import Flask
import json
app = Flask(__name__)

LINES_DICT = {'123': ['1', '2', '3'],
	      '456': ['4', '5', '6'],
   	      'ACE': ['A', 'C', 'E'],
              'BDFM': ['B', 'D', 'F', 'M'],
              'JZ': ['J', 'Z'],
              'NQR': ['N', 'Q', 'R'] }

@app.route('/<line>')
def subway_status(line):
    line = line.upper()
    for key, value in LINES_DICT.iteritems():
        if line in value:
            line = key
    xml_base =  etree.parse("http://web.mta.info/status/serviceStatus.txt")
    root = xml_base.getroot()
    #move the above to an in memory db, fetch every 5 minutes and update
    last_updated = root[1].text
    for subway_element in root[2]:
        subway_line = subway_element[0].text
	if line == subway_line:
            subway_service_status = subway_element[1].text
	    data = { 'subway_line' : line,
		      'status' : subway_service_status,
		      'updated_at' : last_updated
		   }
            json_data = json.dumps(data)
	    return json_data
           
def get_best_route(preferred_subway_lines):
    """
    Take in a list of lines, and only return those that are in good service
    """
    if len(preferred_subway_lines) == 1:
        #Return that there is only one route
	return str('Please add multiple routes')
    for line in preferred_subway_lines:
	line = line.upper()
        subway_service_status = subway_status(line)
	if subway_service_status == "GOOD SERVICE":
	    print 'Status for {} is {}'.format(line, subway_service_status)
	else:
	    print 'Status for {} is {}'.format(line, subway_service_status)
if __name__ == '__main__':
    app.run()

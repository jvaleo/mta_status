from lxml import etree
from flask import Flask
app = Flask(__name__)

@app.route('/<line>')
def subway_status(line):
    line = line.upper()
    xml_base =  etree.parse("http://web.mta.info/status/serviceStatus.txt")
    root = xml_base.getroot()
    #move the above to an in memory db, fetch every 5 minutes and update
    last_updated = root[1].text
    for subway_element in root[2]:
        subway_line = subway_element[0].text
	if line == subway_line:
            subway_service_status = subway_element[1].text
	    return subway_service_status

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

from lxml import etree

def subway_status():
    xml_base = tree = etree.parse("http://web.mta.info/status/serviceStatus.txt")
    root = xml_base.getroot()
    last_updated = root[1].text
    for subway_element in root[2]:
        subway_line = subway_element[0].text
	subway_service_status = subway_element[1].text
	return last_updated, subway_line, subway_service_status

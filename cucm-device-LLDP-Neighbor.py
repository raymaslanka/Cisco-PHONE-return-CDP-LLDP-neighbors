# This returns LLDP or CDP neighbor info retrieved from one or more Cisco CUCM endpoints
# by querying the devices internal web servers
# The device / webserver addresses are stored in a text file you are prompted for.

import requests
from bs4 import BeautifulSoup

def get_switch_info(device_IP):
    # get HTML info from device
    try:
        data = requests.get('http://' + device_IP +'/CGI/Java/Serviceability?adapter=device.statistics.port.network', timeout=2)
    # catch any issues connecting to devices
    # might be wise to catch different types of errors
    except requests.exceptions.RequestException as e:
        print('Something bad happened retrieving info from ' + device_IP)
        print(e)
        return
    # data = requests.get('http://' + device_IP +'/CGI/Java/Serviceability?adapter=device.statistics.port.network')
    # parse the HTML
    soup = BeautifulSoup(data.text, 'html.parser')
    #find all the <tr> elements in the HTML
    my_values = list()
    for tr in soup.find_all('tr'):
        # create a list of the <td> text in each of the <tr>
        values = [td.text for td in tr.find_all('td')]
        # find the <td> we are interested in and
        if values[0]==" LLDP Neighbor device ID":
            # print(values[2])
            my_values.append(values[2])
        if values[0]==" LLDP Neighbor port":
            # print(values[2])
            my_values.append(values[2])
    return my_values

# read file
filename = input('IP input filename:')
fhand = open(filename)

for line in fhand:
    line = line.strip()
    print(line)
    # get switch name and port from device web interface
    switch_info = get_switch_info(line)
    if switch_info != None:
        print(switch_info)

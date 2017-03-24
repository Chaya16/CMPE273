import httplib
import json
from hashing import ConsistentHashRing
cr = ConsistentHashRing()

    
nodes=["192.168.99.100:5001", "192.168.99.100:5002", "192.168.99.100:5003"]

cr["node1"]=nodes[0]
cr["node2"]=nodes[1]
cr["node3"]=nodes[2]

for i in xrange(1,11):
    url1 = cr.__getitem__(str(i))
    
    print url1
    connection = httplib.HTTPConnection(url1)

    headers = {'Content-type': 'application/json'}

    data = {
    "id": i,
    "name" : "Foo Bar %d" %i,
    "email" : "foo %d" %i + "@bar.com",
    "category" : "office supplies",
    "description" : "iPad for office use",
    "link" : "http://www.apple.com/shop/buy-ipad/ipad-pro",
    "estimated_costs" : "800",
    "submit_date" : "12-10-2016"
    }
    dataDict = json.dumps(data)
    url2 = "/v1/expenses/%d" %i
    print url2
    connection.request('POST', url2, dataDict, headers)
    response = connection.getresponse()
    print(response.read().decode())

results = [{'name': 'Yakijo', 'type': 'Shoes', 'address_1': '26310 Victoria Junction', 'address_2': 'Leeds', 'address_3': 'England', 'postcode': 'LS6 1AD', 'telephone': '0586 722 3525', 'latitude': 53.817675, 'longitude': -1.575675, 'distance': 275}, {'name': 'Youtags', 'type': 'Shoes', 'address_1': '0735 Forest Place', 'address_2': 'London', 'address_3': 'England', 'postcode': 'EC3M 1AA', 'telephone': '0275 410 2565', 'latitude': 51.510603, 'longitude': -0.085599, 'distance': 3}, {'name': 'Topicshots', 'type': 'Shoes', 'address_1': '666 Sommers Pass', 'address_2': 'Norton', 'address_3': 'England', 'postcode': 'S8 0FA', 'telephone': '0909 447 0860', 'latitude': 53.338804, 'longitude': -1.495392, 'distance': 224}, {'name': 'Browsebug', 'type': 'Shoes', 'address_1': '312 Superior Junction', 'address_2': 'Stapleford', 'address_3': 'England', 'postcode': 'LN6 0AD', 'telephone': '0761 544 7604', 'latitude': 53.210895, 'longitude': -0.576468, 'distance': 192}]

# hello = sorted(results[0].items(), key=lambda kv:kv[10])

for item in results:
    print(type(item))

newlist = sorted(results, key=lambda k: k['distance'])
print(newlist)

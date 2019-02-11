
import pysqlite3, os, requests
from math import sin, cos, sqrt, atan2, radians


def check_database(db_path):
    if os.path.exists(db_path):
        return True
    else:
        return False


def get_database():
    try:
        conn = pysqlite3.connect('db/phonebook.db')
        cursor = conn.cursor()
        return conn, cursor
    except FileNotFoundError:
        return False


def close_database(cursor, conn):
    cursor.close()
    conn.close()
    return


def query_database(query, value):
    conn, cursor = get_database()
    # cursor.execute(query, value)
    # results = cursor.fetchall()
    results = cursor.execute(query, value).fetchall()
    close_database(cursor, conn)
    return results


def show_business_types():
    select_query = "SELECT DISTINCT business_category FROM business ORDER BY business_category"
    results = query_database(select_query, "")

    types = []
    for item in results:
        types.append(item[0])
        print(item[0], end=', ')

    return types


def get_lat_lon(location):
    endpoint = "https://api.opencagedata.com/geocode/v1/json"
    payload = {"q": location, "key": "054ed13663c94c4791d1806b7b14fd71"}
    response = requests.get(endpoint, params=payload)
    data = response.json()

    lat = ""
    lon = ""

    if data['status']['code'] == 200 and (data['total_results'] > 0):
        if data['results'][0]['components']['country_code'] == 'gb':
            lat = data['results'][0]['geometry']['lat']
            lon = data['results'][0]['geometry']['lng']

    return lat, lon


def distance_haversine(lat1, lon1, lat2, lon2):
    radius = 6371 # km
    lat = radians(lat2 - lat1)
    lon = radians(lon2 - lon1)
    sins_lat = sin(lat/2) * sin(lat/2)
    sins_lon = sin(lon/2) * sin(lon/2)
    cosinus = cos(radians(lat1)) * cos(radians(lat2))
    a = sins_lat + cosinus * sins_lon
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = radius * c
    return round(distance)


def get_locations(results, location):
    """
    If a biz_location was given then find lat/lang for that.
    """
    print('in/near {}'.format(location))
    lat, lon = get_lat_lon(location)

    i = 0
    for item in results:
        if ("" != lat) and ("" != lon):
            # lat = 53.817675
            # lon = -1.575675
            # item[-1] = distance_haversine(item[8], item[9], lat, lon)
            item['distance'] = distance_haversine(item['latitude'], item['longitude'], lat, lon)

        i += 1

    return sorted(results, key=lambda k: k['distance'])


def tuple_to_dictionary(results, table):
    """
    Convert the tuple list elements into dictionaries.
    That way you can append a distance value to update if applicable.
    And it will be easier to display with Flask too.
    """
    converted = []
    for item in results:
        dictionary = {}
        if "business" == table:
            dictionary['name'] = item[0]
            dictionary['type'] = item[1]

        elif "people" == table:
            dictionary['first_name'] = item[0]
            dictionary['last_name'] = item[1]

        dictionary['address_1'] = item[2]
        dictionary['address_2'] = item[3]
        dictionary['address_3'] = item[4]
        dictionary['postcode'] = item[5]
        dictionary['telephone'] = item[6]
        dictionary['latitude'] = item[8]
        dictionary['longitude'] = item[9]
        dictionary['distance'] = ""
        converted.append(dictionary)

    return converted


# def convert_to_lists(results):
#     """
#     Convert the tuple list elements into normal lists.
#     That way you can append a distance value to update if applicable.
#     """
#     i = 0
#     for item in results:
#         results[i] = list(item)
#         results[i].append("")
#         i += 1
#
#     return results


def process_results(results, location, table):
    if len(results) > 0:
        # results = convert_to_lists(results)
        results = tuple_to_dictionary(results, table)
        if location:
            return get_locations(results, location)
    return results


def search_business_type(biz_type, location=None):
    """
    Results is a list with businesses and their lat/lang.
    For each item, decide how far it is from location given.
    Append result list with distance.
    Sort result list by distance.
    """
    select_query = "SELECT * FROM business INNER JOIN postcodes ON (business.postcode = postcodes.postcode) WHERE business.business_category = ?"
    value_query = (biz_type, )
    results = query_database(select_query, value_query)

    print('... Looking for {} '.format(biz_type), end='')
    return process_results(results, location, "business")


def search_business_name(biz_name, location=None):
    """
    Results is a list with businesses and their lat/lang.
    For each item, decide how far it is from location given.
    Append result list with distance.
    Sort result list by distance.
    """
    select_query = "SELECT * FROM business INNER JOIN postcodes ON (business.postcode = postcodes.postcode) WHERE business.business_name LIKE ?"
    value_query = ("%"+biz_name+"%", )
    results = query_database(select_query, value_query)

    print('... Looking for {} '.format(biz_name), end='')
    return process_results(results, location, "business")


def search_people(person_name, location=None):
    """
    Results is a list with people and their lat/lang.
    For each item, decide how far it is from location given.
    Append result list with distance.
    Sort result list by distance.
    """
    select_query = "SELECT * FROM people INNER JOIN postcodes ON (people.postcode = postcodes.postcode) WHERE people.last_name LIKE ?"
    value_query = ("%"+person_name+"%", )
    results = query_database(select_query, value_query)

    print('... Looking for {} '.format(person_name), end='')
    return process_results(results, location, "people")


def print_results(kind, results, location):
    """
    Results is a list with results in order of the
    distance to the requested location.
    """

    if results:
        if len(results) > 1:
            plural = 's'
        else:
            plural = ''

        print('\nFound {} result{}'.format(len(results), plural), end=" ")
        if "" != results[0]['distance']:
            print('near {}\n-----'.format(location))
        else:
            print('\nNo location given\n-----')

        for item in results:
            if "" != item['distance']:
                print('{}km - '.format(item['distance']), end='')

            if 'business' == kind:
                print('{}, {}, {}, {}, {}'.format(item['name'], item['address_1'], item['address_2'], item['postcode'], item['telephone']))
            elif 'person' == kind:
                print('{}, {}, {}, {}, {}, {}'.format(item['first_name'], item['last_name'], item['address_1'], item['address_2'], item['postcode'], item['telephone']))

    else:
        print('-----\nNothing was found.')

    # print('And these are related searches')
    # print('\n-----')
    # print('(alpha) Sort results alphabetically')
    # print('(geo) Sort results geographically')



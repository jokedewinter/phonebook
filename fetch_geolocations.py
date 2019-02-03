
import pysqlite3
import requests

conn = pysqlite3.connect('db/phonebook5.db')
cursor = conn.cursor()


def remove_spaces(text):
	return text.replace(" ", "")


def call_postcode_api(postcode):
	postcode_short = remove_spaces(postcode)
	endpoint = "https://api.postcodes.io/postcodes/"
	response = requests.get(endpoint + postcode_short)
	data = response.json()
	if response.status_code == 200:
		insert_query = "INSERT INTO postcodes(postcode, latitude, longitude) VALUES(?, ? , ?)"
		insert_values = (postcode, data['result']['latitude'], data['result']['longitude'])
		cursor.execute(insert_query, insert_values)
		conn.commit()
	return


def check_postcode_exists(postcode):
	select_query = "SELECT * FROM postcodes WHERE postcode = ?"
	cursor.execute(select_query, (postcode, ))

	if not cursor.fetchone():
		call_postcode_api(postcode)
	return


def read_data_tables(table_type):
	if 'people' == table_type:
		print('browse people table')
		cursor.execute('SELECT postcode FROM people')
		for row in cursor.fetchall():
			check_postcode_exists(row[0])

	elif 'business' == table_type:
		print('browse business table')
		cursor.execute('SELECT postcode FROM business')
		for row in cursor.fetchall():
			check_postcode_exists(row[0])


def create_postcode_table():
	cursor.execute('CREATE TABLE IF NOT EXISTS postcodes(postcode TEXT, latitude INT, longitude INT)')
	print('create postcodes table')


create_postcode_table()
read_data_tables('people')
read_data_tables('business')

cursor.close()
conn.close()





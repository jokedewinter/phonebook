
import pysqlite3
import json

conn = pysqlite3.connect('db/phonebook.db')
cursor = conn.cursor()


def read_json_file(json_file, file_type):
	with open(json_file) as file:
		data = json.load(file)
		for row in data:
			if 'people' == file_type:
				cursor.execute('INSERT INTO people(first_name, last_name, address_line_1, address_line_2, address_line_3, postcode, telephone) VALUES(?, ?, ?, ?, ?, ?, ?)', (row['first_name'], row['last_name'], row['address_line_1'], row['address_line_2'], row['address_line_3'], row['postcode'], row['telephone_number']))
			elif 'business' == file_type:
				cursor.execute('INSERT INTO business(business_name, business_category, address_line_1, address_line_2, address_line_3, postcode, telephone) VALUES(?, ?, ?, ?, ?, ?, ?)', (row['business_name'], row['business_category'], row['address_line_1'], row['address_line_2'], row['address_line_3'], row['postcode'], row['telephone_number']))

			conn.commit()


def create_tables():
	cursor.execute('CREATE TABLE IF NOT EXISTS people(first_name TEXT, last_name TEXT, address_line_1 TEXT, address_line_2 TEXT, address_line_3 TEXT, postcode TEXT, telephone TEXT)')
	cursor.execute('CREATE TABLE IF NOT EXISTS business(business_name TEXT, business_category TEXT, address_line_1 TEXT, address_line_2 TEXT, address_line_3 TEXT, postcode TEXT, telephone TEXT)')


create_tables()
read_json_file('json/mock_data_people.json', 'people')
read_json_file('json/mock_data_business.json', 'business')


cursor.close()
conn.close()

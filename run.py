
from search import *


def kick_off():
	print('PHONE BOOK SEARCH\n----------------')
	print('(a) Find a Business by type or name')
	print('(b) Find a Person')

	bp_answer = ("a", "b")
	business_or_person = ""
	while business_or_person not in bp_answer:
		business_or_person = input()
		if 'a' == business_or_person.lower():
			business_search()
		elif 'b' == business_or_person.lower():
			person_search()
		else:
			print('Please choose (a) or (b)')


def business_search():
	print('\nBusiness search\n----------------')
	print('(c) by Business Type (default)')
	print('(d) by Business name')

	bc_answer = ("c", "d")
	business_choice = ""
	while business_choice not in bc_answer:
		business_choice = input()

		if 'c' == business_choice.lower():
			print('Available business types:\n----------------')
			types = show_business_types()
			print('\n----------------')
			biz_type, location = get_business_type(types)
			results = search_business_type(biz_type, location)
			print_results('business', results, location)

		elif 'd' == business_choice.lower():
			biz_name, location = get_business_name()
			results = search_business_name(biz_name, location)
			print_results('business', results, location)

		else:
			print('Please choose (c) or (d)')
	search_again()


def get_business_type(types):
	biz_type = ""
	while biz_type == "":
		biz_type = input('Business Type: ').strip()
		if biz_type or (biz_type.title() in types):
			location = get_location()
			return biz_type.title(), location
		else:
			print('Please enter a valid Business Type')


def get_business_name():
	biz_name = ""
	while biz_name == "":
		try:
			biz_name = input('Business Name: ').strip()
			if biz_name:
				location = get_location()
				return biz_name.title(), location
		except ValueError:
			print('Please enter a Business Name')


def person_search():
	print('\nPerson search\n----------------')

	person_name, location = get_person_name()
	results = search_people(person_name, location)
	print_results('person', results, location)
	search_again()


def get_person_name():
	person_name = ""
	while person_name == "":
		try:
			person_name = input('Surname Name: ').strip()
			if person_name:
				location = get_location()
				return person_name.title(), location
		except ValueError:
			print('Please enter a Surname')


def get_location():
	biz_location = input('Location: ')
	return biz_location


def search_again():
	print('SEARCH AGAIN?\n----------------')
	print('(y) Yes')
	print('(n) No')

	again = input()
	if 'y' == again.lower():
		kick_off()
	else:
		print('Goodbye')


if __name__ == "__main__":
	kick_off()

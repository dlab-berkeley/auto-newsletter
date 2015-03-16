import urllib2, bs4


def training_html():
	url = 'http://dlab.berkeley.edu/training'
	page = bs4.BeautifulSoup(urllib2.urlopen(url).read())


def pull_titles(content):
	"""
	Return a list of all the event titles on the D-Lab training page.
	"""
	return content.find_all('div', class_ = 'title')


def pull_dates(content):
	"""
	This pulls and returns training dates in the following format:
		Thu, January 1, 2015 - 9:00 AM to 10:00 AM
	The values are text. Additional parsing needed to put into Python date format.
	"""
	return content.find_all('span', class_ = 'date-display-single')

def status(content):
	""" This returns the registration status, whether it's 'waiting list'(full) or 'register'(has vacancies)"""
	return content.find_all('a', class_ = 'register-link')
	
url = 'http://dlab.berkeley.edu/training'
page = bs4.BeautifulSoup(urllib2.urlopen(url).read())
for word in status(page):
	print(word)


def main():
	pass


if __name__ == '__main__':
	main()

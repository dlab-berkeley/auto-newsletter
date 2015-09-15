import requests, datetime, pdb, re

from bs4 import BeautifulSoup


class Training:
	def __init__(self, title, instructor, dateAndTime, status, link, description):
		self.title = title
		self.instructor = instructor
		self.date = dateAndTime
		self.status = status
		self.link = link
		self.description = description


def pullTitle(training):
	"""
	Return the title of the specific training.
	"""
	return training.find('div', class_ = 'title')

def pullDate(training):
	"""
	This pulls and returns training dates in the following format:
		Thu, January 1, 2015 - 9:00 AM to 10:00 AM
	The values are text. Additional parsing needed to put into Python date format.
	"""
	trainingSchedule = training.find('div', class_ = 'views-field views-field-field-schedule')
	schedule = trainingSchedule.find_all('span', 'date-display-single')
	dates = []
	for s in schedule:
		dates += [s.text]
	return dates

def pullInstructor(training):
	"""
	Return the instructor for the specific training.
	"""
	instructors = training.find('div', class_ = 'views-field views-field-field-trainer')
	return instructors.find('div', class_ = 'field-content')

def pullStatus(training):
	"""
	Return whether the training is full or not
	"""
	trainingStatus = training.find('div', class_ = 'views-field views-field-field-training-status')
	reStatus = trainingStatus.find('a', class_ = 'register-link')
	return reStatus.text, reStatus.get('href')

def pullDescription(training):
	"""
	Return the description of the training from the specific training webpage
	"""
	titlePart = pullTitle(training)
	url = 'http://dlab.berkeley.edu'
	pageLink = url + titlePart.find('a').get('href')
	r = requests.get(pageLink)
	soup = BeautifulSoup(r.content, 'html.parser')
	descriptionPart = soup.find_all('div', class_ = 'field field-name-body field-type-text-with-summary field-label-hidden')[1]
	return descriptionPart.find('div', class_ = 'field-item even').text
	
def fileOutput(trainings):
	"""
	Write all the training infomation to the file weeklyNewsletter.txt
	"""
	f = open('weeklyNewsletter.txt', 'w')
	for training in trainings:
		f.write('\n')
		f.write(training.title + '\n')
		f.write('\n')
		f.write('Instructor(s): ' + training.instructor + '\n')
		f.write('\n')
		f.write('Date and Time: ' + training.date[0] + '\n')
		if len(training.date) > 1:
			for d in training.date[1:]:
				f.write('               ' + d + '\n')
		f.write('\n')
		f.write('Description: ' + '\n')
		f.write(training.description + '\n')
		f.write('Training Status: ' + training.status + '\n')
		f.write('Training Link: ' + training.link + '\n')
		f.write('\n' + '-----------------------------' + '\n')
	f.close()

def main():
	url = 'http://dlab.berkeley.edu/training'
	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'html.parser')
	content = soup.find_all('div', class_ = 'view-content')[1]
	ts = []
	today = datetime.datetime.today().isoweekday()
	startDate = datetime.date.today() + datetime.timedelta(days = 5 - today)

	# startDate = datetime.date(2015, 9, 14)
	
	endDate = startDate + datetime.timedelta(days = 14)
	for training in content.children:
		# pdb.set_trace()
		try:
			title = pullTitle(training).text
			instructor = pullInstructor(training).text
			status, link = pullStatus(training)
			description = pullDescription(training)
			dates = pullDate(training)
			firstDate = datetime.datetime.strptime(re.search(r'.+\d{4}', dates[0]).group(0), '%a, %B %d, %Y')
			lastDate = datetime.datetime.strptime(re.search(r'.+\d{4}', dates[len(dates) - 1]).group(0), '%a, %B %d, %Y')
			if (firstDate.date() >= startDate) and (lastDate.date() <= endDate):
				t = Training(title, instructor, dates, status, link, description)
				ts += [t]
		except:
			pass

	fileOutput(ts)

if __name__ == '__main__':
	main()

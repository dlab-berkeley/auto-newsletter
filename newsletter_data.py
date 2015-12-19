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

def fileOutput(trainings, fileName):
	"""
	Write all the training infomation to the file
	"""
	f = open(fileName, 'w')
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
		if fileName == 'current_trainings.txt':
			f.write('Description: ' + '\n')
			f.write(training.description + '\n')
			f.write('Training Status: ' + training.status + '\n')
			f.write('Training Link: ' + training.link + '\n')
		f.write('\n' + '-----------------------------' + '\n')
	f.close()

def pullPastTrainings():
	past_url = 'http://dlab.berkeley.edu/past-trainings?page='
	dlab = 'http://dlab.berkeley.edu'
	past_r = requests.get(past_url)
	past_soup = BeautifulSoup(past_r.content, 'html.parser')
	lp = past_soup.find('li', class_ = 'pager-last last').a.get('href')
	# pdb.set_trace()
	last_page = int(re.search(r'page=[0-9]*', lp).group(0)[5:])
	past_ts = []
	# test purpose
	# for i in range(3):
	for i in range(last_page + 1):
		past_url = 'http://dlab.berkeley.edu/past-trainings?page='
		past_url += str(i)
		past_r = requests.get(past_url)
		past_soup = BeautifulSoup(past_r.content, 'html.parser')
		# pdb.set_trace()
		past_content = past_soup.find_all('div', class_ = 'view-content')[1]
		for past_training in past_content.children:
			try:
				title_link = past_training.find('div', class_ = 'title').a.get('href')
				training_link = dlab + title_link
				training_r = requests.get(training_link)
				training_soup = BeautifulSoup(training_r.content, 'html.parser')
				title = training_soup.find('div', class_ = 'page-title span12').text[1:]
				dateTimes = []
				dts = training_soup.find_all('span', class_ = 'date-display-single')
				for dt in dts:
					dateTimes.append(dt.text)
				if len(dateTimes) == 0:
					start = training_soup.find('span', class_ = 'date-display-start').text
					end = training_soup.find('span', class_ = 'date-display-end').text
					dateTimes.append(start + ' to ' + end)
				ins = training_soup.find_all('h2')[1:]
				instructors = ''
				for instructor in ins:
					instructors += instructor.text
					instructors += ', '
				instructors = instructors[:-2]
				t = Training(title, instructors, dateTimes, None, None, None)
				past_ts.append(t)
			except:
				pass
	return past_ts

def pullCurrentTrainings():
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
	return ts

if __name__ == '__main__':
	current_trainings = pullCurrentTrainings()
	past_trainings = pullPastTrainings()
	fileOutput(current_trainings, 'current_trainings.txt')
	fileOutput(past_trainings, 'past_trainings.txt')

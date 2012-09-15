import requests

currTerm = "20123"
depUrl = "http://web-app.usc.edu/ws/soc/api/depts/"
baseClassUrl = "http://web-app.usc.edu/ws/soc/api/classes/"
deps = []
courses = []

class DepItem(dict):
	code = []
	name = []


class ClassItem(dict):
	department = []
	code = []
	title = []
	desc = []
	units = []
	sections = []

class SectionItem(dict):
	course = []
	code = []
	secType = []
	startTime = []
	endTime = []
	days = []
	reg = []
	seats = []
	instructor = []
	loc = []
	dclear = False

def processSection(sec, course):
	if sec['canceled'] == 'Y':
		return None
	section = SectionItem()
	section['course'] = course['code']
	section['code'] = sec['id']
	section['dclear'] = (sec['dclass_code'] == "D")
	section['secType'] = sec['type']
	try:
		section['startTime'] = sec['start_time']
		section['endTime'] = sec['end_time']
	except KeyError:
		section['startTime'] = 'TBA'
		section['endTime'] = 'TBA'
	try:
		section['location'] = sec['location']
	except KeyError:
		section['location'] = 'TBD'
	section['seats'] = sec['spaces_available']
	section['reg'] = sec['number_registered']
	section['days'] = []
	section['instructor'] = []
	try:
		for day in sec['day']:
			section['days'].append({
				'M' : 'M',
				'T' : 'T',
				'W' : 'W',
				'H' : 'H',
				'F' : 'F'
			}[day])
	except KeyError:
		section['days'] = ['TBD']
	try:
		sec['instructor']['first_name']
		section['instructor'].append(sec['instructor']['first_name'] + ' ' + sec['instructor']['first_name'])
	except TypeError:
		for instructor in section['instructor']:
			section['instructor'].append(sec['instructor']['first_name'] + ' ' + sec['instructor']['first_name'])

def processDepartment(department):
	if (department['type'] == "Y" or department['type'] == []):
		deps = []
		deplist = department['department']
		try:
			deplist['code']
			deps.append(processDepartment(deplist))
		except TypeError:
			for d in deplist:
				print d
				try:
					deps = deps + (processDepartment(d))
				except TypeError:
					deps.append(processDepartment(d))
	else:
		dep = DepItem()
		dep['code'] = department['code']
		dep['name'] = department['name']
		return dep

def processCourse(course, depcode):
	co = ClassItem()
	cdata = course['CourseData']
	co['department'] = depcode
	co['code'] = course['PublishedCourseID']
	co['title'] = cdata['title']
	co['desc'] = cdata['description']
	co['units'] = cdata['units']
	secdata = cdata['SectionData']
	co['sections'] = []
	try:
		secdata['id']
		nsec = processSection(secdata, co)
		if nsec:
			co['sections'].append(nsec)
	except TypeError:
		for sec in secdata:
			nsec = processSection(sec, co)
			if nsec:
				co['sections'].append(nsec)
	return co

r = requests.get(depUrl + currTerm)
for department in r.json['department']:
	try:
		deps = deps + (processDepartment(department))
	except TypeError:
		deps.append(processDepartment(department))
deps = filter(None, deps)
for department in deps:
	clr = requests.get(baseClassUrl + department['code'] + '/' + currTerm).json
	coursedata = clr['OfferedCourses']['course']
	try:
		for course in coursedata:
			print course['PublishedCourseID']
			courses.append(processCourse(course, department['code']))
	except TypeError:
		print coursedata['PublishedCourseID']
		courses.append(processCourse(coursedata, department['code']))
print courses


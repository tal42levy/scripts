import time
import requests
import sqlite3

currTerm = "20131"
depUrl = "http://web-app.usc.edu/ws/soc/api/depts/"
baseClassUrl = "http://web-app.usc.edu/ws/soc/api/classes/"
dbUrl = "example.sqlite3"
deps = {} 
courses = []

def add_to_db():
	conn = sqlite3.connect(dbUrl)
	c = conn.cursor()

	#DELETE THIS LATER
	#c.execute('drop table departments')
	#c.execute('drop table courses')
	#c.execute('drop table sections')
	#c.execute('drop table instructors')

	c.execute('Create table if not exists departments (id integer primary key, code text, name text)')
	c.execute('create table if not exists courses (id integer primary key, code text, department_id integer, title text, desc blob, units integer)')
	c.execute('create table if not exists sections (id integer primary key, course_id integer, code text, sect text, start text, \
		end text, days text, reg integer, seats integer, instructor_ids string, loc text, dclear boolean)')
	c.execute('create table if not exists instructors (id integer primary key, name text)')

	for depkey in deps.keys():
		dep = deps[depkey]
		c.execute('select * from departments where code = ?', (dep['code'],))
		if c.fetchone() is None:
			c.execute('Insert into departments(code, name) values (?, ?)', (dep['code'], dep['name']))

		else: 
			next

	for course in courses:
		c.execute('select id from departments where code = ?', [course['department']])
		row = c.fetchone()
		data = (course['code'], course['title'], course['desc'], course['units'], row[0])
		c.execute('select id from courses where code = ? and department_id = ?', (course['code'],row[0]))
		currcourse = c.fetchone()
		if currcourse is None:
			c.execute('insert into courses(code, title, desc, units, department_id) values (?, ?, ?, ?, ?)', data)
		else: 
			c.execute('update courses set title = ?, desc = ?, units = ? where id = ?', (course['title'], course['desc'], course['units'], currcourse[0]))
		c.execute('select id from courses where code = ? and department_id = ?', (course['code'],row[0]))
		currcourse = c.fetchone()
		code = currcourse[0]
		c.execute('delete from sections where course_id = ?', (code,))
		for section in course['sections']:
		
			instids = []
			for ins in section['instructor']:
				c.execute('select * from instructors where name = ?', (ins,))
				inst = c.fetchone()
				if not (inst):
					c.execute('insert into instructors (name) values (?)', (section['instructor']))
					c.execute('select * from instructors where name = ?', (ins,))
					inst = c.fetchone()
				instids.append(inst[1])
			#print section['location']
			c.execute('insert into sections(code, course_id, sect, start, end, days, reg, seats, instructor_ids, loc, dclear) values \
				(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (section['code'], code, section['secType'], section['startTime'], section['endTime'], \
					''.join(section['days']), section['reg'], section['seats'], ' ,'.join(instids), section['location'], section['dclear']))
	conn.commit()

class DepItem(dict):
	code = []
	name = []


class ClassItem(dict):
	department = []
	code = []
	title = ''
	desc = ""
	units = ''
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

	if not isinstance(section['endTime'], str):
		section['endTime'] = section['endTime'][0]
	if not isinstance(section['startTime'], str):
		section['startTime'] = section['startTime'][0]
	try:
		section['location'] = sec['location']
	except KeyError:
		section['location'] = 'TBD'
	if not isinstance(section['location'], basestring):
		#print section['location']
		try:
			section['location'] = section['location'][0]
		except KeyError:
			section['location'] = 'TBD'
	if not section['location']:
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
		section['instructor'].append(sec['instructor']['first_name'] + ' ' + sec['instructor']['last_name'])
	except TypeError:
		for instructor in section['instructor']:
			section['instructor'].append(sec['instructor']['first_name'] + ' ' + sec['instructor']['last_name'])
	return section

def processDepartment(department):
	if (department['type'] == "Y" or department['type'] == []):
		deplist = department['department']
		try:
			deplist['code']
			temp = processDepartment(deplist)
			deps[temp['code']] = temp
		except TypeError:
			for d in deplist:
				temp = processDepartment(d)
				deps[temp['code']] = temp
	else:
		dep = DepItem()
		dep['code'] = department['code']
		dep['name'] = department['name']
		return dep

def processCourse(course, depcode):
	co = ClassItem()
	cdata = course['CourseData']
	co['department'] = depcode
	co['code'] = course['PublishedCourseID'].split('-')[1]
	co['title'] = cdata['title']
	if cdata['description']:
		co['desc'] = cdata['description']
	else: 
		co['desc'] = ""
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
		temp = processDepartment(department)
		deps[temp['code']] = temp
	except TypeError:
		pass
for depkey in deps.keys():
	department = deps[depkey]
	print department['code']
	clr = requests.get(baseClassUrl + department['code'] + '/' + currTerm).json
	coursedata = clr['OfferedCourses']['course']
	try:
		for course in coursedata:
			courses.append(processCourse(course, department['code']))
	except TypeError:
		courses.append(processCourse(coursedata, department['code']))
add_to_db()


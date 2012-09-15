from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from classer.items import ClassItem, SectionItem

class ClassSpider(BaseSpider):
	name = "classer"
	allowed_domains = ["usc.edu"]
	start_urls = [
		"http://web-app.usc.edu/soc/20123/fbe"
	]

	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		classes = hxs.select("//div[@id='course_table']/div")
		items = []
		for cl in classes:
			item = ClassItem()
			item['department'] = "AEST"
			item['code'] = cl.select("div[@class='course_id']/h3/a/strong/text()").extract()
			item['units'] = cl.select("div[@class='course_id']/h3/a/span/text()").extract()
			item['desc'] = cl.select("div[@class='course_details']/div/text()").extract()
			details = cl.select("div[@class='course_details']")
			sections = details.select("table/tr")
			secdata = []
			for section in sections:
				if (section.select("th")):
					print "header found"
				else :
					sec = self.parseSection(section)
					secdata.append(sec)
			item['sections'] = secdata
			items.append(item)
		return items

	def parseSection(self, secData):
		if (secData.select("th[@class='location']/text()").extract() == 'Location'):
			print "Headers"
			return 0
		section = SectionItem()
		section['code'] = secData.select("td[@class='section']/text()").extract()
		section['secType'] = secData.select("td[@class='type']/text()").extract()
		section['instructor'] = secData.select("td[@class='instructor']/text()").extract()
		section['loc'] = secData.select("td[@class='location']/text()").extract()
		timeraw = secData.select("td[@class='time']/text()").extract()[0].split('-')
		print "TIMERAW: ", timeraw
		section['startTime'] = timeraw[0]
		if (len(timeraw) > 1):
			section['endTime'] = timeraw[1]
		else:
			section['endTime'] = timeraw[0]
		dayraw = secData.select("td[@class='days']/text()").extract()
		days = self.parseDays(dayraw[0])
		seatraw = secData.select("td[@class='registered']/text()")
		if (not seatraw.extract()) or ("on waitlist" in seatraw.extract()[0]):
			print "new"
			seatraw = secData.select("td[@class='registered']/div/text()").extract()
		else:
			seatraw = seatraw.extract()
		if (seatraw[0] == "Canceled"):
			section['reg'] = 0
			section['seats'] = 0
			return section
		seatstring = seatraw[0].split(" of ")
		print seatstring
		section['reg'] = seatstring[0]
		section['seats'] = seatstring[1]
		return section

	def parseDays(self, dayraw):
		days = []
		daysplit = dayraw.split(', ')
		print daysplit
		print len(daysplit)
		if (len(daysplit) > 1):
			i = 0
			for dayta in daysplit:
				if (daysplit[i] == 'Monday' or daysplit[i] == 'Mon'):
					days.append("Monday")
				elif (daysplit[i] == 'Tuesday' or daysplit[i] == 'Tue'):
					days.append("Tuesday")
				elif (daysplit[i] == 'Wednesday' or daysplit[i] == 'Wed'):
					days.append("Wednesday")
				elif (daysplit[i] == 'Thursday' or daysplit[i] == 'Thu'):
					days.append("Thursday")
				elif (daysplit[i] == 'Friday' or daysplit[i] == 'Fri'):
					days.append("Friday")
		elif (dayraw[-3:] == 'day'):
			if (dayraw == 'Monday' or dayraw == 'Mon'):
				days.append("Monday")
			elif (dayraw == 'Tuesday' or dayraw == 'Tue'):
				days.append("Tuesday")
			elif (dayraw == 'Wednesday' or dayraw == 'Wed'):
				days.append("Wednesday")
			elif (dayraw == 'Thursday' or dayraw == 'Thu'):
				days.append("Thursday")
			elif (dayraw == 'Friday' or dayraw == 'Fri'):
				days.append("Friday")
		else:
			if (dayraw == 'TBD'):
				days.append['TBD']
			for i in range(len(dayraw)):
				if (dayraw[i] == 'M'):
					days.append("Monday")
				elif (dayraw[i] == 'T'):
					if (dayraw[i+1] == 'u'):
						days.append("Tuesday")
						i = i + 1
					elif (dayraw[i+1] == 'h'):
						days.append("Thursday")
						i = i + 1
					else:
						days.append("Tuesday")
				elif (dayraw[i] == 'W'):
					days.append("Wednesday")
				elif (dayraw[i] == 'F'):
					days.append("Friday")
		return days






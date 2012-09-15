# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class ClassItem(Item):
	department = Field()
	code = Field()
	title = Field()
	desc = Field()
	units = Field()
	sections = Field()
	pass

class SectionItem(Item):
	code = Field()
	secType = Field()
	startTime = Field()
	endTime = Field()
	days = Field()
	reg = Field()
	seats = Field()
	instructor = Field()
	loc = Field()
	pass

require 'date'
require 'active_support'
require 'win32ole'

connection = WIN32OLE.new('ADODB.Connection')
connection.Open('Provider=Microsoft.ACE.OLEDB.12.0;
                 Data Source=c:\path\filename.mdb')
tabname = 'schedule'

class Sect 
	attr_accessor :date, :name, :loc, :length, :type
	def initialize(date, name, loc, length, type)
		@date = date
		@name = name
		@loc = loc
		@length = length
		@type = type
	end
end

$THH301 = 1
$OHE406 = 2
$SLH100 = 3
$KAP267 = 4
$OHE336 = 5
$KAP140 = 6
$KAPB5 = 7
$SGM101 = 8
$lec = 1
$disc = 2
$leclab = 3
$lab = 4

clas149a = Sect.new(DateTime.new(2012, 10, 1, 12, 0, 0), '1', 'THH301', 50, 'lec')
clas149b = Sect.new(DateTime.new(2012, 10, 3, 12, 0, 0), '1', 'THH301', 50, 'lec')
clas149c = Sect.new(DateTime.new(2012, 10, 5, 12, 0, 0), '1', 'THH301', 50, 'lec')
clas149s = Sect.new(DateTime.new(2012, 10, 5, 11, 0, 0), '1', 'THH301', 50, 'disc')
itp125 = Sect.new(DateTime.new(2012, 10, 1, 17, 0, 0), '2', 'OHE406', 170, 'leclab')
phys162a = Sect.new(DateTime.new(2012, 10, 2, 14, 0, 0), '3', 'SLH100', 110, 'lec')
phys162b = Sect.new(DateTime.new(2012, 10, 4, 14, 0, 0), '3', 'SLH100', 110, 'lec')
itp300 = Sect.new(DateTime.new(2012, 10, 3, 14, 0, 0), '4', 'KAP267', 170, 'leclab')
ee201l = Sect.new(DateTime.new(2012, 10, 2, 17, 0, 0), '5', 'OHE336', 170, 'lab')
ee201a = Sect.new(DateTime.new(2012, 10, 2, 9, 30, 0), '5', 'KAP140', 80, 'lec')
ee201b = Sect.new(DateTime.new(2012, 10, 4, 9, 30, 0), '5', 'KAP140', 80, 'lec')
phys152 = Sect.new(DateTime.new(2012, 10, 4, 17, 0, 0), '6', 'KAPB5', 170, 'lab')
engr100 = Sect.new(DateTime.new(2012, 10, 5, 13, 0, 0), '7', 'SGM101', 50, 'lec')

sects = [clas149a, clas149s, clas149c, clas149b, itp125, itp300, ee201b, ee201a, ee201l, phys152, engr100]

while (clas149c.date < DateTime.new(2012, 12, 8, 11, 0, 0)) do

	#insert into db

	sects.each do |sec|
		s = "$" + sec.loc 
		p = "$" + sec.type
		upd = "INSERT INTO #{tabname} (class_id, start, location_id, end, type_id) values (#{sec.name}, ##{sec.date.strftime('%D %T')}#, #{eval(s)}, ##{(sec.date + Rational(sec.length, 1440)).strftime('%D %T')}#, #{eval(p)});"
		connection.Execute(upd)
		puts upd
		sec.date += 7
	end
end

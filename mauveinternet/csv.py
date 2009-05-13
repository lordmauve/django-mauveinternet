import csv

from django.http import HttpResponse

class CSVResponse(HttpResponse):
	def __init__(self, filename):
		super(CSVResponse, self).__init__(mimetype='text/csv; charset=UTF-8')
		resp['Content-Disposition'] = 'attachment; filename="%s"' % self.filename().replace('"', '\'')
		self.spreadsheet = csv.writer(self)

	def writerow(self, row):
		self.spreadsheet.writerow([unicode(r).encode('utf8') for r in row])
		

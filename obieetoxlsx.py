import xlsxwriter
import sys
filename = sys.argv[1]

workbookName = filename.split('.')[0] + '.xlsx'
workbook = xlsxwriter.Workbook(workbookName)
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': True})
headers = ('Timestamp', 'Trace no.', 'User', 'ECID', 'TID', 'Request ID', 'Session ID', 'Username', 'SQL')
worksheet.write_row('A1', headers, bold)

log = open(filename)

logString = log.read()

logEntries = logString.split("[20") 
rowNum = 1
print('Converting ' + filename + ' to ' + workbookName + '...')

for entry in logEntries:
	entryFields = entry.split('[')
	newFieldList = []

	counter = 0
	for field in entryFields:
		field = field.replace('[', '')
		field = field.replace(']', '')
		if ':' in field and counter > 0 and counter != 5: #stop it from slicing up the timestamp
			field = field.split(':')[1]
		field = field.lstrip()
		newFieldList.append(field)
		counter+=1

	if 'OracleBIServerComponent ' in newFieldList: #remove OracleBIServerComponent field
		newFieldList.remove('OracleBIServerComponent ')
	while '' in newFieldList:
		newFieldList.remove('')
	if len(newFieldList) > 4:
		newFieldList[3] = newFieldList[3].lstrip('ecid: ')

	worksheet.write_row(rowNum, 0, newFieldList)
	rowNum+=1
	
workbook.close()
print('Conversion complete.')
	
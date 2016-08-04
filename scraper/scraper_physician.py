from mechanize import Browser
from bs4 import BeautifulSoup as BS
from time import sleep # be nice
from pandas import DataFrame
import json

content = {}


states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}


#f = open('physician.txt','w')


br = Browser()

# Browser options
# Ignore robots.txt. Do not do this without thought and consideration.
br.set_handle_robots(False)

# Don't add Referer (sic) header
br.set_handle_referer(False)

# Don't handle Refresh redirections
br.set_handle_refresh(False)

#Setting the user agent as firefox
br.addheaders = [('User-agent', 'Chrome')]

state_list = sorted(states.keys())


for num in range(0,len(state_list)):
	link = 'http://superdimension.com/state/'+str(state_list[num])+'/'
	print
	print
	print '======================================================'
	print states[str(state_list[num])]
	print '======================================================'
	print
	print
	br.open(url = link)

	#Getting the response in beautifulsoup
	soup = BS(br.response().read(),'html.parser')

	#print soup
	list_comp = soup.findAll("section", {"class":"physician-list"})


	
	for line in list_comp:
		a = line.find('h3').contents[0]
		b = line.findAll('p')
		href = len(b)
		hos_aff = len(b)
		print a
		#print len(b)
		#for k in b:
	    #	print k.contents[0]


		for i in range(len(b)):
			if b[i].contents[0] == 'Hospital Affiliations:':
				hos_aff = i
			if b[i].find('a',href = True) != None:
				href = i
				

		#print 'hos:' + str(hos_aff)
		#print 'href: ' + str(href)
		
		for j in range(1,min(hos_aff,href)-1):
			if b[j].find('a',href = True) != None:
				print b[j].find('a',href = True)['href']
			else:
				print b[j].contents[0]
		

		print
	




'''
l = {'AIG','Kensho'}
#for i in content:
#	print i
count = 0
for i in content:
	count +=1
	br.open(url = content[i]['link    '])
	temp_soup = BS(br.response().read(),'html.parser')


	profile_temp = temp_soup.find('div',{'class':'field field-type-text field-field-profile'})
	if profile_temp != None:
		profile = profile_temp.find('p').contents[0]
	else:
		profile = ''


	webpage_temp = temp_soup.find('div',{'class':'field field-type-text field-field-webpage'})
	if webpage_temp != None:
		if webpage_temp.find('a',href = True) != None:
			webpage = webpage_temp.find('a',href = True)['href']
		else:
			webpage = webpage_temp.find('p').contents[0]
	else:
		webpage = ''


	major_temp = temp_soup.find('div',{'class':'field field-type-text field-field-major'})
	if major_temp != None:
		major = major_temp.find('div',{'class':'field-item odd'}).contents[2].strip()
	else:
		major = ''


	hiring_temp = temp_soup.find('div',{'class':'field field-type-text field-field-hiring'})
	if hiring_temp != None:
		hiring = hiring_temp.find('p').contents[0]
	else:
		hiring = ''


	industry_temp = temp_soup.find('div',{'class':'field field-type-text field-field-industry'})
	if industry_temp != None:
		industry = industry_temp.find('div',{'class':'field-item odd'}).contents[2].strip()
	else:
		industry = ''


	position_temp = temp_soup.find('div',{'class':'field field-type-text field-field-position-type'})
	if position_temp != None:
		position = position_temp.find('div',{'class':'field-item odd'}).contents[2].strip()
	else:
		position = ''


	visa_temp = temp_soup.find('div',{'class':'field field-type-text field-field-visa'})
	if visa_temp != None:
		visa = visa_temp.find('div',{'class':'field-item odd'}).contents[2].strip()
	else:
		visa = ''
	content[i]['profile '] = profile.encode('utf8')
	content[i]['webpage '] = str(webpage)
	content[i]['major   '] = str(major)
	content[i]['hiring  '] = str(hiring)
	content[i]['industry'] = str(industry)
	content[i]['position'] = str(position)
	content[i]['visa    '] = str(visa)
	print 'webpage ', str(webpage)
	print 'major ', str(major)
	print 'position ', str(position)
	print 'hiring ', str(hiring)
	print 'industry ', str(industry)
	print 'visa ', str(visa)
	
f = open('career.txt','w')

for i in content:
	f.write('Company :\t\t' + i.encode('utf8') + '\n')
	for j in content[i]:
		f.write(str(j) + ':\t\t' + str(content[i][j])+'\n')
	f.write('\n\n')

f.close()


f2 = open('career_sponsor.txt','w')

sponsor = [i for i in content if content[i]['visa    '] == 'Yes']
print sponsor

for i in sponsor:
	f2.write('Company :\t\t' + i.encode('utf8') + '\n')
	for j in content[i]:
		f2.write(str(j) + ':\t\t' + str(content[i][j])+'\n')
	f2.write('\n\n')

f2.close()



f3 = open('career_sponsor_engineering.txt','w')

sponsor_E = [i for i in content if content[i]['visa    '] == 'Yes' and ('Engineering' in content[i]['major   '] or 'All' in content[i]['major   '])]
print sponsor

for i in sponsor_E:
	f3.write('Company :\t\t' + i.encode('utf8') + '\n')
	for j in content[i]:
		f3.write(str(j) + ':\t\t' + str(content[i][j])+'\n')
	f3.write('\n\n')

f3.close()




f4 = open('career_sponsor_consulting.txt','w')

sponsor_E = [i for i in content if content[i]['visa    '] == 'Yes' and 'Consulting' in content[i]['industry']]
print sponsor

for i in sponsor_E:
	f4.write('Company :\t\t' + i.encode('utf8') + '\n')
	for j in content[i]:
		f4.write(str(j) + ':\t\t' + str(content[i][j])+'\n')
	f4.write('\n\n')

f4.close()

#for i in content:
#	content[i]['link']


'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


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

#states = {'AZ':1,'AR':2}
state_list = sorted(states.keys())
driver = webdriver.Firefox()
output = []
for s in state_list:
	driver.get("http://www.riskforcancer.com/find-a-hospital.html")
	driver.find_element_by_id("inputAddress").clear()
	element = driver.find_element_by_id("inputAddress")
	element.send_keys(s)
	element.send_keys(Keys.RETURN)
	driver.implicitly_wait(5)
	result = driver.find_elements_by_class_name("listText")
	for i in result:
		if i.text not in output:
			output.append(i.text)
			print i.text
		print



mouse = webdriver.ActionChains(driver)    


inside = 0
for s in state_list:
	driver.get("http://www.riskforcancer.com/find-a-hospital.html")
	driver.find_element_by_id("inputAddress").clear()
	element = driver.find_element_by_id("inputAddress")
	element.send_keys(s)
	element.send_keys(Keys.RETURN)
	driver.implicitly_wait(5)
	span_xpath = '//*[@id="locationsNav"]/span/a'
	next_elem = driver.find_element_by_xpath(span_xpath)
	mouse.move_to_element(next_elem).click().perform()
	result = driver.find_elements_by_class_name("listText")
	for i in result:
		if i.text not in output:
			output.append(i.text)
			print i.text
		print
	mouse = webdriver.ActionChains(driver) 


#print driver.page_source.encode("utf-8")
driver.close()


#//*[@id="locationsNav"]/span/a
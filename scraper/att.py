#!/Users/xiawei918/anaconda2/bin/python
from mechanize import Browser
from bs4 import BeautifulSoup as BS
from time import sleep # be nice
from pandas import DataFrame
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from att_config import USERID, PWD, password
import smtplib
from email.mime.text import MIMEText
import base64

def get_att_data():
	id_list = ['260-564-32160T','484-633-80401T','484-747-30892T','484-934-21563T','610-659-14904T','610-674-77855T','610-674-77966T','610-739-98597T','757-645-68698T']
	driver = webdriver.Firefox()
	output = []
	driver.get("https://www.att.com/olam/loginAction.olamexecute")
	driver.find_element_by_name("userid").clear()
	userid = driver.find_element_by_name("userid")
	password = driver.find_element_by_name("password")
	userid.send_keys(USERID)
	password.send_keys(base64.b64decode(PWD))
	password.send_keys(Keys.RETURN)
	driver.implicitly_wait(20)

	data = driver.find_element_by_id('phoneItemContainer').text.encode('utf-8')

	timestr = time.strftime("%Y%m%d") + '.txt'
	f=open(timestr,'w+')
	
	driver.implicitly_wait(20)

	try:
		driver.find_element_by_link_text('View bill details').click()
	except:
		driver.refresh()
		driver.find_element_by_link_text('View bill details').click()

	driver.implicitly_wait(30)

	#driver.find_element_by_id('260-564-32160T').click()
	for item in id_list:
		driver.find_element_by_id(item).click()
		driver.implicitly_wait(2)

	driver.implicitly_wait(5)

	info = driver.find_element_by_id('toggleGroup10').text.encode('utf-8')
	
	info = data + info
	f.write(info)



	'''s
	result = driver.find_elements_by_class_name("listText")
	for i in result:
		if i.text not in output:
			output.append(i.text)
			print i.text
		print

	'''
	f.close()
	driver.close()
	return timestr


def calculate_fee(f_name, cell):
	g = open(f_name,'r')
	g_list = [line for line in g]
	#g = open(f_name, 'rU')
	
	data = {}
	base_cost = {}
	total_cost = {}
	total_overage = 0
	overage_cost = 0

	temp_data = []
	number = []
	data_fee = []
	data_overage = 0

	for i in xrange(len(g_list)):
		if g_list[i] == "\n":
			counter = i
			break
		if i % 5 == 0:
			number.append(g_list[i][:-1])
		if i % 5 == 3:
			temp_data.append(float(g_list[i][:3]))
		

	for i in xrange(len(number)):
		data[number[i]] = temp_data[i]



	total_overage = sum([max(0,float(data[key])-1.67) for key in data])


	cost_file = g_list[counter+23:]

	for i in xrange(len(cost_file)):
		if cost_file[i][:9] == 'Total for':
			base_cost[cost_file[i][10:-1]] = cost_file[i+1][1:-1]
	

	overage_ind = cost_file.index('Data & Text Usage Charges\n')+1
	overage_cost = cost_file[overage_ind][1:]

	base_cost['757-645-6869'] = str(round(float(base_cost['757-645-6869']) - 90 - float(overage_cost),2))

	if total_overage != 0:
		for key in data:
			temp = round((max(0,float(data[key]) - 1.67)/float(total_overage))*float(overage_cost),2)
			total_cost[str(key)] = round(temp + 10 + float(base_cost[key]),2)

	width = 37
	detail = ''
	detail += 'Total cost for ' + cell + ' in month ' + time.strftime("%m/%Y") + ' is $' + str(total_cost[cell]) + '.\n'
	detail += '================ Cost Summary ================\n'
	detail += '{:<22}  {:>22}\n'.format('Base ($): ', str(base_cost[cell]))
	detail += '{:<22}  {:>22}\n'.format('Data ($):', str(total_cost[cell] - float(base_cost[cell])))
	detail += '================ Data Summary ================\n'
	detail += '{:<22}  {:>22}\n'.format('Data used (GB): ', str(data[cell]))
	detail += '{:<22}  {:>22}\n'.format('Data overage (GB): ', str(max(0,data[cell] - 1.67)))
	detail += '{:<24}  {:>20}\n'.format('Overage percentage (%): ', str(round(max(0,data[cell] - 1.67)/total_overage,2)))
	detail += '{:<22}  {:>22}\n'.format('Overage cost (S): ', str(round((max(0,data[cell] - 1.67)/total_overage)*float(overage_cost),2)))
	detail += '==================== Total ====================\n'
	detail += '{:<22}  {:>22}\n'.format('Total ($): ', str(total_cost[cell]))


	return detail


if __name__ == "__main__":
	f_name = get_att_data()
	try:
		result = calculate_fee(f_name,"610-674-7796")
	except:
		f_name = get_att_data()
		result = calculate_fee(f_name,"610-674-7796")
	
	#result = calculate_fee('20160721.txt',"610-674-7796")


	emails = {'757-645-6869':'wex213@lehigh.edu','610-674-7796':'yuh212@lehigh.edu','484-934-2156':'susiesonghx@gmail.com','484-633-8040':'xih314@lehigh.edu','610-674-7785':'xik312@lehigh.edu','260-564-3216':'sht213@lehigh.edu','610-739-9859':'chi208@lehigh.edu','610-659-1490':'ruy212@lehigh.edu'}

	for num in emails:
		result = calculate_fee(f_name,num)
		print result
		to = emails[num]
		gmail_user = 'xiawei27149@gmail.com'
		gmail_pwd = base64.b64decode(password)
		smtpserver = smtplib.SMTP("smtp.gmail.com",587)
		smtpserver.ehlo()
		smtpserver.starttls()
		smtpserver.ehlo
		smtpserver.login(gmail_user, gmail_pwd)
		header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject: Phone bill for ' + time.strftime("%m/%Y") + '\n'
		print header
		msg = header + result
		msg = msg +'\n\n The following banks are eligible for transfer:\n Wells Fargo\n Bank Of American\n'
		msg = msg +'\n Please use wex213 at lehigh dot edu for money transfer.\n\n If you have any questions, please contact wex213.\n'
		
		smtpserver.sendmail(gmail_user, to, msg)
		print 'done!'
		smtpserver.close()
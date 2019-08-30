from db import db_connect as db
from datetime import datetime
from dateutil import relativedelta
import logging




cur = db.connectToDb()
logging.basicConfig(filename="newfile.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w')
log = logging.getLogger()

departments = ['Customer Service', 'Development', 'Finance', 'Human Resources', 'Human Resources', 'Sales']
titles = ['Senior Engineer', 'Staff', 'Engineer', 'Senior Staff', 'Assistant Engineer', 'Technical Lead']
title_mapper = {
	'Staff': 'Senior staff',
	'Senior staff': 'Assistant Engineer',
	'Assistant Engineer': 'Engineer',
	'Engineer': 'Senior Engineer',
	'Senior Engineer': 'Technical Lead',
	'Technical Lead': 'Manager',
	'Manager': 'CEO'
}



now = datetime.now()

def hike_eligibility(emp_no):


	# Fetching the employee department name
	log.info("Fetching the employee department name")
	try:
		dept_query = "select dept_name from test.departments where dept_no = (select dept_no from test.dept_emp where emp_no = '"+ str(emp_no) +"')"

		cur.execute(dept_query)
		dept_name = cur.fetchall()[0][0]

	except:

		log.error("Unable to fetch data from DB")


	# Fetching the employee title
	log.info("Fetching the employee department title")
	try:
		title_query = "select title from test.titles where emp_no = '"+ str(emp_no) +"'"

		cur.execute(title_query)
		title = cur.fetchall()[0][0]

	except:

		log.error("Unable to fetch data from DB")

	if dept_name not in departments or title not in titles:

		return {'hike': False}

	# check experience and age of the employee

	try:
		exp_query = "select hire_date from test.employees where emp_no = '"+ str(emp_no) +"'"

		cur.execute(exp_query)
		experience = cur.fetchall()[0][0]

	except:
		log.error("Unable to fetch data from DB")


	try:
		exp_query = "select birth_date from test.employees where emp_no = '"+ str(emp_no) +"'"

		cur.execute(exp_query)
		birthday = cur.fetchall()[0][0]

	except:
		log.error("Unable to fetch data from DB")




	exp = relativedelta.relativedelta(now, experience)
	age = relativedelta.relativedelta(now, birthday)

	if exp.years <= 1 or age.years <= 20:

		return {'hike': False}
		

	# Check gender and designation to check whether the employee is eligible for hike or not


	try:
		exp_query = "select gender from test.employees where emp_no = '"+ str(emp_no) +"'"

		cur.execute(exp_query)
		gender = cur.fetchall()[0][0]

	except:
		log.error("Unable to fetch data from DB")


	try:
		exp_query = "select title from test.titles where emp_no = '"+ str(emp_no) +"'"

		cur.execute(exp_query)
		title = cur.fetchall()[0][0]

	except:
		log.error("Unable to fetch data from DB")


	if gender == 'M' and title == 'Technical Lead':
		return {'hike': False}

	# Promote the employee to higher level
	try:
		exp_query = "select title from test.titles where emp_no = '"+ str(emp_no) +"'"

		cur.execute(exp_query)
		title = cur.fetchall()[0][0]

	except:
		log.error("Unable to fetch data from DB")

	try:

		new_position = title_mapper[title]

		exp_query = "update test.titles set title = '"+ new_position +"' where emp_no = '"+ str(emp_no) +"'"
		cur.execute(exp_query)

		exp_query = "select title from test.titles where emp_no = '"+ str(emp_no) +"'"

		cur.execute(exp_query)
		title = cur.fetchall()[0][0]

	except:
		log.error("Unable to fetch data from DB")


	return {'hike': True, 'designation': title}










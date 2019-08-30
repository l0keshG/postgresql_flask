from db import db_connect as db
from datetime import datetime
import logging
from errors.error import JsonFormatError
from dateutil import relativedelta

cur = db.connectToDb()
logging.basicConfig(filename="newfile.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w')
log = logging.getLogger()

# salary and title role mapper dictionary
salary_role_mapper = {
	'Staff': 300000,
	'Senior staff': 500000,
	'Assistant Engineer': 700000,
	'Engineer': 900000,
	'Senior Engineer': 1200000,
	'Technical Lead': 2000000,
	'Manager': 3000000
}

departments = ['Customer Service', 'Development', 'Finance', 'Human Resources', 'Marketing', 'Sales', 'Production', 'Quality Management', 'Research']
now = datetime.now()

def insert_employee(data):

	"""
	Inserting employee details in test.employee table and checking constraint age if employee is above 18 and below 60
	"""

	log.info("Reading the file and loading data into DB")

	emp_no = str(data['emp_no'])
	birth_date = datetime.strptime(data['birth_date'], '%d/%m/%Y').strftime('%Y-%m-%d')
	first_name = data['first_name']
	last_name = data['last_name']
	gender = data['gender']
	hire_date = datetime.strptime(data['hire_date'], '%d/%m/%Y').strftime('%Y-%m-%d')

	age = relativedelta.relativedelta(now, datetime.strptime(data['birth_date'] , '%d/%m/%Y'))
	if age.years < 18 and age.years > 60:
		return { "error": "Employee age must be between 18 and 60", "status_code": 502 }


	try:

		sql_query = "insert into test.employees(emp_no, birth_date, first_name, last_name, gender, hire_date) \
					values('" + emp_no + "','"+ birth_date +"','"+ first_name +"','"+ last_name  + "','" + gender + "','"+ hire_date +"' )"

		cur.execute(sql_query)

	except:
		log.error("Unable to insert data into table. Incorrect data format")
		return {"error": "Data is not inserted. Please check the input file", "status_code": 500}

	else:
		log.info("Data in inserted successfully")
		return {"info": "Data is inserted successfully", "status_code": 200}


def insert_dept_emp(data):

	"""
	Inserting employee dept details in test.dept_emp table and checking constraint dept is valid
	"""

	if data['department'] not in departments:
		return { "error": "Employee age must be between 18 and 60", "status_code": 501 }

	try:


		query = "select dept_no from test.departments where dept_name = '"+ data['department']+ "'"

		cur.execute(query)
		dept_no = cur.fetchall()[0][0]

	except:
		log.error("Unable to fetch data from table")
		return {"error": "Data is not inserted. Please check the input file", "status_code": 500}


	emp_no = str(data['emp_no'])
	from_date = datetime.strptime(data['salary_from'], '%d/%m/%Y').strftime('%Y-%m-%d')
	to_date = datetime.strptime(data['salary_to'], '%d/%m/%Y').strftime('%Y-%m-%d')


	try:

		sql_query = "insert into test.dept_emp(emp_no, dept_no, from_date, to_date) \
					values('"+ emp_no +"', '"+ dept_no +"', '"+ from_date +"', '"+ to_date +"')"
		cur.execute(sql_query)
	except:
		log.error("Unable to insert data into table. Incorrect data format")
		return {"error": "Data is not inserted. Please check the input file", "status_code": 500}

	else:
		log.info("Data in inserted successfully")
		return {"info": "Data is inserted successfully", "status_code": 200}



def insert_titles(data):

	"""
	Inserting employee title details in test.title table
	"""

	emp_no = str(data['emp_no'])
	from_date = datetime.strptime(data['salary_from'], '%d/%m/%Y').strftime('%Y-%m-%d')
	to_date = datetime.strptime(data['salary_to'], '%d/%m/%Y').strftime('%Y-%m-%d')
	title = data['title']

	try:

		sql_query = "insert into test.titles(emp_no, title, from_date, to_date) \
					values('"+ emp_no +"', '"+ title +"', '"+ from_date +"', '"+ to_date +"')"

		cur.execute(sql_query)

	except:
		log.error("Unable to insert data into table. Incorrect data format")
		return {"error": "Data is not inserted. Please check the input file", "status_code": 500}

	else:
		log.info("Data in inserted successfully")
		return {"info": "Data is inserted successfully", "status_code": 200}

def insert_salaries(data):


	"""
	Inserting employee salary details in test.salary table based on the employee title
	"""
	
	emp_no = str(data['emp_no'])
	from_date = datetime.strptime(data['salary_from'], '%d/%m/%Y').strftime('%Y-%m-%d')
	to_date = datetime.strptime(data['salary_to'], '%d/%m/%Y').strftime('%Y-%m-%d')
	salary = str(salary_role_mapper[data['title']])
	
	try:

		sql_query = "insert into test.salaries(emp_no, salary, from_date, to_date) \
					values('"+ emp_no +"', '"+ salary +"', '"+ from_date +"', '"+ to_date +"')"

		cur.execute(sql_query)

	except:
		log.error("Unable to insert data into table. Incorrect data format")
		return {"error": "Data is not inserted. Please check the input file", "status_code": 500}

	else:
		log.info("Data in inserted successfully")
		return {"info": "Data is inserted successfully", "status_code": 200}



def insert_data(data):

	emp_list = ['emp_no', 'birth_date', 'gender', 'last_name', 'first_name', 'hire_date']
	dept_emp_list = ['emp_no', 'department', 'salary_to', 'salary_from']
	salary_list = ['emp_no', 'salary_to', 'salary_from', 'title']
	emp_titles = ['emp_no', 'title', 'salary_from', 'salary_to']

	for details in data['details']:

		employee_details = dict()
		emp_dept_details = dict()
		salary_details = dict()
		title_details = dict()

		for k,v in details.items():

			if k in emp_list:
				employee_details[k] = v

			if k in dept_emp_list:
				emp_dept_details[k] = v

			if k in salary_list:
				salary_details[k] = v

			if k in emp_titles:
				title_details[k] = v

		emp_status = insert_employee(employee_details)
		dept_status = insert_dept_emp(emp_dept_details)
		title_status = insert_titles(title_details)
		salary_status = insert_salaries(salary_details)


	if emp_status['status_code'] == 502:
		return emp_status
	if dept_status['status_code'] == 501:
		return dept_status
	if emp_status['status_code'] == 500 and dept_status['status_code'] == 500 and title_status['status_code'] == 500 and salary_status['status_code'] == 500:
		return {"error": "Data is not inserted. Please check the input file", "status_code": 500}
	else:
		return {"info": "Data is inserted successfully", "status_code": 200}


















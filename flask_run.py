
from flask import Flask, jsonify
from model import eligibility as ce
from model import hire_emp as hp

import json
import logging


app = Flask(__name__)
log = logging.getLogger(__name__)

@app.route('/hire_employee/')
def json_data():

   
	with open("templates/index.json") as file:
		data = json.load(file)

	response = hp.insert_data(data)

	return jsonify(response)

@app.route("/check_eligibility/<emp_no>")
def check_eligible_for_hike(emp_no):

   response = ce.hike_eligibility(emp_no)

   return jsonify(response)


if __name__ == "__main__":
   app.run(debug = True)
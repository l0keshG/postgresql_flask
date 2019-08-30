
"""
DB access module
"""

import psycopg2 as pg
import logging

from settings import config
from errors.error import InternalServerError
logging.basicConfig(filename="newfile.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w')
log = logging.getLogger()

def connectToDb():
	"""
	Connecting to the DB by fetching the values supplied in json file
	"""
	
	try:
	    log.info(
	        "Attempting to connect to db")

	    db_details = config.load_config()
	    connectionString = "dbname={0} user={1} password={2} host={3}".format(db_details['dbname'], db_details['user'], db_details['password'], db_details['host'])
	    client = pg.connect(connectionString)
	    client.autocommit = True
	    return client.cursor()

	except Exception as exc:
	    log.error("Error connecting to mongo: %r", exc)
	else:
		log.info("Connected to db")

from flask import Flask
from flask import request, jsonify
from model import db
from model import Expense
from model import CreateDB
from model import app as application
import simplejson as json
from sqlalchemy.exc import IntegrityError
import os
from flask import Response
import redis
import sys
import signal

r = redis.StrictRedis(host='localhost', port=6379, db=0)

# initate flask app
app = Flask(__name__)

@app.route('/')
def index():
	str = 'Welcome to Part 2 of Docker-Composed for Flask & Mysql \n'
	str +='You are connected to port ' + sys.argv[1] + '\n'
	return str

@app.route('/v1/expenses', methods = ['POST'])
def new_expense():
	try:
		dataDict = json.loads(request.data)
		dataDict['status'] = "pending"
		dataDict['decision_date'] = ""

		e = Expense(dataDict['name'], 
				dataDict['email'], 
				dataDict['category'], 
				dataDict['description'],
				dataDict['link'],
				dataDict['estimated_costs'],
				dataDict['submit_date'],
				dataDict['status'],
				dataDict['decision_date'])

		db.session.add(e)
		db.session.commit()
		dataDict['id'] = e.id
		return Response(json.dumps(dataDict), status=201)
	except IntegrityError:
		return json.dumps({'status':False})
	

@app.route('/v1/expenses/<expense_id>', methods = ['PUT', 'GET', 'DELETE'])
def expense_with_id(expense_id):
	if request.method == 'GET':
		try:
			expense_dict = {}
			q = Expense.query.filter_by(id=expense_id).first()
			expense_dict['id'] = q.id
			expense_dict['name'] = q.name
			expense_dict['email'] = q.email
			expense_dict['category'] = q.category
			expense_dict['description'] = q.description
			expense_dict['link'] = q.link
			expense_dict['estimated_costs'] = q.estimated_costs
			expense_dict['submit_date'] = q.submit_date
			expense_dict['status'] = q.status
			expense_dict['decision_date'] = q.decision_date			 
			return Response(json.dumps(expense_dict), status=200)
		except:
			return Response(status=404)

	if request.method == 'PUT':
		try:
			cost_estimate = json.loads(request.data)["estimated_costs"]
			q = Expense.query.filter_by(id=expense_id).first()
			q.estimated_costs = cost_estimate
			return Response(status=202)
		except:
			return Response(status=404)

	if request.method == 'DELETE':
		try:
			Expense.query.filter_by(id=expense_id).delete()
			db.session.commit()
			return Response(status=204)
		except:
			return Response(status=204)

			

@app.route('/v1/expenses/deleteall', methods = ['DELETE'])
def deleteAll():

	try:	
		Expense.query.delete()
		db.session.commit()
		return Response(status = 350)
	except:
		return  Response(status = 351)
	

@app.route('/createtbl')
def createUserTable():
	try:
		db.create_all()
		return json.dumps({'status':True})
	except IntegrityError:
		return json.dumps({'status':False})



@app.route('/createdb')
def createDatabase():
	HOSTNAME = 'mysqlserver'
	try:
		HOSTNAME = 'localhost'#request.args['hostname']
	except:
		pass
	
	while(1):
		try:
			database = CreateDB(hostname = HOSTNAME)
		except:
			continue
		break

	return json.dumps({'status':True})


def signal_handler(signal, frame):
	print "Ctrl C - Stopping app"
	#r.delete(sys.argv[1])
	sys.exit(0)

# run app service 
if __name__ == "__main__":
	if len(sys.argv) <= 1:
		print "port missing, usage : app.py <port#>\n"
		sys.exit(1)
	createDatabase()
        createUserTable()
	print("Main starts, port = ", sys.argv[1] )
	r.set(sys.argv[1], "true")
	signal.signal(signal.SIGINT, signal_handler)
        app.run(host="0.0.0.0", port=int(sys.argv[1]), debug=True)

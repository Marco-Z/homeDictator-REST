from flask import request
import datetime as dt
from flask_restful import Resource, reqparse
from homeDictator.common.db import db, Finance, User, _all, _first
from sqlalchemy.sql.functions import func

class list(Resource):
	def get(self, group_id):
		parser = reqparse.RequestParser()
		parser.add_argument('offset')
		parser.add_argument('count')
		args = parser.parse_args()
		try: offset = int(args['offset'])
		except: offset = 0
		try: count = int(args['count'])
		except: count = 10
		movements = (db.session.query(Finance.amount,
									  Finance.date,
									  Finance.description,
									  User.name.label('user')
									 )
							   .order_by(Finance.date.desc())
							   .join(User)
							   .filter_by(group=group_id)
							   .offset(offset)
							   .limit(count))
		count = (db.session.query(func.count(Finance.id).label('number'))
							   .join(User)
							   .filter_by(group=group_id)).first()[0]
		return {'movements': _all(movements), 'count': count}

class create(Resource):
	def post(self, group_id):
		try:
			user = request.form['user']
			print(user)
			amount = request.form['amount']
			print(amount)
			date = dt.datetime.strptime(request.form['date'], "%Y-%m-%d").date()
			print(date)
			description = request.form['description']
			print(description)
		except Exception as e:
		   print(str(e))
		   return {'message': 'invalid movement post'+ str(e)}
		movement = Finance(user, amount, date, description)
		db.session.add(movement)
		db.session.commit()
		return movement.toJSON()

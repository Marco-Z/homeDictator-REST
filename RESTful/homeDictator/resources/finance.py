from flask import request
import datetime as dt
from flask_restful import Resource, reqparse
from homeDictator.common.db import db, Finance, User

class balance(Resource):
	def get(self, group_id):
		users = User.query.filter_by(group=group_id).all()
		if users is None:
			return {'message': 'error'}
		return [user.toJSON() for user in users]

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
		movements = (Finance.query.order_by(Finance.date.desc())
								  .join(User)
								  .filter_by(group=group_id)
								  .offset(offset)
								  .limit(count)
								  .all())
		return [movement.toJSON() for movement in movements]

class create(Resource):
	def post(self, group_id):
		try:
			user = request.form['user']
			amount = request.form['amount']
			date = dt.datetime.strptime(request.form['date'], "%d-%m-%Y").date()
			description = request.form['description']
		except:
		   return {'message': 'invalid movement post'}
		movement = Finance(user, amount, date, description)
		db.session.add(movement)
		db.session.commit()
		return movement.toJSON()

class destroy(Resource):
	def post(self, group_id):
		try:
			_id = int(request.form['id'])
		except Exception:
			return {'message': 'invalid request'}
		movement = (Finance.query.filter_by(id=_id)
								 .join(User)
								 .filter_by(group=group_id)
								 .first())
		if movement is not None:
			db.session.delete(movement)
			db.session.commit()
			return movement.toJSON()
		else:
			return {'message': 'no movement'}


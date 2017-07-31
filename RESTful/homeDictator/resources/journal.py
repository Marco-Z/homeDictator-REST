from flask import request
import datetime as dt
from flask_restful import Resource, reqparse
from homeDictator.common.db import db, User, Journal

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
		activities = (Journal.query.order_by(Journal.date.desc())
								   .join(User)
								   .filter_by(group=group_id)
								   .offset(offset)
								   .limit(count)
								   .all())
		return [activity.toJSON() for activity in activities]

class _type(Resource):
	def get(self, group_id, _type):
		parser = reqparse.RequestParser()
		parser.add_argument('offset')
		parser.add_argument('count')
		args = parser.parse_args()
		try: offset = int(args['offset'])
		except: offset = 0
		try: count = int(args['count'])
		except: count = 10
		activities = (Journal.query.order_by(Journal.date.desc())
								   .filter_by(task=_type)
								   .join(User)
								   .filter_by(group=group_id)
								   .offset(offset)
								   .limit(count)
								   .all())
		return [activity.toJSON() for activity in activities]

# TO FIX
class last(Resource):
	def get(self, group_id):
		activities = (Journal.query.order_by(Journal.date.desc())
								   .group_by(Journal.task)
								   .join(User)
								   .filter_by(group=group_id)
								   .all())
		return [activity.toJSON() for activity in activities]


class create(Resource):
	def post(self, group_id):
		try:
			user = request.form['user']
			task = request.form['task']
			date = dt.datetime.strptime(request.form['date'], "%d-%m-%Y").date()
			description = request.form['description']
		except Exception as e:
			return {'message': 'invalid activity post: ' + str(e)}
		activity = Journal(user, task, date, description)
		db.session.add(activity)
		db.session.commit()
		return activity.toJSON()

class destroy(Resource):
	def post(self, group_id):
		try:
			_id = int(request.form['id'])
		except Exception:
			return {'message': 'invalid request'}
		activity = (Journal.query.filter_by(id=_id)
								 .join(User)
								 .filter_by(group=group_id)
								 .first())
		if activity is not None:
			db.session.delete(activity)
			db.session.commit()
			return activity.toJSON()
		else:
			return {'message': 'no activity'}


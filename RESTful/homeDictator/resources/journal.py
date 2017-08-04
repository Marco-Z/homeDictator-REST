from flask import request
import datetime as dt
from flask_restful import Resource, reqparse
from homeDictator.common.db import db, User, Journal, Task, _all, _first
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
		activities = (db.session.query(Journal.id,
									   Journal.date,
									   User.name.label('user'),
									   Task.name.label('task'),
								  )
							 .join(Task)
							 .join(User)
							 .filter_by(group=group_id)
							 .offset(offset)
							 .limit(count))
		count = (db.session.query(func.count(Journal.id).label('number'))
							   .join(User)
							   .filter_by(group=group_id)).first()[0]
		return {'activities': _all(activities), 'count': count}

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


class to_do(Resource):
	def get(self, group_id):
		points = (db.session.query(Journal.task,
								   Journal.date,
								   Task.name
								  )
							.filter(dt.date.today() - Journal.date > Task.frequency )
							.join(Task)
							.group_by(Journal.task)
							)

		return _all(points)

# TO FIX
# not ordered
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
			date = dt.datetime.strptime(request.form['date'], "%Y-%m-%d").date()
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


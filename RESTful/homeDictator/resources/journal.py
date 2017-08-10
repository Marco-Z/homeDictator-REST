from flask import request
import datetime as dt
from flask_restful import Resource, reqparse
from homeDictator.common.db import db, User, Journal, Task, _all, _first
from sqlalchemy.sql.functions import func
import copy

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
									   Journal.description,
									   User.name.label('user'),
									   Task.name.label('task'),
								  )
							 .join(Task)
							 .join(User)
							 .filter_by(group=group_id)
							 .order_by(Journal.date.desc())
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
		activities = (db.session.query(Journal.id,
									   Journal.date,
									   Journal.description,
									   User.name.label('user'),
									   Task.name.label('task'),
								  )
								.order_by(Journal.date.desc())
								.filter_by(task=_type)
								.join(Task)
								.join(User)
								.filter_by(group=group_id)
								.offset(offset)
								.limit(count))
		return _all(activities)


class to_do(Resource):
	def get(self, group_id):
		tasks = _all(db.session.query(Task.name,
									  Task.value,
									  Task.group,
									  Task.frequency)
							   .filter_by(group=group_id))
		last  = _all(db.session.query(Journal.id,
									  Task.name,
									  Task.frequency,
									  func.max(Journal.date).label('date')
									  )
							   .join(Task)
							   .filter_by(group=group_id)
							   .group_by(Task.name)
							   .order_by(Journal.date.desc()))
		todo = copy.deepcopy(tasks)
		for t in tasks:
			if t['value'] < 0:
				todo.remove(t)
			elif t['frequency'] < 0:
				todo.remove(t)
			else:
				try:
					res = next((item for item in last if item['name'] == t['name']))
					d = dt.datetime.strptime(res['date'], "%Y-%m-%d").date()
					if (dt.date.today() - d).days > res['frequency']:
						todo.remove(t)
				except: pass
		return todo

class last(Resource):
	def get(self, group_id):
		tasks = (db.session.query(Journal.id,
								  Task.name.label('task'),
								  User.name.label('user'),
								  Journal.description,
								  func.max(Journal.date).label('date')
								  )
						   .join(User)
						   .join(Task)
						   .group_by(Task.name)
						   .order_by(Journal.date.desc()))

		return _all(tasks)

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


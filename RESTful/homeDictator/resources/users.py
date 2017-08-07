from flask import request
from flask_restful import Resource, reqparse
from homeDictator.common.db import db, User, Journal, Task, _all, _first
from sqlalchemy.sql.functions import func

class _get(Resource):
	def get(self, group_id, user_id):
		user = (User.query.order_by(User.name) 
						  .filter_by(group=group_id) 
						  .filter_by(id=user_id)
						  .first())
		if user is None:
			return {'message': 'no such user in this group'}
		else:
			return user.toJSON()

class search(Resource):
	def post(self):
		name = request.form['name']
		user = (User.query.filter_by(name=name)
						  .first())
		if user is None:
			return {'message': 'no such user in this group'}
		else:
			return user.toJSON()

class journal(Resource):
	def get(self, group_id, user_id):
		activities = (Journal.query.filter_by(user=user_id)
								   .join(User)
								   .order_by(User.name) 
								   .filter_by(group=group_id)
								   .all())
		return [activity.toJSON() for activity in activities]

class gist(Resource):
	def get(self, group_id, user_id):
		journal = (db.session.query(Journal.date,
									func.sum(Task.value).label('points'))
							 .join(Task)
							 .join(User)
							 .filter_by(id=user_id)
							 .group_by(Journal.date) 
							 .order_by(Journal.date))
		return _all(journal)

class create(Resource):
	def post(self, group_id):
		name = request.form['name']
		password = request.form['password']
		avatar = request.form['avatar']
		group = group_id
		if (name is None or 
		    password is None or 
		    avatar is None or 
		    group is None):
		   return {'message': 'invalid user'}
		else:
			user = User(name, password, avatar, group)
			db.session.add(user)
			db.session.commit()
			return user.toJSON()

class update(Resource):
	def post(self, group_id, user_id):
		try:
			user = (User.query.filter_by(group=group_id)
							  .filter_by(id=user_id)
							  .first())
			if user is None:
				return {'message': 'no such user in this group'}
			else:
				try:
					name = request.form['name']
					if len(name)>0:
						user.name = name
				except: pass
				try:
					password = request.form['password']
					if len(password)>0:
						user.password = password
				except: pass
				try:
					avatar = request.form['avatar']
					if len(avatar)>0:
						user.avatar = avatar
				except: pass
				try:
					db.session.commit()
				except Exception as e: return {'message': str(e)}
				return user.toJSON()
		except Exception as e:
			return {'message': str(e)}

class update_balance(Resource):
	def post(self, group_id, user_id):
		try:
			user = (User.query.filter_by(group=group_id)
							  .filter_by(id=user_id)
							  .first())
			if user is None:
				return {'message': 'no such user in this group'}
			else:
				try:
					delta = float(request.form['delta'])
					user.balance += delta
				except Exception as e:
					return {'message': str(e)}
				try:
					db.session.commit()
				except Exception as e: return {'message': str(e)}
				return user.toJSON()
		except Exception as e:
			return {'message': str(e)}

class destroy(Resource):
	def post(self, group_id, user_id):
		user = (User.query.filter_by(group=group_id)
						  .filter_by(id=user_id)
						  .first())
		if user is None:
			return {'message': 'no such user in this group'}
		else:
			db.session.delete(user)
			db.session.commit()
			return user.toJSON()


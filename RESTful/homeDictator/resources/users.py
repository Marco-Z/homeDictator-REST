from flask import request
from flask_restful import Resource, reqparse
from homeDictator.common.db import db, User, Journal

class _get(Resource):
	def get(self, group_id, user_id):
		user = (User.query.filter_by(group=group_id)
						  .filter_by(id=user_id)
						  .first())
		if user is None:
			return {'message': 'no such user in this group'}
		else:
			return user.toJSON()

class journal(Resource):
	def get(self, group_id, user_id):
		activities = (Journal.query.filter_by(user=user_id)
								   .join(User)
								   .filter_by(group=group_id)
								   .all())
		return [activity.toJSON() for activity in activities]

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
					user.name = name
				except: pass
				try:
					password = request.form['password']
					user.password = password
				except: pass
				try:
					avatar = request.form['avatar']
					user.avatar = avatar
				except: pass
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


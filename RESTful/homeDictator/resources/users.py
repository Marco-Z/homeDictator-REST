from flask import request
from flask_restful import Resource, reqparse
from homeDictator.common.db import query_db

users_list = [{'id': 0,
			   'name': 'marco',
			   'password': 'muschio',
			   'avatar': 'foto',
			   'group': 1},
			  {'id': 1,
			   'name': 'matteo',
			   'password': 'muschio',
			   'avatar': 'foto',
			   'group': 1}
			   ]
use_id = 2

class _get(Resource):
	def get(self, group_id, user_id):
		user = next((x for x in users_list if user_id == x['id']),None)
		if user is None:
			return {'message': 'error'}
		return {'user': user}

class journal(Resource):
	def get(self, group_id, user_id):
		from homeDictator.resources.journal import activities_list
		return activities_list

class create(Resource):
	def post(self, group_id):
		global use_id
		user = {}
		user['id'] = use_id
		use_id+=1
		user['name'] = request.form['name'] # id of user
		user['password'] = request.form['password']
		user['avatar'] = request.form['avatar']
		user['group'] = group_id
		users_list.append(user)
		return {'user': user}

class update(Resource):
	def post(self, group_id, user_id):
		try:
			user = next((x for x in users_list if user_id == x['id']),None)
			if user is None:
				# error
				return {'message': 'error'}
			user['name'] = request.form['name'] # id of user
			user['password'] = request.form['password']
			user['avatar'] = request.form['avatar']
			return {'user': user}
		except Exception:
			return {'message': 'error'}

class destroy(Resource):
	def post(self, group_id, user_id):
		user = next((x for x in users_list if user_id == x['id']),None)
		if user is None:
			# error
			return {'message': 'error'}
		users_list.remove(user)
		return {'user': user}
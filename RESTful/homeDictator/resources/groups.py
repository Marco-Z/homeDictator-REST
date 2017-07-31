from flask import request
from flask_restful import Resource, reqparse
from homeDictator.common.db import query_db
from functools import lru_cache

groups_list = [{'id': 0, 'name': '2 piano'},{'id': 1, 'name': '3 piano'}]
grogroup_id = 2

class get_group(Resource):
	@lru_cache(maxsize=32)
	def get(self, group_id):
		group = next((x for x in groups_list if group_id == x['id']),None)
		if group is None:
			# error
			return {'message': 'error'}
		return group

class create(Resource):
	def post(self):
		global grogroup_id
		group = {}

		group['id'] = grogroup_id
		grogroup_id+=1
		group['name'] = request.form['name']
		groups_list.append(group)
		return group

class update(Resource):
	def post(self, group_id):
		try:
			group_id = int(request.form['id'])
			# update case
			group = next((x for x in groups_list if group_id == x['id']),None)
			if group is None:
				# error
				return {'message': 'error'}
			group['name'] = request.form['name']
			return {'group': group}
		except Exception:
			return {'message': 'error'}

class destroy(Resource):
	def post(self, group_id):
		group = next((x for x in groups_list if group_id == x['id']),None)
		if group is None:
			# error
			return {'message': 'error'}
		groups_list.remove(group)
		return {'group': group}


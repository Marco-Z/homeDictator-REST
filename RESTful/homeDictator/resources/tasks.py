from flask import request
from flask_restful import Resource, reqparse
from homeDictator.common.db import query_db

tasks_list = [ {'id': 0,
				'name': 'piatti',
				'frequency': 1980,
				'value': 2,
				'description':'lavare i piatti'},
			   {'id': 1,
				'name': 'aspirapolvere',
				'frequency': 7,
				'value': 5,
				'description': 'passare l\'aspirapolvere'}
				]
tas_id = 2


class list(Resource):
	def get(self, group_id):
		return tasks_list

class create(Resource):
	def post(self, group_id):
		global tas_id
		task = {}
		task['id'] = tas_id
		tas_id+=1
		task['name'] = request.form['name'] # id of user
		task['frequency'] = request.form['frequency'] # id of task
		task['value'] = request.form['value']
		task['description'] = request.form['description']
		tasks_list.append(task)
		return {'activity': task}

class update(Resource):
	def post(self, group_id):
		try:
			_id = int(request.form['id'])
			# update case
			task = next((x for x in tasks_list if _id == x['id']),None)
			if task is None:
				# error
				return {'message': 'error'}
			task['name'] = request.form['name']
			task['frequency'] = request.form['frequency']
			task['description'] = request.form['description']
			task['value'] = request.form['value']
			return {'task': task}
		except Exception:
			return {'message': 'error'}

class destroy(Resource):
	def post(self, group_id):
		# delete
		try:
			_id = int(request.form['id'])
		except Exception:
			_id = None
		task = next((x for x in tasks_list if _id == x['id']),None)
		if task is None:
			# error
			return {'message': 'error'}
		tasks_list.remove(task)
		return {'task': task}



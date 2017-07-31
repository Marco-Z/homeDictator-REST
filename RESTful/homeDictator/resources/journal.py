from flask import request
from flask_restful import Resource, reqparse
from homeDictator.common.db import query_db

activities_list = [{'id': 0,
					'user': 2,
					'task': 1,
					'date': '30-07-2017',
					'description': None},
				   {'id': 1,
					'user': 4,
					'task': 10,
					'date': '30-07-2017',
					'description': None}
					]
act_id = 2

def get_last_activities_for_each_type():
	return activities_list



class list(Resource):
	def get(self, group_id):
		parser = reqparse.RequestParser()
		parser.add_argument('offset')
		parser.add_argument('count')
		args = parser.parse_args()
		try: offset = int(args['offset'])
		except: offset = None
		try: count = int(args['count'])
		except: count = None
		if offset is not None and count is not None:
			return activities_list[offset:offset+count]
		else:
			if offset is None:
				offset = 0
			if count is None:
				count = 10
			return activities_list[offset:offset+count]

class _type(Resource):
	def get(self, group_id, _type):
		parser = reqparse.RequestParser()
		parser.add_argument('offset')
		parser.add_argument('count')
		args = parser.parse_args()
		try: offset = int(args['offset'])
		except: offset = None
		try: count = int(args['count'])
		except: count = None
		if _type is not None:
			if offset is None:
				offset = 0
			if count is None:
				count = 10
			ac_list = [x for x in activities_list if x['task'] == _type]
			return ac_list[offset:offset+count]
		else:
			return {'message': 'error'}

class last(Resource):
	def get(self, group_id):
			return get_last_activities_for_each_type()

class create(Resource):
	def post(self, group_id):
		global act_id
		activity = {}
		activity['id'] = act_id
		act_id+=1
		activity['user'] = request.form['user'] # id of user
		activity['task'] = request.form['task'] # id of task
		activity['date'] = request.form['date']
		activity['description'] = request.form['description']
		activities_list.append(activity)
		return {'activity': activity}

class destroy(Resource):
	def post(self, group_id):
		# delete
		try:
			_id = int(request.form['id'])
		except Exception:
			_id = None
		activity = next((x for x in activities_list if _id == x['id']),None)
		if activity is None:
			# error
			return {'message': 'error'}
		activities_list.remove(activity)
		return {'activity': activity}


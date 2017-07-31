from flask import request
from flask_restful import Resource, reqparse
from homeDictator.common.db import query_db

movements = [{'user':'marco',
			  'amount':'10.25',
			  'date': '31-07-2017',
			  'description': 'prova',
			  'id': 0 }
			]
bal = [{'user': 'marco',
		'balance': 10.21},
	   {'user': 'matteo',
		'balance': -10.21}
	  ]
mov_id = 0

class balance(Resource):
	def get(self, group_id):
		return bal

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
		return movements[offset:offset+count]

class create(Resource):
	def post(self, group_id):
		global mov_id
		movement = {}

		movement['id'] = mov_id
		mov_id+=1
		movement['user'] = request.form['user']
		movement['amount'] = request.form['amount']
		movement['date'] = request.form['date']
		movement['description'] = request.form['description']
		movements.append(movement)
		return {'movement': movement}

class update(Resource):
	def post(self, group_id):
		try:
			_id = int(request.form['id'])
			# update case
			movement = next((x for x in movements if _id == x['id']),None)
			if movement is None:
				# error
				return {'message': 'error'}
			movement['user'] = request.form['user']
			movement['amount'] = request.form['amount']
			movement['date'] = request.form['date']
			movement['description'] = request.form['description']
			return {'movement': movement}
		except Exception:
			return {'message': 'error'}

class destroy(Resource):
	def post(self, group_id):
		# delete
		try:
			_id = int(request.form['id'])
		except Exception:
			_id = None
		movement = next((x for x in movements if _id == x['id']),None)
		if movement is None:
			# error
			return {'message': 'error'}
		movements.remove(movement)
		return {'movement': movement}


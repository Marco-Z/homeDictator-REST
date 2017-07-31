from flask import request
from flask_restful import Resource, reqparse
from homeDictator.common.db import db, Group
# from functools import lru_cache

class get_group(Resource):
	# @lru_cache(maxsize=32)
	def get(self, group_id):
		group = Group.query.filter_by(id=group_id).first()
		if group is None:
			return {'message': 'No such group'}
		return group.toJSON()

class create(Resource):
	def post(self):
		name = request.form['name']
		group = Group(name)
		db.session.add(group)
		db.session.commit()
		return group.toJSON()

class update(Resource):
	def post(self, group_id):
		try:
			group = Group.query.filter_by(id=group_id).first()
			if group is None:
				return {'message': 'No such group'}
			name = request.form['name']
			if name is not None:
				group.name = name
				db.session.commit()
				return group.toJSON()
		except Exception as e:
			return {'message': str(e)}

class destroy(Resource):
	def post(self, group_id):
		group = Group.query.filter_by(id=group_id).delete()
		db.session.commit()
		return group


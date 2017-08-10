from flask import request
from flask_restful import Resource, reqparse
from homeDictator.common.db import db, Group, User, Journal, Finance, Task, _all, _first
from flask_restful.utils import cors 
import json 
from sqlalchemy.sql.functions import func

# from functools import lru_cache

class get_group(Resource):
	# @lru_cache(maxsize=32)
	def get(self, group_id):
		group = Group.query.filter_by(id=group_id).first()
		if group is None:
			return {'message': 'No such group'}
		members = (db.session.query(User.name,
									User.id,
									func.sum(Task.value).label('points'),
									User.password,
									User.balance
								  )
							 .filter_by(group=group_id)
							 .outerjoin(Journal)
							 .outerjoin(Task)
							 .group_by(User.id)
							 .order_by(func.sum(Task.value).desc()))
		group.members = _all(members) 
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
			if name is not None and len(name)>0:
				group.name = name
				db.session.commit()
				return group.toJSON()
		except Exception as e:
			return {'message': str(e)}

class destroy(Resource):
	def post(self, group_id):
		group = get_group().get(group_id=group_id)
		Group.query.filter_by(id=group_id).delete()

		# cascade
		users = _all(db.session.query(User.id).filter_by(group=group_id))
		ul = User.query.filter_by(group=group_id).delete()
		t = Task.query.filter_by(group=group_id).delete()
		for u in users:
			print(u)
			f = Finance.query.filter_by(user=u['id']).delete()
			j = Journal.query.filter_by(user=u['id']).delete()

		db.session.commit()
		return group


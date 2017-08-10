from flask import request
from flask_restful import Resource, reqparse
from homeDictator.common.db import db, Group
from flask_restful.utils import cors 
import json 
from sqlalchemy.sql.functions import func

class read(Resource):
	def get(self, group_id):
		response = db.session.query(Group.shopping_list).filter_by(id=group_id).one()
		return(response[0])

class write(Resource):
	def post(self, group_id):
		try:
			shopping = request.form['list']
		except Exception:
			return {'message': 'invalid request'}
		try:
			group = Group.query.filter_by(id=group_id).first()
			if group is None:
				return {'message': 'No such group'}
			if shopping is not None:
				group.shopping_list = shopping
				db.session.commit()
				return shopping
		except Exception as e:
			return {'message': str(e)}

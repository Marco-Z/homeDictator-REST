from flask import request
from flask_restful import Resource, reqparse
from homeDictator.common.db import db, Group, User, Journal, Task, _all, _first
from flask_restful.utils import cors 
import json 
from sqlalchemy.sql.functions import func

class read(Resource):
	# @lru_cache(maxsize=32)
	def get(self, group_id):
		myfile = open('shopping_list.txt', 'r')
		shopping = myfile.read()
		print(shopping)
		myfile.close()
		return shopping

class write(Resource):
	def post(self, group_id):
		try:
			shopping = request.form['list']
		except Exception:
			return {'message': 'invalid request'}
		myfile = open('shopping_list.txt', 'w')
		print('writing---------------')
		print(shopping)
		myfile.write(shopping)
		myfile.flush()
		myfile.close()
		return shopping

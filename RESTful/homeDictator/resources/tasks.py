from flask import request
from flask_restful import Resource, reqparse
from homeDictator.common.db import db, User, Task, Journal

class list(Resource):
	def get(self, group_id):
		tasks = Task.query.filter_by(group=group_id).all()
		if tasks is None:
			return {'message': 'no tasks found'}
		return [task.toJSON() for task in tasks]

class create(Resource):
	def post(self, group_id):
		try:
			name = request.form['name']
			frequency = request.form['frequency']
			value = request.form['value']
		except Exception as e:
			return {'message': 'invalid activity post: ' + str(e)}
		task = Task(name, frequency, value, group_id)
		db.session.add(task)
		db.session.commit()
		return task.toJSON()

class update(Resource):
	def post(self, group_id):
		try:
			_id = request.form['id']
		except: return {'message': 'invalid request'}
		try:
			task = (Task.query.filter_by(group=group_id)
							  .filter_by(id=_id)
							  .first())
			if task is None:
				return {'message': 'no such task in this group'}
			else:
				try:
					name = request.form['name']
					if len(name)>0:
						task.name = name
				except: pass
				try:
					frequency = request.form['frequency']
					if len(frequency)>0:
						task.frequency = frequency
				except: pass
				try:
					value = request.form['value']
					if len(value)>0:
						task.value = value
				except: pass
				try:
					db.session.commit()
				except Exception as e: return {'message': str(e)}
				return task.toJSON()
		except Exception as e:
			return {'message': str(e)}


		try:
			_id = int(request.form['id'])
			# update case
			task = next((x for x in tasks_list if _id == x['id']),None)
			if task is None:
				# error
				return {'message': 'error'}
			task['name'] = request.form['name']
			task['frequency'] = request.form['frequency']
			task['value'] = request.form['value']
			return {'task': task}
		except Exception:
			return {'message': 'error'}

class destroy(Resource):
	def post(self, group_id):
		try:
			_id = int(request.form['id'])
		except Exception:
			return {'message': 'invalid request'}
		task = (Task.query.filter_by(id=_id)
						  .filter_by(group=group_id)
						  .first())
		if task is not None:
			db.session.delete(task)
			(Journal.query.filter_by(task=_id)
						  .delete())
			db.session.commit()
			return task.toJSON()
		else:
			return {'message': 'no task'}


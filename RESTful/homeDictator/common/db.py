from flask_sqlalchemy import SQLAlchemy
import datetime as dt
import json
from sqlalchemy.orm import relationship

db = SQLAlchemy()

def _all(query):
	res = []
	data = query.all()
	schema = query.column_descriptions
	for row in data:
		r = {}
		for i,column in enumerate(schema):
			r[column['name']] = row[i]
			if column['name'] == 'date':
				r[column['name']] = row[i].strftime("%Y-%m-%d")
		res.append(r)
	return res

def _first(query):
	data = query.first()
	schema = query.column_descriptions
	r = {}
	for i,column in enumerate(schema):
		r[column['name']] = row[i]
		if column['name'] == 'date':
			r[column['name']] = row[i].strftime("%Y-%m-%d")
	return r

class Finance(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user = db.Column(db.Integer, db.ForeignKey('user.id'))
	amount = db.Column(db.Float)
	date = db.Column(db.Date)
	description = db.Column(db.Text)

	user_id = relationship("User", single_parent=True)

	def __init__(self, user, amount, date, description):
		self.user = user
		self.amount = amount
		self.date = date
		self.description = description

	def toJSON(self):
		return ({'id': self.id, 
				'user': self.user,
				'amount': self.amount,
				'date': self.date.strftime("%d-%m-%Y"),
				'description': self.description
				})

class Group(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), unique=True)
	shopping_list = db.Column(db.Text, default='')
	members = []

	def __init__(self, name):
		self.name = name

	def toJSON(self):
		return ({'id': self.id, 
				 'name': self.name,
				 'members': self.members
				})

class Journal(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user = db.Column(db.Integer, db.ForeignKey('user.id'))
	task = db.Column(db.Integer, db.ForeignKey('task.id'))
	date = db.Column(db.Date)
	description = db.Column(db.Text)

	user_id = relationship("User", single_parent=True)
	task_id = relationship("Task", single_parent=True)
	def __init__(self, user, task, date, description):
		self.user = user
		self.task = task
		self.date = date
		self.description = description

	def toJSON(self):
		return ({'id': self.id, 
				'user': self.user,
				'task': self.task,
				'date': self.date.strftime("%d-%m-%Y"),
				'description': self.description
				})

class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), unique=True)
	frequency = db.Column(db.Integer)
	value = db.Column(db.Integer)
	group = db.Column(db.Integer, db.ForeignKey('group.id'))

	group_id = relationship("Group", single_parent=True)

	def __init__(self, name, frequency, value, group):
		self.name = name
		self.frequency = frequency
		self.value = value
		self.group = group

	def toJSON(self):
		return ({'id': self.id, 
				'name': self.name,
				'frequency': self.frequency,
				'value': self.value,
				'group': self.group
				})
				
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), unique=True)
	balance = db.Column(db.Float, default=0.0)
	password = db.Column(db.String(66))
	group = db.Column(db.Integer, db.ForeignKey('group.id'))

	group_id = relationship("Group", single_parent=True)

	def __init__(self, name, password, group):
		self.name = name
		self.password = password
		self.group = group

	def toJSON(self):
		return ({'id': self.id, 
				'name': self.name,
				'password': self.password,
				'balance': self.balance,
				'group': self.group
				})
				
from flask_sqlalchemy import SQLAlchemy
import datetime as dt
import json

db = SQLAlchemy()

class Finance(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user = db.Column(db.Integer, db.ForeignKey('user.id'))
	amount = db.Column(db.Float)
	date = db.Column(db.Date)
	description = db.Column(db.Text)

	def __init__(self, user, amount, date, description):
		self.user = user
		self.amount = amount
		self.date = date
		self.description = description

	def toJSON(self):
		return {'id': self.id, 
				'user': self.user,
				'amount': self.amount,
				'date': self.date.strftime("%d-%m-%Y"),
				'description': self.description
				}

class Group(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), unique=True)

	def __init__(self, name):
		self.name = name

	def toJSON(self):
		return {'id': self.id, 
				'name': self.name}

class Journal(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user = db.Column(db.Integer, db.ForeignKey('user.id'))
	task = db.Column(db.Integer, db.ForeignKey('task.id'))
	date = db.Column(db.Date)
	description = db.Column(db.Text)

	def __init__(self, user, task, date, description):
		self.user = user
		self.task = task
		self.date = date
		self.description = description

	def toJSON(self):
		return {'id': self.id, 
				'user': self.user,
				'task': self.task,
				'date': self.date.strftime("%d-%m-%Y"),
				'description': self.description
				}

class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), unique=True)
	frequency = db.Column(db.Integer)
	value = db.Column(db.Integer)
	group = db.Column(db.Integer, db.ForeignKey('group.id'))

	def __init__(self, name, frequency, value, group):
		self.name = name
		self.frequency = frequency
		self.value = value
		self.group = group

	def toJSON(self):
		return {'id': self.id, 
				'name': self.name,
				'frequency': self.frequency,
				'value': self.value,
				'group': self.group
				}
				
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), unique=True)
	balance = db.Column(db.Float, default=0.0)
	password = db.Column(db.String(64))
	avatar = db.Column(db.String(64))
	group = db.Column(db.Integer, db.ForeignKey('group.id'))

	def __init__(self, name, password, avatar, group):
		self.name = name
		self.password = password
		self.avatar = avatar
		self.group = group

	def toJSON(self):
		return {'id': self.id, 
				'name': self.name,
				'password': self.password,
				'avatar': self.avatar,
				'balance': self.balance,
				'group': self.group
				}
				
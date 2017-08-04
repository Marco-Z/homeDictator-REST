import configparser

class User(object):
	def __init__(self, usr):
		self.id = usr['id']
		self.username = usr['name']
		self.password = usr['password']
		self.balance = usr['balance']
		self.group = usr['group']

	def is_authenticated(self):
		return True


	def is_active(self):
		return True


	def is_anonymous(self):
		return False

	def get_id(self):
		return str(self.id)

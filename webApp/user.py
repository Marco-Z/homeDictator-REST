class User(object):
	def __init__(self, usr):
		self._id = int(usr['_id'])
		self.user_id = str(usr['group'])+'_'+str(usr['_id'])
		self.username = usr['name']
		self.password = usr['password']
		self.balance = float(usr['balance'])
		self.group = int(usr['group'])

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return str(self.user_id)

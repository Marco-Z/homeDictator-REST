from flask import Flask
from flask_restful import Api, reqparse
from homeDictator.resources import finance, groups, journal, tasks, users, shopping

app = Flask(__name__)
api = Api(app)

api.add_resource(finance.list, '/<int:group_id>/finance/list', endpoint='finance/list')
api.add_resource(finance.balance, '/<int:group_id>/finance/balance')
api.add_resource(finance.create, '/<int:group_id>/finance/create', endpoint='finance/create')
api.add_resource(finance.destroy, '/<int:group_id>/finance/destroy', endpoint='finance/destroy')

api.add_resource(groups.get_group, '/<int:group_id>')
api.add_resource(groups.update, '/<int:group_id>/update', endpoint='group/update')
api.add_resource(groups.destroy, '/<int:group_id>/destroy', endpoint='group/destroy')
api.add_resource(groups.create, '/create_group', endpoint='group/create')

api.add_resource(journal.list, '/<int:group_id>/journal/list', endpoint='journal/list')
api.add_resource(journal._type, '/<int:group_id>/journal/<int:_type>')
api.add_resource(journal.last, '/<int:group_id>/journal/last')
api.add_resource(journal.to_do, '/<int:group_id>/journal/to_do')
api.add_resource(journal.create, '/<int:group_id>/journal/create', endpoint='journal/create')
api.add_resource(journal.destroy, '/<int:group_id>/journal/destroy', endpoint='journal/destroy')

api.add_resource(tasks.list, '/<int:group_id>/tasks/list', endpoint='tasks/list')
api.add_resource(tasks.create, '/<int:group_id>/tasks/create', endpoint='tasks/create')
api.add_resource(tasks.update, '/<int:group_id>/tasks/update', endpoint='tasks/update')
api.add_resource(tasks.destroy, '/<int:group_id>/tasks/destroy', endpoint='tasks/destroy')

api.add_resource(users._get, '/<int:group_id>/<int:user_id>', endpoint='users/_get')
api.add_resource(users.search, '/search', endpoint='users/search')
api.add_resource(users.journal, '/<int:group_id>/<int:user_id>/journal', endpoint='users/journal')
api.add_resource(users.gist, '/<int:group_id>/<int:user_id>/gist', endpoint='users/gist')
api.add_resource(users.create, '/<int:group_id>/create_user', endpoint='users/create')
api.add_resource(users.update, '/<int:group_id>/<int:user_id>/update', endpoint='users/update')
api.add_resource(users.update_balance, '/<int:group_id>/<int:user_id>/update_balance', endpoint='users/update_balance')
api.add_resource(users.destroy, '/<int:group_id>/<int:user_id>/destroy', endpoint='users/destroy')

api.add_resource(shopping.read, '/<int:group_id>/shopping/read', endpoint='shopping/read')
api.add_resource(shopping.write, '/<int:group_id>/shopping/write', endpoint='shopping/write')

if __name__ == '__main__':
	app.run(debug=True)
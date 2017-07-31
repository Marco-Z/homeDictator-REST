from homeDictator.api import app
from homeDictator.common.db import db

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///common/homeDictator.db'
db.init_app(app)
with app.app_context():
	db.create_all()

app.run(debug=True)
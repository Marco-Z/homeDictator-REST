from homeDictator.api import app
from homeDictator.common.db import db

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///common/homeDictator.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
	db.create_all()

app.run(debug=True, host='0.0.0.0', port=5050)
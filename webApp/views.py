from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response, session, escape, json
from datetime import date
from subprocess import Popen
import os
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_openid import OpenID
import requests
from user import User

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

#login
login_m = LoginManager()
login_m.init_app(app)
#
url = 'http://localhost:5050'

#-----
@login_m.user_loader
def load_user(user_id):
	group_id = 2
	try:
		return User(requests.get(url+'/'+str(group_id)+'/'+str(user_id), data=None)) # get user info
	except:
		return None
#----
@app.route("/")
def index(error=None):
	group_id = 2
	user_id = 1
	# user_id = current_user.get_id()
	if not user_id:
		return redirect(url_for('login'))

	name = json.loads(requests.get(url+'/'+str(group_id)+'/'+str(user_id), data=None).text)['name']	# get user info
	users = json.loads(requests.get(url+'/'+str(group_id), data=None).text)['members'] # get data for each user
	tasks = json.loads(requests.get(url+'/'+str(group_id)+'/tasks/list', data=None).text) # get tasks
	todo =  json.loads(requests.get(url+'/'+str(group_id)+'/journal/to_do', data=None).text) # get tasks to do

	return render_template('index.html', users=users, tasks=tasks, todo=todo, name=name)

@app.route("/log", methods=['POST'])
def log():
	group_id = 2
	user_id = 1
	name=None
	try:
		# user_id = current_user.get_id()
		response = requests.get(url+'/'+str(group_id)+'/'+str(user_id), data=None)	# get user info
		name=json.loads(response.text)['name']
	except:
		pass
	if not name :
		error="Pleas log-in before continiung"
		return render_template('login.html', error=error)
	a = int(request.form['task'])

	data =  { 'user': user_id,
			  'task': a,
			  'date': date.today(),
			  'description': ''
			}
	response = requests.post(url+'/'+str(group_id)+'/journal/create', data=data) # create activity entry
	return redirect(url_for('index'))

@app.route("/pay", methods=['POST'])
def pay():
	group_id=2
	name=""
	try:
		u = request.form['user']
		amount = float(request.form['amount'])
		desc = request.form['description']
		resp = requests.get(url+'/'+str(group_id), data=None).text
		users = json.loads(resp)['members']
		weight = dict()
		somma = 0
		for user in users:
			n = user['name']
			weight[n] = int(request.form[n])
			somma = somma + weight[n]
		response = requests.post(url+'/'+str(group_id)+'/'+u+'/update_balance', data={'delta':amount})
		for user in users:
			_id = user['user']
			n = user['name']
			delta = -(amount*(weight[n]/somma))
			response = requests.post(url+'/'+str(group_id)+'/'+str(_id)+'/update_balance', data={'delta':delta})
		data = {'user': u,
				'amount': amount,
				'date': date.today(),
				'description': desc
				}
		response = requests.post(url+'/'+str(group_id)+'/finance/create', data=data)
		print(response.text)
		return redirect(url_for('index'))
	except Exception as e:
		return str(e)
		error="Oops, qualcoca è andato storto, controlla di aver inserito i dati correttamente"
		return redirect(url_for('index'))

@app.route("/manage_journal", methods=['GET','POST'])
def manage_journal():
	error=""
	group_id = 2
	user_id = 1
	name=None
	try:
		# user_id = current_user.get_id()
		response = requests.get(url+'/'+str(group_id)+'/'+str(user_id), data=None)	# get user info
		name=json.loads(response.text)['name']
	except:
		pass
	count = 10
	offset = 0
	try:
		count = int(request.args['count'])
	except:
		pass
	try:
		offset = int(request.args['offset'])
	except:
		pass
	payload = { 'offset' : offset,
				'count' : count }
	if request.method == 'POST':
		try:
			ac = int(request.form['activity'])
			print(ac)
			response = requests.post(url+'/'+str(group_id)+'/journal/destroy', data={'id': ac}) # delete the activity
		except:
			error="Errore nel cancellare l'attivita', riprovare"
		finally:
			response = json.loads(requests.get(url+'/'+str(group_id)+'/journal/list', params=payload).text)	# get activities list
			journal = response['activities']
			count = int(response['count'])
			return render_template('journal.html',journal=journal,name=name,error=error,offset=offset,count=count)
	else:
		response = json.loads(requests.get(url+'/'+str(group_id)+'/journal/list', params=payload).text)	# get activities list
		journal = response['activities']
		count = int(response['count'])
		return render_template('journal.html',journal=journal,name=name,offset=offset,count=count)

@app.route('/login', methods = ['GET','POST'])
def login():
	nome=""
	# if current_user.get_id():
	# 	error="Hai già eseguito l'accesso"
	# 	return redirect(url_for('index'))
	if request.method == 'POST':
		try:
			group_id = 2
			user = request.form['username']
			pssw=request.form['password']
			remember=None
			try:
				remember=bool(request.form['remember-me'])
			except:
				remember=False
			response = requests.post(url+'/'+str(group_id)+'/search', data={'name': user})	# search user
			usr=User(json.loads(response.text))
			if usr and usr.password == pssw:
				res = login_user(usr,remember=remember)
				return redirect(url_for('index'))
		except Exception as e:
			wrong="Username o password sbagliati"
			return render_template('login.html',wrong=wrong)

	
	return render_template('login.html')

# TO FIX
@app.route("/shopping_list", methods=['GET','POST'])
def shopping_list():
	group_id = 2
	user_id = 1
	name=None
	try:
		# user_id = current_user.get_id()
		response = requests.get(url+'/'+str(group_id)+'/'+str(user_id), data=None)	# get user info
		name=json.loads(response.text)['name']
	except:
		pass
	if request.method == 'POST':
		_list = request.form['list']
		_list = requests.post(url+'/'+str(group_id)+'/shopping/write', data={'list':_list.encode('utf8')}).text
		return redirect(url_for('index'))
	else:
		_list = requests.get(url+'/'+str(group_id)+'/shopping/read', data=None).text.encode('utf8').decode('unicode_escape')
		return render_template('shopping_list.html',list=_list,name=name)

@app.route("/movements")
def movements():
	group_id = 2
	user_id = 1
	name=None
	try:
		# user_id = current_user.get_id()
		response = requests.get(url+'/'+str(group_id)+'/'+str(user_id), data=None)	# get user info
		name=json.loads(response.text)['name']
	except:
		pass
	count = 10
	offset = 0
	try:
		count = int(request.args['count'])
	except:
		pass
	try:
		offset = int(request.args['offset'])
	except:
		pass
	payload = { 'offset' : offset,
				'count' : count }
	response = json.loads(requests.get(url+'/'+str(group_id)+'/finance/list', params=payload).text)
	movs = response['movements']
	count = int(response['count'])
	return render_template('finance.html',list=movs,name=name,count=count,offset=offset)

@app.route("/images/<string:nome>.jpg")
def getImage(nome):
	image_binary=mydb.get_avatar_from_name(nome)
	response = make_response(image_binary)
	response.headers['Content-Type'] = 'image/jpeg'
	#response.headers['Content-Disposition'] = 'attachment; filename=%s.jpg'%(nome) per il download
	return response

@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route("/user")
@login_required
def user_page():
	nome=None
	group=None
	try:
		nome=mydb.get_user_by_id(current_user.get_id())[1]
		group=mydb.get_userGroupId(current_user.get_id())
		gruppi_esistenti= mydb.getGroupsAndComponents()
	except:
		pass
	return render_template('user.html',nome=nome,grup=group)

@app.route("/change-avatar",methods=['POST'])
@login_required
def update_avatar():
	try:
		for f in request.files:
			file = request.files[f]	
			print(file)
			ok=mydb.change_avatar(file, current_user.get_id())
			if not ok:
				raise Exception('error')

	except:
		return json.dumps({'success':False,"status": "error",'msg': "Error,change file"}), 403, {'ContentType':'application/json'}

	print("%s ha cambiato avatar"%current_user.get_id())
	return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 



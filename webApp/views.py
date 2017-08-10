from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response, session, escape, json
from datetime import date
import os, time
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_openid import OpenID
import requests
from user import User
import plots
import configparser
from werkzeug.security import generate_password_hash, check_password_hash

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
	try:
		group_id,_id = user_id.split('_',2)
		user = json.loads(requests.get(url+'/'+str(group_id)+'/'+str(_id), data=None).text)
		return User(user) # get user info
	except Exception as e:
		print(str(e))
		return None
#----
@app.route("/")
def index(error=None):
	if current_user.get_id():
		group_id = current_user.group
		user_id = current_user._id
	else:
		return render_template('landing.html')

	name = json.loads(requests.get(url+'/'+str(group_id)+'/'+str(user_id), data=None).text)['name']	# get user info
	res = json.loads(requests.get(url+'/'+str(group_id), data=None).text) # get data for each user
	users = res['members']
	tasks = json.loads(requests.get(url+'/'+str(group_id)+'/tasks/list', data=None).text) # get tasks
	todo =  json.loads(requests.get(url+'/'+str(group_id)+'/journal/to_do', data=None).text) # get tasks to do

	plot = 'img/'+plots.points_bar_chart(plots.HList(users), app.static_folder)

	return render_template('index.html', users=users, tasks=tasks, todo=todo, name=name, time=time.time(), plot=plot)

@app.route("/signup", methods=['GET','POST'])
def signup(error=None):
	if request.method == 'GET':
		group_name = request.args['group_name']

		tasks = []
		config = configparser.ConfigParser()
		config.read('tasks.ini')
		a = config.options('points')

		for ac in a:
			row = {'name': ac}
			row['value'] = int(config['points'][ac])
			row['frequency'] = int(config['frequency'][ac])
			tasks.append(row)

		return render_template('signup.html',group_name=group_name, tasks=tasks)
	elif request.method == 'POST':
		def search(dictionary, substr):
			result = []
			for key in dictionary:
				if substr in key:
					result.append({key: dictionary[key]})
			return result

		# group
		group_name = request.form['group_name']
		response = requests.post(url+'/create_group', data={'name':group_name})
		print(json.loads(response.text))
		group_id = json.loads(response.text)['id']

		# members
		m = []
		field = 'member_name_'
		members = search(request.form.to_dict(), field)
		for member in members:
			for key in member:
				response = requests.post(url+'/'+str(group_id)+'/create_user', data={'name': member[key]})

		# tasks
		n = []
		tasks = []
		t_name = 'task_name_'
		t_value = 'task_value_'
		t_freq = 'task_frequency_'
		tasks_names = search(request.form.to_dict(), t_name)
		tasks_values = search(request.form.to_dict(), t_value)
		tasks_freqs = search(request.form.to_dict(), t_freq)

		for task in tasks_names:
			for key in task:
				n.append(key.split(t_name,1)[1])

		for i in n:
			task ={ 'name': request.form[t_name+i],
					'frequency': request.form[t_freq+i],
					'value': request.form[t_value+i]}
			response = requests.post(url+'/'+str(group_id)+'/tasks/create', data=task)
		return redirect(url_for('login'))

@app.route("/log", methods=['POST'])
@login_required
def log():
	group_id = current_user.group
	user_id = current_user._id
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
@login_required
def pay():
	group_id = current_user.group
	user_id = current_user._id
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
			_id = user['id']
			n = user['name']
			delta = -(amount*(weight[n]/somma))
			response = requests.post(url+'/'+str(group_id)+'/'+str(_id)+'/update_balance', data={'delta':delta})
		data = {'user': u,
				'amount': amount,
				'date': date.today(),
				'description': desc
				}
		response = requests.post(url+'/'+str(group_id)+'/finance/create', data=data)
		return redirect(url_for('index'))
	except Exception as e:
		return str(e)
		error="Oops, qualcoca è andato storto, controlla di aver inserito i dati correttamente"
		return redirect(url_for('index'))

@app.route("/manage_journal", methods=['GET','POST'])
@login_required
def manage_journal():
	error=""
	group_id = current_user.group
	user_id = current_user._id
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
	if current_user.get_id():
		error="Hai già eseguito l'accesso"
		return redirect(url_for('index'))
	if request.method == 'POST':
		try:
			user = request.form['username']
			pssw=request.form['password']
			remember=None
			try:
				remember=bool(request.form['remember-me'])
			except:
				remember=False
			response = requests.post(url+'/search', data={'name': user})	# search user
			usr=User(json.loads(response.text))
			if usr and check_password_hash(usr.password,pssw):
				try:
					res = login_user(usr,remember=remember)
				except Exception as e:
					print(str(e))
					raise e
				return redirect(url_for('index'))
		except Exception as e:
			print(str(e))
			wrong="Username o password sbagliati"
			return render_template('login.html',wrong=wrong)

	return render_template('login.html')

@app.route("/shopping_list", methods=['GET','POST'])
@login_required
def shopping_list():
	group_id = current_user.group
	user_id = current_user._id
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
		return render_template('shopping_list.html',list=_list[1:len(_list)-2],name=name)

@app.route("/movements")
@login_required
def movements():
	group_id = current_user.group
	user_id = current_user._id
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

@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route("/user")
@login_required
def user_page():
	group_id = current_user.group
	user_id = current_user._id
	name=None
	try:
		# user_id = current_user.get_id()
		response = requests.get(url+'/'+str(group_id)+'/'+str(user_id))	# get user info
		name=json.loads(response.text)['name']
	except:
		pass
	journal = json.loads(requests.get(url+'/'+str(group_id)+'/'+str(user_id)+'/gist').text)['gist'] # get data for user
	plot = 'img/'+plots.points_line_chart(plots.HList(journal), app.static_folder)
	tasks = json.loads(requests.get(url+'/'+str(group_id)+'/tasks/list').text) # get tasks
	response = json.loads(requests.get(url+'/'+str(group_id)).text) # get data for each user
	members = response['members']
	group_name = response['name']
	return render_template('user.html',name=name,group=group_id,group_name=group_name,members=members,tasks=tasks,time=time.time(),plot=plot)

@app.route("/update_user", methods=['POST'])
@login_required
def update_user():
	group_id = current_user.group
	user_id = current_user._id
	try:
		name = request.form['username']
	except Exception as e:
		name = None
	try:
		pssw = request.form['password']
	except Exception as e:
		pssw = None
	data={'name':name,'password':pssw}
	response = requests.get(url+'/'+str(group_id)+'/'+str(user_id), data=None)	# get user info
	old_name=json.loads(response.text)['name']

	response = requests.post(url+'/'+str(group_id)+'/'+str(user_id)+'/update', data=data)

	os.rename(app.static_folder+'\\img\\'+old_name+'.jpg', app.static_folder+'\\img\\'+name+'.jpg')
	return redirect(url_for('user_page'))

@app.route("/update_group", methods=['POST'])
@login_required
def update_group():
	group_id = current_user.group
	user_id = current_user._id
	# update group name
	try:
		group_name = request.form['group_name']
	except Exception as e:
		group_name = None
	if group_name is not None and len(group_name)>0 :
		response = requests.post(url+'/'+str(group_id)+'/update', data={'name': group_name})

	# add group member
	try:
		new_member_name = request.form['new_member_name']
		new_member_password = request.form['new_member_password']
		if len(new_member_name) > 0 and len(new_member_password) > 0:
			data = {'name': new_member_name,
					'password': new_member_password}
			response = requests.post(url+'/'+str(group_id)+'/create_user', data=data)
	except:
		pass

	# delete group member
	try:
		member_id = int(request.form['delete_user'])
		response = requests.post(url+'/'+str(group_id)+'/'+str(member_id)+'/destroy')
		if member_id == user_id:	
			logout_user()
			return redirect(url_for('index'))
	except Exception as e:
		member_id = None
	return redirect(url_for('user_page'))

@app.route("/update_task", methods=['POST'])
@login_required
def update_task():
	group_id = current_user.group
	user_id = current_user._id
	# update group name
	try:
		task_id = int(request.form['task'])

		try:
			task_name = request.form['task_name']
		except Exception as e:
			task_name = ''
		try:
			task_value = int(request.form['task_value'])
		except Exception as e:
			task_value = ''
		try:
			task_frequency = int(request.form['task_frequency'])
		except Exception as e:
			task_frequency = ''

		if task_id == 0:
			# new task
			if(len(task_name) > 0 and 
			   task_value and 
			   task_frequency > 0):
				data = {'name': task_name,
						'value': task_value,
						'frequency': task_frequency}
				response = requests.post(url+'/'+str(group_id)+'/tasks/create', data=data)
		else:
			data = {'id': task_id,
					'name': task_name,
					'value': task_value,
					'frequency': task_frequency}
			response = requests.post(url+'/'+str(group_id)+'/tasks/update', data=data)

	except Exception as e:
		print(e)

	return redirect(url_for('user_page'))

@app.route("/delete_group", methods=['GET'])
@login_required
def delete_group():
	group_id = current_user.group
	user_id = current_user._id
	response = requests.post(url+'/'+str(group_id)+'/destroy')

	logout_user()
	return redirect(url_for('login'))

@app.route("/change-avatar",methods=['POST'])
@login_required
def update_avatar():
	group_id = current_user.group
	user_id = current_user._id
	try:
		for f in request.files:
			file = request.files[f]	
			file.save(app.static_folder+'\\img\\users\\'+current_user.get_id()+'.jpg')

	except:
		return json.dumps({'success':False,"status": "error",'msg': "Error,change file"}), 403, {'ContentType':'application/json'}

	print("%s changed avatar"%current_user.get_id())
	return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 



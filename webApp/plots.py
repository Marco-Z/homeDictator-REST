import json
import requests
from requests.auth import HTTPBasicAuth
from functools import lru_cache
 
auth = HTTPBasicAuth('Marco-Z', 'mEmCZp7RWjgKujDXqVqG')
headers = {'Plotly-Client-Platform': 'python'}

@lru_cache(maxsize=32)
def points_bar_chart(people,static_path):
	x = []
	y = []
	for person in people:
		x.append(person['name'])
		y.append(person['points'])

	color = 'rgb(25, 118, 210)'
	payload = {
		"figure": { 
			"data": [
				{
				'x': x, 
				'y': y, 
				'marker': {'color': 'rgb(250, 155, 80)'}, 
				'type': 'bar'
				}
			],
        	"layout": {
				"width": 500,
				"height": 300,
			    "format": "png",
			    "encoded": 'true'
			}
		},
		"width": 700,
		"height": 400,
		"scale": 2
	}

	r = requests.post('https://api.plot.ly/v2/images', auth=auth, headers=headers, json=payload)

	file = 'plots/plot'+str(people.__hash__())+'.png'
	try:
		with open(static_path+'/img/'+file, 'wb') as i:
			i.write(r.content)
	except:
		return ''
	return file

@lru_cache(maxsize=32)
def points_line_chart(data,static_path):
	x = []
	y = []
	for point in data:
		x.append(point['date'])
		y.append(point['points'])

	color = 'rgb(25, 118, 210)'
	payload = {
		"figure": { 
			"data": [
				{
				'x': x, 
				'y': y, 
				'marker': {'color': 'rgb(250, 155, 80)'}, 
				'type': 'bar'
				}
			],
        	"layout": {
				"width": 1000,
				"height": 500,
			    "format": "png",
			    "encoded": 'true'
			}
		},
		"width": 1000,
		"height": 500,
	    "scale": 2
	}

	r = requests.post('https://api.plot.ly/v2/images', auth=auth, headers=headers, json=payload)

	file = 'plots/plot'+str(data.__hash__())+'.png'
	try:
		with open(static_path+'/img/'+file, 'wb') as i:
			i.write(r.content)
	except Exception as e:
		return ''

	return file

class HList(list):
	def __hash__(self):
		hstr = ''
		try:
			for el in self:
				hstr += el['name']
		except: pass
		try:
			for el in self:
				hstr += el['date']
		except: pass
		return hash(hstr)

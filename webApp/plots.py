import json
import requests
from requests.auth import HTTPBasicAuth
from PIL import Image
from io import BytesIO
 
auth = HTTPBasicAuth('Marco-Z', '0kN05xPfvSSlgS2vW2cI')
headers = {'Plotly-Client-Platform': 'python'}

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

	file = 'plot1.png'
	try:
		i = Image.open(BytesIO(r.content))
		i.save(static_path+'\\img\\'+file, 'png')
	except:
		return ''
	return file




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
				'marker': {'color': 'rgb(250, 155, 80)'}
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

	file = 'plot2.png'
	try:
		i = Image.open(BytesIO(r.content))
		i.save(static_path+'\\img\\'+file, 'png')
	except:
		return ''

	return file

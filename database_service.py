from flask import Flask, render_template
from flask import request
import psycopg2

import requests

app = Flask(__name__)

@app.route('/')
def index():
	return '<h1>Home Page</h1>'

@app.route('/get_data_count/<label_name>/', defaults={'count':'0'})
@app.route('/get_data_count/<label_name>/<count>')
def get_data_count(label_name, count=0):
	try:
		types_dicts = {}
	
		conn = psycopg2.connect(user='postgres', password='123pass', host='ip-172-31-33-3', port='5432', database='postgres')
		cursor = conn.cursor()
	
		cursor.execute("SELECT * FROM label_types")
		rows = cursor.fetchall()

		for r in rows:
			types_dicts[r[1]] = r[0]

		if label_name in types_dicts.keys():
			label_no = types_dicts[label_name]
		else:
			raise InvalidError

		cursor.execute("SELECT * FROM data_input INNER JOIN data_labeling ON data_input.inpt_id=data_labeling.id_text ORDER BY data_input.inpt_id")

		result = cursor.fetchall()
		if count == '0':
			count = len(result)
		count_r = 0
		for r in range(int(count)):
			if result[r][4] == int(label_no):
				count_r+=1
		cursor.close()
		conn.close()
		return str(count_r)
	except:
		return render_template('error.html')

@app.route('/get_data/<count>/<sort_order>')
def get_data(count,sort_order):
	try:
		if count == None or sort_order == None:
			raise InvalidError

		conn = psycopg2.connect(user='postgres', password='123pass', host='ip-172-31-33-3', port='5432', database='postgres')
                
		cursor = conn.cursor()
		
		if sort_order not in ['asc', 'desc']:
			raise InvalidError

		cursor.execute("SELECT * FROM data_input INNER JOIN data_labeling ON data_input.inpt_id=data_labeling.id_text ORDER BY data_input.inpt_id, data_input.input_date "+sort_order.upper())

		result = cursor.fetchall()
		textval = []
		sentval = []
		for r in range(int(count)):
			textval.append(result[r][1])
			sentval.append(int(result[r][4]))
		cursor.close()
		conn.close()
		return dict({'review':textval,'sentiment':sentval})
	except:
		return render_template('error.html')

@app.errorhandler(404)
def not_found(e):
	return render_template('error.html')

if __name__ == '__main__':
	app.run(debug=True, port=3000)

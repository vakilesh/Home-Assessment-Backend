from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import json
import psycopg2
import os

# from flask import jsonify
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Connect to your postgres DB
conn = psycopg2.connect(
     database = os.environ.get("database"),
     user = os.environ.get("user"),
     password = os.environ.get("password"),
     host = os.environ.get("host")
)
cur = conn.cursor()


@app.route('/update/<id>', methods = ['POST'])
def update(id):
    data = request.get_json()
    description = data.get('description', '')
    name = data.get('name', '')
    if not name or not description:
        return jsonify(data={}, st=400)
    if name:
        cur.execute("UPDATE assessment SET name=%s WHERE id=%s", (name, id))
    if description:
        cur.execute("UPDATE assessment SET description=%s WHERE id=%s", (description, id))
    conn.commit()
    return jsonify(message="success", st=200)

@app.route('/<name>', defaults={'page': 0, "order": ""})
@app.route('/<name>/<page>/<order>')
def get(name, page, order):
    orderby = " " + order
    cur.execute("SELECT * FROM assessment ORDER BY {}{} LIMIT 20 OFFSET {}".format(name, orderby, int(page) * 20))
    records = cur.fetchall()
    data = []
    for arr in records:
        data.append({
            "id": arr[0],
            "name": arr[1],
            "description": arr[2],
            "year": arr[3],
            "endyear": arr[4],
            "time": arr[5],
        })
    print(records)
    return jsonify(data=data, st=200)  
 


@app.route('/insert/data/add/all')
def insert():
    f = open('data.json',)
    data = json.load(f) 
    for val in data.get('Data', []):
        temp = val.get('Item', {})
        years = temp["ReleaseYear"].split('-')
        start_year = years[0]
        runtime = temp.get('RunTimeSec', 0)
        print('temp["RunTimeSec"]', runtime)
        end_year = years[1] if  1 < len(years) else 0
        cur.execute('INSERT INTO assessment (name, description, year, endyear, RunTimeSec) VALUES (%s, %s, %s, %s, %s)', (temp["Title"], temp["ShortSynopsis"], start_year, end_year, runtime))
        print('inserted')
        print('\n\n\n')
    conn.commit()
    return jsonify(message="success")

if __name__ == '__main__':
    app.debug = true
    app.run()


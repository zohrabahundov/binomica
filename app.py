#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
from flask_cors import CORS, cross_origin
import numpy as np

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

tasks = [
    {
        'user_id': 1,
        'name': 'Zohrab',
        'surname': 'Ahundov', 
        'birth_date': '1994-04-02',
        'sex':'m',
        'height':'175',
        'width':'82'
    },
    {
        'user_id': 2,
        'name': 'Evgeniy',
        'surname': 'Stepanov', 
        'birth_date': '1990-04-02',
        'sex':'m',
        'height':'170',
        'width':'80'
    }
]

@app.route('/todo/api/v1.0/all_users', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/todo/api/v1.0/user/<int:user_id>', methods=['GET'])
def get_task(task_id):
    task = list(filter(lambda t: t['user_id'] == user_id, tasks))
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/todo/api/v1.0/add_user', methods=['POST'])
def create_task():
    if not request.json or not 'name' in request.json:
        abort(400)
    task = {'user_id': tasks[-1]['user_id'] + 1,\
            'name': request.json['name'],\
            'surname': request.json['surname'],\
            'birth_date': request.json['birth_date'],\
            'sex':request.json['sex'],\
            'height': request.json['height'],\
            'width':request.json['width']
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

@app.route('/todo/api/v1.0/acquire/<int:mu>', methods=['GET','POST'])
def acquire_task(mu):
    pulse = np.random.normal(mu, 1, size=1)
    pressure_up = np.random.normal(120, 1, size=1)
    pressure_dn = np.random.normal(75, 1, size=1)
    return jsonify({
        'pulse': str(pulse.astype(dtype='int32')[0]),
        'pressure_dn': str(pressure_dn.astype(dtype='int32')[0]),
        'pressure_up': str(pressure_up.astype(dtype='int32')[0]),
    }), 201

@app.route('/todo/api/v1.0/result/<int:mu>', methods=['GET','POST'])
def result_task(mu):
    if mu <=50:
        pulse = np.random.normal(mu, 1, size=1000).mean()
        pressure_up = np.random.normal(120, 1, size=1000).mean()
        pressure_dn = np.random.normal(75, 1, size=1000).mean()
    elif mu>=90:
        pulse = np.random.normal(mu, 1, size=1000).mean()
        pressure_up = np.random.normal(120, 1, size=1000).mean()
        pressure_dn = np.random.normal(75, 1, size=1000).mean()
    else:
        pulse = np.random.normal(mu, 1, size=1000).mean()
        pressure_up = np.random.normal(120, 1, size=1000).mean()
        pressure_dn = np.random.normal(75, 1, size=1000).mean()
     
    return jsonify({
        'pulse': str(pulse.astype(dtype='int32')),
        'pressure_up': str(pressure_up.astype(dtype='int32')),
        'pressure_dn': str(pressure_dn.astype(dtype='int32')),
        'height': str(175),
        'width': str(85),
        'pulse_n': str(70),
        'pressure_up_n': str(120),
        'pressure_dn_n': str(75),
        'height_n': str(175),
        'width_n': str(75),
        'pulse_ot': str(round(1 - pulse.astype(dtype='int32') / 70, 2)),
        'pressure_ot': str(round(1 - np.array([pressure_up.astype(dtype='int32') / 120, pressure_dn.astype(dtype='int32') / 75]).mean() / 2, 2)),
        'height_ot': str(round(1 - (175 / 175), 2)),
        'width_ot': str(round(1 - (75 / 70), 2)),
    }), 201

if __name__ == '__main__':
    app.run(debug=True)
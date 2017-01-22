from flask import Flask, jsonify
import psycopg2
import json

conn = psycopg2.connect(database="net_infra", user="postgres", password="12345678", host="127.0.0.1", port="5432")


cur = conn.cursor()
cur.execute('''
SELECT
 *
FROM
 pg_catalog.pg_tables
WHERE
 schemaname != 'pg_catalog'
AND schemaname != 'information_schema';''')

def node_req_status(node_id):
    stm = '''
    SELECT *
      FROM rest.node
     WHERE id = {id};
    '''.format(id=node_id)
    cur.execute(stm)
    return cur.fetchone()

def all_req_status():
    stm = '''
    SELECT *
      FROM rest.node
     ;
    '''
    cur.execute(stm)
    return cur.fetchall()


def add_node_req(**d):
    stm = '''
    INSERT
      INTO rest.node(id,gisid,owner,type,material, speed,technology,installdate, declaredate,comment)
    VALUES (nextval('rest.request_pk_seq'),{gisid},'{owner}','{type}','{material}', {speed},'{technology}','{installdate}', current_date,'{comment}');
    '''.format(**d)
    # .format(gisid=d['gisid'], owner=d['owner'], type=d['type'], material=d['material'],
    #         speed=d['speed'], technology=d['technology'], installdate=d['installdate'],
    #         comment=d['comment'])
    cur.execute(stm)
    conn.commit()
    return

def log_call(**d):
    stm = '''
    INSERT
      INTO rest.log(id,user,action,time,ip,browser,comment)
    VALUES (nextval('rest.request_pk_seq'),{gisid},'{owner}','{type}','{material}', {speed},'{technology}','{installdate}', current_date,'{comment}');
    '''.format(**d)
    cur.execute(stm)
    conn.commit()
    return

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

from flask import abort


@app.route('/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'requests': all_req_status()})


@app.route('/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    # task = [task for task in tasks if task['id'] == task_id]
    # if len(task) == 0:
    #     abort(404)
    #node_req_status(task_id)

    return jsonify({'request': node_req_status(task_id)})

from flask import request


@app.route('/getstuff', methods=['get'])
def get_stuff():
    return jsonify({'browser': request.headers.get('User-Agent'), 'ip': request.remote_addr}), 201



@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():

    if not request.json or 'gisid' not in request.json:
        abort(402)
    try:
        add_node_req(**request.json)
    except (psycopg2.InternalError, psycopg2.IntegrityError, psycopg2.InterfaceError, psycopg2.ProgrammingError) as e:
        conn.rollback()
        return jsonify({"error": str(e)})

    return jsonify(request.json), 201

if __name__ == '__main__':
    app.run(debug=True)



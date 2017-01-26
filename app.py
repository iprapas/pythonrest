from flask import Flask, jsonify, request
import psycopg2
import json
from itsdangerous import Serializer, BadSignature
import atexit

conn = psycopg2.connect(database="network_infra", user="postgres", password="12345678", host="127.0.0.1", port="5432")
atexit.register(conn.close)
cur = conn.cursor()
serializer = Serializer('secret-key')

def node_req_status(node_id):
    stm = '''
    SELECT status
      FROM rest.node
     WHERE id = {id};
    '''.format(id=node_id)
    cur.execute(stm)
    return cur.fetchone()[0]

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
      INTO rest.node(id,gisid,owner,nodetype,material, speed,technology,installdate, declaredate,status,comment)
    VALUES (nextval('rest.request_pk_seq'),{gisid},'{owner}','{type}','{material}', {speed},'{technology}',
	   '{installdate}', current_date,'STAGED','{comment}') RETURNING id	;
    '''.format(**d)
    # .format(gisid=d['gisid'], owner=d['owner'], type=d['type'], material=d['material'],
    #         speed=d['speed'], technology=d['technology'], installdate=d['installdate'],
    #         comment=d['comment'])
    cur.execute(stm)
    conn.commit()
    return cur.fetchone()[0]

def update_node_status(id, new_status):
    stm = '''
    UPDATE rest.node
       SET status='{new_status}'
     WHERE id={id};
    '''.format(new_status=new_status, id=id)
    cur.execute(stm)
    conn.commit()
    return

def log_call(request):
    stm = '''
    INSERT
      INTO rest.log(id,userid,action,ip,browser,time,comment)
    VALUES (nextval('rest.request_pk_seq'),'{user}','{action}','{ip}','{browser}',current_date,'{comment}');
    '''.format(user='',action='',browser=request.headers.get('User-Agent'), ip=request.remote_addr,comment='')
    cur.execute(stm)
    conn.commit()
    return

def all_logs():
    stm = '''
    SELECT *
      FROM rest.log
     ;
    '''
    cur.execute(stm)
    return cur.fetchall()



app = Flask(__name__)


from flask import abort


@app.route('/api/v1.0/nodes', methods=['GET'])
def get_tasks():
    return jsonify({'Nodes': all_req_status()})


@app.route('/api/v1.0/logs', methods=['GET'])
def get_logs():
    return jsonify({'Logs': all_logs()})


@app.route('/api/v1.0/nodes/<string:key_id>/status', methods=['GET'])
def get_node_status(key_id):
    # task = [task for task in tasks if task['id'] == task_id]
    # if len(task) == 0:
    #     abort(404)
    log_call(request)
    try:
        task_id = setzarializer.loads(key_id)
    except BadSignature as e:
        return jsonify({'BadSignatureError':str(e)})

    return jsonify({'status': node_req_status(task_id)})

@app.route('/api/v1.0/nodes', methods=['POST'])
def create_node():
    log_call(request)
    if not request.json or 'gisid' not in request.json:
        abort(402)
    try:
        id = add_node_req(**request.json)
    except (psycopg2.InternalError, psycopg2.IntegrityError, psycopg2.InterfaceError, psycopg2.ProgrammingError) as e:
        conn.rollback()
        return jsonify({"error": str(e)})

    return jsonify({"key-id": serializer.dumps(id)}), 201


@app.route('/api/v1.0/nodes/<int:id>/status', methods=['PATCH'])
def set_node_status(id):
    log_call(request)
    if not request.json or 'status' not in request.json:
        abort(402)
    try:
	new_status = request.json.get('status')
        update_node_status(id, new_status)
    except (psycopg2.InternalError, psycopg2.IntegrityError, psycopg2.InterfaceError, psycopg2.ProgrammingError) as e:
        conn.rollback()
        return jsonify({"error": str(e)})
    return jsonify({'new_status':new_status}),201


if __name__ == '__main__':
    app.run(debug=True)



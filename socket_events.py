from flask_socketio import SocketIO, emit
from models import db, Task
from flask_jwt_extended import decode_token
from flask import request

socketio = SocketIO()

@socketio.on('connect')
def handle_connect():
    emit('message', {'data': 'Connected to the server'})

@socketio.on('create_task')
def handle_create_task(data):
    try:
        token = data.get('token')
        decoded_token = decode_token(token)
        user_id = decoded_token['sub']

        task = Task(
            title=data['title'],
            description=data.get('description'),
            done=data.get('done', False),
            user_id=user_id
        )
        db.session.add(task)
        db.session.commit()

        emit('task_created', {'task': task.id, 'title': task.title}, broadcast=True)
    except Exception as e:
        emit('error', {'message': str(e)})

@socketio.on('disconnect')
def handle_disconnect():
    emit('message', {'data': 'Disconnected from the server'})

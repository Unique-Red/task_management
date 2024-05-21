from flask import request, jsonify
from app import app, db, jwt, socketio
from models import User, Task
from schemas import TaskSchema, UserSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
user_schema = UserSchema()

# User Registration
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(user_schema.dump(new_user)), 201

# User Login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

# Create Task
@app.route('/api/tasks', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json()
    current_user_id = get_jwt_identity()

    # Ensure user_id is set correctly
    data['user_id'] = current_user_id

    # Validate the request data against the TaskSchema
    errors = task_schema.validate(data)
    if errors:
        return jsonify(errors), 422

    # Create the Task object
    task = Task(
        title=data['title'],
        description=data['description'],
        completed=data.get('completed', False),
        user_id=current_user_id  # Ensure user_id is set correctly
    )

    # Add the Task to the database
    db.session.add(task)
    db.session.commit()

    # Emit socket event for real-time updates
    socketio.emit('new_task', task_schema.dump(task))

    # Return the created task
    return jsonify(task_schema.dump(task)), 201


# Get Tasks
@app.route('/api/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    current_user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=current_user_id).all()
    return jsonify(tasks_schema.dump(tasks)), 200

# Update Task
@app.route('/api/tasks/<int:id>', methods=['PUT'])
@jwt_required()
def update_task(id):
    task = Task.query.get_or_404(id)
    current_user_id = get_jwt_identity()

    if task.user_id != current_user_id:
        return jsonify({'message': 'Permission denied'}), 403

    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)

    db.session.commit()
    return jsonify(task_schema.dump(task)), 200

# Delete Task
@app.route('/api/tasks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    task = Task.query.get_or_404(id)
    current_user_id = get_jwt_identity()

    if task.user_id != current_user_id:
        return jsonify({'message': 'Permission denied'}), 403

    db.session.delete(task)
    db.session.commit()
    return '', 204

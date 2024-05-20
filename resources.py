from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, Task
from schemas import UserSchema, TaskSchema
from marshmallow import ValidationError

user_schema = UserSchema()
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

class UserRegistration(Resource):
    def post(self):
        json_data = request.get_json()
        try:
            data = user_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 400

        if User.query.filter_by(username=data['username']).first():
            return {'message': 'User already exists'}, 400

        user = User(username=data['username'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return {'message': 'User created successfully'}, 201

class UserLogin(Resource):
    def post(self):
        json_data = request.get_json()
        try:
            data = user_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 400

        user = User.query.filter_by(username=data['username']).first()
        if not user or not user.check_password(data['password']):
            return {'message': 'Invalid credentials'}, 401

        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token}, 200

class TaskList(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        tasks = Task.query.filter_by(user_id=user_id).all()
        return tasks_schema.dump(tasks), 200

    @jwt_required()
    def post(self):
        json_data = request.get_json()
        try:
            data = task_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 400

        user_id = get_jwt_identity()
        task = Task(title=data['title'], description=data.get('description'), done=data.get('done', False), user_id=user_id)
        db.session.add(task)
        db.session.commit()
        return task_schema.dump(task), 201

class TaskDetail(Resource):
    @jwt_required()
    def get(self, task_id):
        user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            return {'message': 'Task not found'}, 404
        return task_schema.dump(task), 200

    @jwt_required()
    def put(self, task_id):
        json_data = request.get_json()
        try:
            data = task_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 400

        user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            return {'message': 'Task not found'}, 404

        task.title = data['title']
        task.description = data.get('description')
        task.done = data.get('done', task.done)
        db.session.commit()
        return task_schema.dump(task), 200

    @jwt_required()
    def delete(self, task_id):
        user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            return {'message': 'Task not found'}, 404

        db.session.delete(task)
        db.session.commit()
        return {'message': 'Task deleted successfully'}, 204

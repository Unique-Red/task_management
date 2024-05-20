from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from models import db
from resources import UserRegistration, UserLogin, TaskList, TaskDetail
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

api = Api(app)
jwt = JWTManager(app)

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(TaskList, '/tasks')
api.add_resource(TaskDetail, '/tasks/<int:task_id>')

if __name__ == '__main__':
    app.run(debug=True)

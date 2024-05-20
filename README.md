# Task Management System API

## Overview

This is a simple RESTful API for a task management system that allows users to register, log in, and manage their tasks. The system uses JWT for authentication and SQLite for data persistence. It also includes real-time data streaming using Flask-SocketIO.

## Features

- **User Authentication:** Implemented using JWT tokens.
- **CRUD Operations:** Endpoints for creating, reading, updating, and deleting tasks.
- **Data Persistence:** Uses SQLite database to store task data.
- **Input Validation:** Validates input data to ensure data integrity and security.
- **Real-Time Data Streaming:** Uses Socket.IO to stream task data in real-time.

## Requirements

- Python 3.7+
- Flask
- Flask-RESTful
- Flask-JWT-Extended
- Flask-SQLAlchemy
- Flask-SocketIO
- Marshmallow
- Werkzeug

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Unique-Red/task_management.git
cd task-management
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Set up environment variables for secret keys (optional but recommended)

```bash
export SECRET_KEY='your_secret_key'
export JWT_SECRET_KEY='your_jwt_secret_key'
export DATABASE_URL='sqlite:///tasks.db'  # Or your preferred database URL
```

5. Run the application:

```bash
python app.py
```

The API will be available at http://localhost:5000.

## API Endpoints
User Registration
- Endpoint: /register
- Method: POST
- Request Body:
```bash
{
  "username": "example_user",
  "password": "example_password"
}
```

- Response:
```bash
{
  "message": "User created successfully"
}
```
## User Login
- Endpoint: /login
- Method: POST
- Request Body:
```bash
{
  "access_token": "jwt_token"
}
```

## Get Tasks
- Endpoint: /tasks
- Method: GET
- Headers: Authorization: Bearer <jwt_token>
- Response:
```bash
[
  {
    "id": 1,
    "title": "Task 1",
    "description": "Description 1",
    "done": false,
    "user_id": 1
  }
]
```

## Create Task
- Endpoint: /tasks
- Method: POST
- Headers: Authorization: Bearer <jwt_token>
- Request Body:
```bash
{
  "title": "New Task",
  "description": "Task Description",
  "done": false
}
```

- Response
```bash
{
  "id": 1,
  "title": "New Task",
  "description": "Task Description",
  "done": false,
  "user_id": 1
}
```

## Get Task by ID
- Endpoint: /tasks/<int:task_id>
- Method: GET
- Headers: Authorization: Bearer <jwt_token>
- Response:
```bash
{
  "id": 1,
  "title": "Task 1",
  "description": "Description 1",
  "done": false,
  "user_id": 1
}
```
## Update Task by ID
- Endpoint: /tasks/<int:task_id>
- Method: PUT
- Headers: Authorization: Bearer <jwt_token>
- Request Body:
```bash
{
  "title": "Updated Task",
  "description": "Updated Description",
  "done": true
}
```
- Response:
```bash
{
  "id": 1,
  "title": "Updated Task",
  "description": "Updated Description",
  "done": true,
  "user_id": 1
}
```

## Delete Task by ID
- Endpoint: /tasks/<int:task_id>
- Method: DELETE
- Headers: Authorization: Bearer <jwt_token>
- Response:
```bash
{
  "message": "Task deleted successfully"
}
```


## Real-Time Data Streaming
To enable real-time data streaming, the API uses Flask-SocketIO. Clients can connect to the WebSocket and receive updates on task creation.

### Socket Events
Connect

- Event: connect
- Response:
```bash
{
  "data": "Connected to the server"
}
```

## Create Task

- Event: create_task
- Request:
```bash
{
  "token": "jwt_token_here",
  "title": "New Task via Socket",
  "description": "Task Description",
  "done": false
}
```
- Response:
```bash
{
  "task": 1,
  "title": "New Task via Socket"
}
```

## Disconnect

- Event: disconnect
- Response:
```bash
{
  "data": "Disconnected from the server"
}
```

## Testing the Socket Connection
Use a client library such as Socket.IO-client for Python or a web client to connect and test the socket events.

Example using a Python client:
```bash
import socketio

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to the server")

@sio.event
def message(data):
    print("Message from server:", data)

@sio.event
def task_created(data):
    print("Task created:", data)

@sio.event
def error(data):
    print("Error:", data)

sio.connect('http://localhost:5000')

# Example: Creating a task
sio.emit('create_task', {
    'token': 'jwt_token_here',
    'title': 'New Task via Socket',
    'description': 'Task Description',
    'done': False
})
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any bugs or feature requests.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
```bash
This `README.md` file provides an overview of the Task Management System API, installation instructions, details about the API endpoints, real-time data streaming, and a brief guide on how to test the socket connection.
```
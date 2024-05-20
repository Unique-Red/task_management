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


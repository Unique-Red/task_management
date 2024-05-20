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

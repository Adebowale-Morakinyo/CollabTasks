# CollabTasks
CollabTasks is a collaborative task management platform built with Flask, designed to streamline task organization and improve team collaboration. 🚀

## Features

- User registration and authentication using JWT
- CRUD operations for tasks
- Real-time task collaboration with Flask-SocketIO
- Custom task prioritization algorithm for efficient scheduling

## Tech Stack

- Flask
- Flask-Smorest
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Flask-SocketIO

## Getting Started

1. Clone the repository: `git clone https://github.com/yourusername/CollabTasks.git`
2. Create a virtual environment: `python -m venv venv`
3. Activate virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up environment variables (see below).
6. Run the application: `python app.py`

## Environment Variables

- `SECRET_KEY`: Your secret key for Flask-JWT-Extended
- `DATABASE_URL`: URL for your chosen database (e.g., SQLite, PostgreSQL)

## Project Structure

```
CollabTasks/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── tasks.py
│   └── socketio/
│       ├── __init__.py
│       └── events.py
├── venv/
├── .gitignore
├── app.py
└── requirements.txt
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://github.com/Adebowale-Morakinyo/CollabTasks/blob/main/LICENSE)

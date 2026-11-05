# DevPulse

**An Async Incident Post-Mortem & Discussion Engine for Engineering Teams**

DevPulse is a backend application designed to help engineering teams document technical incidents, discuss their causes, and share solutions through structured posts and threaded comments.

It provides an API for managing users, posts, and nested discussions, with authentication and authorization to protect user operations.

## Features

### Authentication & User Management
- User registration and login.
- Password hashing.
- JWT-based authentication.
- Protected user operations.
- User authorization and ownership checks.

### Post Management
- Create, retrieve, update, and delete posts.
- Retrieve posts from the platform.
- Restrict post modifications to their owners.
- Input validation for post titles and content.

### Nested Comment System
- Create comments on posts.
- Reply to existing comments.
- Retrieve comments in a hierarchical structure.
- Update and delete comments with ownership checks.
- Soft deletion to preserve discussion threads.
- Prevent editing or replying directly to deleted comments.
- Validate comment content and parent-comment relationships.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API development |
| PostgreSQL | Relational database |
| SQLAlchemy | ORM and database operations |
| Pydantic | Data validation and schemas |
| Alembic | Database migrations |
| JWT | Authentication |
| Postman | API testing and documentation |
| Git & GitHub | Version control |

## Project Structure

```text
DevPulse/
│
├── docs/
│   └── postman/
│       └── DevPulse APIs.postman_collection.json
│
├── migrations/
│   └── versions/
│
├── app/
│   ├── controllers/
│   ├── models/
│   ├── routers/
│   └── schemas/
│
├── alembic.ini
├── requirements.txt
├── README.md
└── .gitignore
```

*Note: Adjust the project structure above to match your actual folders and filenames.*

## Getting Started

### Prerequisites

- Python 3.10 or later (use the version compatible with your project).
- PostgreSQL.
- Git.

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd DevPulse
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows:**
```bash
venv\Scripts\activate
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and configure the database connection and authentication settings required by the application.

Do not commit your `.env` file or expose database credentials and JWT secrets.

### 5. Apply database migrations

```bash
alembic upgrade head
```

### 6. Run the application

```bash
uvicorn main:app --reload
```

*Adjust `main:app` if your FastAPI application entry point is located elsewhere.*

The API should now be accessible at:

```text
http://127.0.0.1:8000
```

FastAPI interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## API Documentation

The Postman collection contains requests for authentication, user management, posts, and comments.

**Published Postman Documentation:**  
[View DevPulse API Documentation](YOUR_PUBLISHED_POSTMAN_DOCUMENTATION_URL)

The exported Postman collection is also available in:

```text
docs/postman/
```

## Current Development Status

- [x] Authentication and user management
- [x] Posts CRUD operations
- [x] Nested comments and replies
- [x] Comment soft deletion
- [x] Input validation and authorization checks
- [x] Database migrations
- [x] Manual API testing with Postman
- [x] Postman API documentation
- [ ] Automated testing with pytest
- [ ] Docker configuration
- [ ] Application deployment

## Future Improvements

- Automated test coverage.
- Docker-based application setup.
- Continuous integration.
- Production deployment.

## Author

**Prasheek Prakash Wankhede**

- GitHub: [@prasheekw](https://github.com/prasheekw)
- LinkedIn: [Prasheek Wankhede](https://www.linkedin.com/in/prasheek-wankhede-121240329/)

---

*DevPulse is an independent backend engineering project built to explore REST API development, authentication, relational database design, and threaded discussions using Python and FastAPI.*

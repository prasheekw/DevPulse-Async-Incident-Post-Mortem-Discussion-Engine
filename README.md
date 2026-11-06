# DevPulse

**An Async Incident Post-Mortem & Discussion Engine for Engineering Teams**

DevPulse is a backend application designed to help engineering teams document technical incidents, discuss their causes, and share solutions through structured posts and threaded comments.

It provides REST APIs for user management, incident posts, and nested discussions, with JWT-based authentication and authorization to protect user operations.

**Live API:** https://devpulse-async-incident-post-mortem.onrender.com

**Interactive API Documentation:** [Swagger UI](https://devpulse-async-incident-post-mortem.onrender.com/docs)

---

## Features

### Authentication & User Management
- User registration and login.
- Password hashing using `pwdlib`.
- JWT-based authentication.
- Protected endpoints using bearer-token authentication.
- Authorization and ownership checks for user operations.

### Post Management
- Create, retrieve, update, and delete posts.
- Retrieve posts across the platform.
- Restrict post modifications to their owners.
- Input validation for post titles and content.

### Nested Comment System
- Create comments on posts.
- Reply to existing comments.
- Retrieve comments in a hierarchical structure.
- Update and delete comments with ownership checks.
- Soft deletion to preserve discussion threads and replies.
- Prevent editing or replying directly to deleted comments.
- Validate comment content and parent-comment relationships.

### Database & Testing
- Relational database design using PostgreSQL.
- SQLAlchemy ORM for database operations.
- Alembic for version-controlled database migrations.
- Automated tests using pytest.
- API testing and documentation using Postman.

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API development |
| PostgreSQL | Relational database |
| SQLAlchemy | ORM and database operations |
| Pydantic | Data validation and schemas |
| Alembic | Database migrations |
| PyJWT | JWT authentication |
| pwdlib | Password hashing |
| pytest | Automated testing |
| Postman | API testing and documentation |
| Neon | Hosted PostgreSQL database |
| Render | Application deployment |
| Git & GitHub | Version control |

---

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
├── src/
│   ├── comments/
│   ├── posts/
│   ├── user/
│   └── utils/
│       ├── config.py
│       ├── database.py
│       └── helper.py
│
├── tests/
│
├── app.py
├── alembic.ini
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Database Design

DevPulse uses PostgreSQL to manage users, posts, and threaded comments.

The main relationships are:

- **Users → Posts:** One user can create multiple posts.
- **Users → Comments:** One user can create multiple comments.
- **Posts → Comments:** One post can contain multiple comments.
- **Comments → Replies:** A comment can have multiple child comments through a self-referencing relationship.

Comments support nested replies through a nullable `parent_comment_id` foreign key.

Soft deletion allows deleted comments to remain in the discussion structure, preserving their replies.

---

## Getting Started

### Prerequisites

- Python 3.10 or later.
- PostgreSQL.
- Git.

### 1. Clone the repository

```bash
git clone https://github.com/prasheekw/DevPulse-Async-Incident-Post-Mortem-Discussion-Engine.git

cd DevPulse-Async-Incident-Post-Mortem-Discussion-Engine
```

### 2. Create a virtual environment

```bash
python -m venv env
```

Activate it:

**Windows:**

```bash
env\Scripts\activate
```

**Linux / macOS:**

```bash
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

Configure the following variables:

```env
DATABASE_URL=your_local_postgresql_connection_string
DATABASE_URL_UNPOOLED=your_database_direct_connection_string

SECRET_KEY=your_jwt_secret_key
ALGORITHM=HS256
EXP_TIME=your_token_expiry_in_minutes
```

`DATABASE_URL_UNPOOLED` can be used for direct database connections during migrations. For local development, configure both URLs according to your PostgreSQL setup.

Never commit your `.env` file or expose database credentials and JWT secrets.

### 5. Apply database migrations

```bash
alembic upgrade head
```

This creates or updates the database schema using the migration history.

### 6. Run the application

```bash
uvicorn app:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

FastAPI interactive documentation:

```text
http://127.0.0.1:8000/docs
```

---

## API Documentation

DevPulse provides interactive API documentation through FastAPI's Swagger UI.

**Live Swagger Documentation:**

https://devpulse-async-incident-post-mortem.onrender.com/docs

The Postman collection includes requests for authentication, user management, posts, and comments.

**Published Postman Documentation:**  
[View DevPulse Postman API Documentation](https://documenter.getpostman.com/view/57676402/2sBYHXRdpa)

The exported Postman collection is available in:

```text
docs/postman/
```

---

## Testing

DevPulse includes automated tests written using pytest.

The current test suite contains 8 tests covering:

- Application startup.
- User registration.
- Duplicate registration.
- Successful login.
- Invalid login credentials.
- Authentication without a token.
- Authentication with a valid token.
- Authentication with an invalid token.

Run the test suite using:

```bash
pytest
```

---

## Deployment

DevPulse is deployed using **Render**, with **Neon PostgreSQL** as its hosted database.

The deployment process uses environment variables for production configuration and runs Alembic migrations before starting the FastAPI application.

The application is accessible at:

https://devpulse-async-incident-post-mortem.onrender.com

---

## Future Improvements

- Expand automated test coverage across posts and comment operations.
- Improve resource-scoped comment endpoint design.
- Add Docker support.
- Implement CI/CD automation.
- Improve production monitoring and error handling.

---

## Author

**Prasheek Prakash Wankhede**

- GitHub: [@prasheekw](https://github.com/prasheekw)
- LinkedIn: [Prasheek Wankhede](https://www.linkedin.com/in/prasheek-wankhede-121240329)

---

*DevPulse is an independent backend engineering project built to explore REST API development, authentication, relational database design, database migrations, and threaded discussions using Python and FastAPI.*
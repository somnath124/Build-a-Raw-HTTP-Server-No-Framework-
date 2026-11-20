# Build-a-Raw-HTTP-Server-No-Framework-
# Raw HTTP Notes API — Python

A simple RESTful Notes API developed using Python's built-in `http.server` module without external frameworks.

This project demonstrates fundamental HTTP concepts, REST API development, JSON request and response handling, and server-side request processing.

### Features
- Create new notes using POST requests.
- Retrieve all notes or a specific note by ID using GET requests.
- Delete notes using DELETE requests.
- Handle JSON data and HTTP status codes (200, 201, 204, 400, 404, 405).
- Log HTTP requests with method, path, status code, and processing time.
- Test API endpoints using Postman.

### Technologies Used
- Python
- HTTPServer and BaseHTTPRequestHandler
- JSON
- Postman

### API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/notes` | Retrieve all notes |
| GET | `/notes/{id}` | Retrieve a specific note |
| POST | `/notes` | Create a new note |
| DELETE | `/notes/{id}` | Delete a note |

### How to Run

1. Clone or download the repository.
2. Open a terminal in the project folder.
3. Run `python server.py`.
4. Access the API at `http://localhost:8080/notes`.
5. Use Postman or curl to test the endpoints.

### Note
The application stores notes in memory, so data is cleared whenever the server restarts.

### Learning Outcomes
This project helped me understand how HTTP servers work internally, how requests and responses are processed, and how to build basic REST-style APIs without relying on frameworks such as Flask or Django.

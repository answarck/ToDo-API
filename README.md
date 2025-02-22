# ToDo API

A simple Flask-based REST API for managing a ToDo list.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/answarck/ToDo-API
   cd ToDo-API
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Run Application

### For Testing
```bash
flask --app main run
```

### For Production
```bash
gunicorn main:app
```

5. Access the **Swagger UI** at [`/`](http://127.0.0.1:5000/) for interactive API documentation and testing.

## Endpoints

### Create a ToDo
**POST** `/create`
- **Request Body (JSON):**
  ```json
  { "todo": "Buy groceries" }
  ```
- **Response (201 Created):**
  ```json
  { "id": 1, "todo": "Buy groceries" }
  ```
- **cURL Example:**
  ```bash
  curl -X POST "http://127.0.0.1:5000/create" -H "Content-Type: application/json" -d '{"todo": "Buy groceries"}'
  ```

### Delete a ToDo
**DELETE** `/delete/<int:id>`
- **Response (200 OK):**
  ```json
  { "message": "Todo deleted successfully" }
  ```
- **Response (404 Not Found):**
  ```json
  { "error": "Todo not found" }
  ```
- **cURL Example:**
  ```bash
  curl -X DELETE "http://127.0.0.1:5000/delete/1"
  ```

### Update a ToDo
**PUT** `/update/<int:id>`
- **Request Body (JSON):**
  ```json
  { "todo": "Buy vegetables" }
  ```
- **Response (200 OK):**
  ```json
  { "id": 1, "todo": "Buy vegetables" }
  ```
- **cURL Example:**
  ```bash
  curl -X PUT "http://127.0.0.1:5000/update/1" -H "Content-Type: application/json" -d '{"todo": "Buy vegetables"}'
  ```

### List ToDos
**GET** `/list/all`
- **Response (200 OK):**
  ```json
  { "todos": [ { "id": 1, "todo": "Buy groceries" } ] }
  ```
- **cURL Example:**
  ```bash
  curl -X GET "http://127.0.0.1:5000/list/all"
  ```

**GET** `/list/<int:id>`
- **Response (200 OK):**
  ```json
  { "id": 1, "todo": "Buy groceries" }
  ```
- **Response (404 Not Found):**
  ```json
  { "error": "Todo not found" }
  ```
- **cURL Example:**
  ```bash
  curl -X GET "http://127.0.0.1:5000/list/1"
  ```

## Database
- Uses SQLite (`todo.db`).
- Table: `ToDo`
  - `id` (INTEGER, Primary Key)
  - `todo` (STRING, Max 255 chars)

## Notes
- The API expects and returns JSON.
- Validation ensures `todo` is non-empty and under 255 characters.
- **Swagger UI** provides an interactive way to explore and test the API at [`/`](http://127.0.0.1:5000/).
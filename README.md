# Todo API (Postman only)

A tiny beginner-friendly FastAPI project meant to be tested using Postman (no frontend).

## Requirements
- Python 3.10+ (recommended: 3.11)
- Postman

## Setup
```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

### Run API
```bash
uvicorn app.main:app --reload
```

#### Base URL:
- `http://127.0.0.1:8000`

#### Healthcheck:
- `GET /health` → 200 OK


## Endpoints (Todo CRUD)
## 1) Create todo
<b>POST</b> `/todos`

Body (JSON):
```JSON
{
  "title": "Learn FastAPI",
  "description": "Build a tiny CRUD API tested with Postman"
}
```
Expected:
- <b>201 Created</b>
- <b>Response example:</b>
```JSON
{
  "id": 1,
  "title": "Learn FastAPI",
  "description": "Build a tiny CRUD API tested with Postman",
  "done": false,
  "created_at_utc": "2026-03-03T12:34:56.123456+00:00"
}
```

## 2) List todos
<b>GET</b> `/todos`

Expected:
- 200 OK
- Response: list of todos

Optional filter:
- `GET /todos?done=true`
- `GET /todos?done=false`

## 3) Get single todo
<b>GET</b> `/todos/{id}`

Example:
- `GET /todos/1`

Expected:
- <b>200 OK</b> if found
- <b>404 Not Found</b> if missing

## 4) Full update (replace)
<b>PUT</b> `/todos/{id}`

Example:
- `PUT /todos/1`

Body (JSON):
```JSON
{
  "title": "Learn FastAPI (updated)",
  "description": "Now with PUT",
  "done": true
}
```

Expected:
- <b>200 OK</b>
- Returns updated todo

## 5) Partial update
<b>PATCH</b> `/todos/{id}`

Example:
- `PATCH /todos/1`

Body (JSON) examples:

Mark as done:
```JSON
{ "done": true }
```

Update title only:
```JSON
{ "title": "New title" }
```

Expected:
- <b>200 OK</b>
- Returns updated todo

## 6) Delete todo
<b>DELETE</b> `/todos/1`

Example:
- `DELETE /todos/1`

Expected:
- <b>204 No Content</b>
- Empty response body


## Notes / Limitations
- Data is stored in-memory only (it resets when you restart the server).
- This project is intentionally minimal for learning + Postman testing.
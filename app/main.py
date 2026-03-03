from datetime import datetime, timezone
from fastapi import FastAPI

from app.todos import router as todos_router

app = FastAPI(title='Todo API (Postman only)', version='0.2.0')

app.include_router(todos_router, prefix='/todos', tags=['todos'])


@app.get('/')
def root():
    return {
        'name': 'Todo API (Postman only)',
        'hint': 'Try GET /health and /todos',
    }
    
    
@app.get('/health')
def health():
    return {
        'status': 'ok',
        'time_utc': datetime.now(timezone.utc).isoformat(),
    }
    
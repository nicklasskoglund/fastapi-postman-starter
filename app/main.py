from datetime import datetime, timezone
from fastapi import FastAPI

app = FastAPI(title='Todo API (Postman only)', version='0.1.0')


@app.get('/')
def root():
    return {
        'name': 'Todo API (Postman only)',
        'hint': 'Try GET /health',
    }
    
    
@app.get('/health')
def health():
    return {
        'status': 'ok',
        'time_utc': datetime.now(timezone.utc).isoformat(),
    }
    
from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException, Response, status
from pydantic import BaseModel, Field

router = APIRouter()

# --- Pydantic-modeller (request/response) ---


class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    
    
class TodoUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    done: bool
    
    
class TodoPatch(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    done: Optional[bool] = None
    
    
class Todo(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    done: bool
    created_at_utc: str
    
    
# --- In-memory "database" ---
_TODOS: Dict[int, Todo] = {}
_NEXT_ID: int = 1


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _get_or_404(todo_id: int) -> Todo:
    todo = _TODOS.get(todo_id)
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Todo with id={todo_id} not found',
        )
    return todo


@router.post('', response_model=Todo, status_code=status.HTTP_201_CREATED)
def creat_todo(payload: TodoCreate) -> Todo:
    global _NEXT_ID
    
    todo = Todo(
        id=_NEXT_ID,
        title=payload.title,
        description=payload.description,
        done=False,
        created_at_utc=_utc_now_iso(),
    )
    _TODOS[_NEXT_ID] = todo
    _NEXT_ID += 1
    return todo


@router.get('', response_model=List[Todo])
def list_todos(done: Optional[bool] = None) -> List[Todo]:
    todos = list(_TODOS.values())
    if done is None:
        return todos
    return [t for t in todos if t.done is done]


@router.get('/{todo_id}', response_model=Todo)
def get_todo(todo_id: int) -> Todo:
    return _get_or_404(todo_id)


@router.put('/{todo_id}', response_model=Todo)
def update_todo(todo_id: int, payload: TodoUpdate) -> Todo:
    _get_or_404(todo_id)    # validate that it exists
    
    updated = Todo(
        id=todo_id,
        title=payload.title,
        description=payload.description,
        done=payload.done,
        created_at_utc=_TODOS[todo_id].created_at_utc,  # keep created_at
    )
    _TODOS[todo_id] = updated
    return updated


@router.patch('/{todo_id}', response_model=Todo)
def patch_todo(todo_id: int, payload: TodoPatch) -> Todo:
    todo = _get_or_404(todo_id)
    
    new_title = payload.title if payload.title is not None else todo.title
    new_desc = payload.description if payload.description is not None else todo.description
    new_done = payload.done if payload.done is not None else todo.done
    
    patched = Todo(
        id=todo.id,
        title=new_title,
        description=new_desc,
        done=new_done,
        created_at_utc=todo.created_at_utc,
    )
    _TODOS[todo_id] = patched
    return patched


@router.delete('/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int) -> Response:
    _get_or_404(todo_id)
    del _TODOS[todo_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select,func


from app.core.db import get_db
from app import models
from app.routes import schemas

# /api/v1/todo
router = APIRouter()


@router.post("", summary="Create a new todo")
async def create_todo(
    db: Annotated[AsyncSession, Depends(get_db)],
    reqeust_data: schemas.CreateTodoRequest,
) -> schemas.CreateTodoResponse:
    todo = models.Todo(content=reqeust_data.content)
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return schemas.CreateTodoResponse(
        id=todo.id,
        content=todo.content,
        created_at=todo.created_at,
        updated_at=todo.updated_at,
    )

@router.get("/{todo_id}", summary="Retrieve a todo")
async def retrieve_todo(
    db: Annotated[AsyncSession, Depends(get_db)],
    todo_id: int,
) -> schemas.RetrieveTodoResponse:
    stmt = select(
        models.Todo.id,
        models.Todo.content,
        models.Todo.created_at,
        models.Todo.updated_at,
    ).where(
        models.Todo.id == todo_id,
        models.Todo.deleted_at.is_(None),
    )
    result_row = (await db.execute(stmt)).first()

    if result_row is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    mapped_row = result_row._mapping
    return schemas.RetrieveTodoResponse(
        id=mapped_row[models.Todo.id],
        content=mapped_row[models.Todo.content],
        created_at=mapped_row[models.Todo.created_at],
        updated_at=mapped_row[models.Todo.updated_at],
    )

@router.get("", summary="List all todos")
async def list_todos(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> schemas.ListTodosResponse:
    count_stmt = select(func.count(models.Todo.id)).where(
        models.Todo.deleted_at.is_(None),
    )
    count_result = (await db.execute(count_stmt)).scalar() or 0

    stmt = (
        select(
            models.Todo.id,
            models.Todo.content,
            models.Todo.created_at,
            models.Todo.updated_at,
        )
        .where(
            models.Todo.deleted_at.is_(None),
        )
        .order_by(models.Todo.created_at.desc())
    )
    result_rows = (await db.execute(stmt)).all()

    return schemas.ListTodosResponse(
        count=count_result,
        items=[
            schemas.ListTodosResponseItem(
                id=row.id,
                content=row.content,
                created_at=row.created_at,
                updated_at=row.updated_at,
            )
            for row in result_rows
        ],
    )
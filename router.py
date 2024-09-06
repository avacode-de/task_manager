#user post
from typing import Annotated

from fastapi import Depends, APIRouter

from repository import TaskRepository
from schemas import STask, STaskAdd, STaskId

router = APIRouter(
    prefix="/tasks",
    tags=["Таски"],
)

@router.post("")
async def add_task(
        task: Annotated[STaskAdd, Depends()],
) -> STaskId:
    task_id = await TaskRepository.add_one(task)
    return {"ok": True, "task_id": task_id}

@router.get("")
async def get_tasks() -> list[STask]:
    #  async request to repository,
    #  which helps get task while 
    #  many users are waiting for request
     tasks = await TaskRepository.find_all()
     return tasks
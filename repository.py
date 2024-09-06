from sqlalchemy import select
from database import TasksOrm, new_session
from schemas import STask, STaskAdd


class TaskRepository:
    @classmethod
    async def add_one(cls, data: STaskAdd) -> int:
        async with new_session() as session:
            task_dict = data.model_dump()

            task = TasksOrm(**task_dict)
            session.add(task)
            await session.flush() #send changing to database and returns id
            await session.commit()
            return task.id

    @classmethod
    async def find_all(cls) -> list[STask]:
        async with new_session() as session:
            query = select(TasksOrm) #getting request from sql (using sqlalchemy)
            result = await session.execute(query)
            task_modules = result.scalars().all()
            task_schemas = [STask.model_validate(task_module) for task_module in task_modules] #validating task schemas as pydantic
            return task_modules
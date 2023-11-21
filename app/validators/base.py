from fastapi import HTTPException


async def check_fields(item) -> None:
    if not any(item.dict().values()):
        raise HTTPException(
            status_code=422,
            detail="Поля запроса заполнены некорректно!",
        )

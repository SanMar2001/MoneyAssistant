from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db
from backend.exceptions.user import EmailAlreadyExistsError
from backend.schemas.common import ApiResponse
from backend.schemas.user import UserCreate, UserResponse
from backend.services.user_service import create_user, delete_user, get_users

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/",
    response_model=ApiResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_user_endpoint(
    user_data: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        user = await create_user(db, user_data)

        return {
            "status": status.HTTP_201_CREATED,
            "body": user,
        }

    except EmailAlreadyExistsError:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "status": status.HTTP_409_CONFLICT,
                "body": {
                    "message": "A user with this email already exists",
                },
            },
        )


@router.get("/", response_model=ApiResponse[list[UserResponse]])
async def get_users_endpoint(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    users = await get_users(db)
    return {
        "status": status.HTTP_200_OK,
        "body": users,
    }


@router.delete("/{user_id}", response_model=ApiResponse[UserResponse | None])
async def delete_user_endpoint(
    user_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    user = await delete_user(db, user_id)
    if user is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "status": status.HTTP_404_NOT_FOUND,
                "body": {
                    "message": "User not found",
                },
            },
        )
    return {
        "status": status.HTTP_200_OK,
        "body": user,
    }

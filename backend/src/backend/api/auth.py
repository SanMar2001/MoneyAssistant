from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db
from backend.core.security import create_access_token
from backend.schemas.user import UserLogin
from backend.services.user_service import authenticate_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(
    credentials: UserLogin,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    user = await authenticate_user(
        db,
        credentials.email,
        credentials.password,
    )

    if user is None:
        return {
            "status": status.HTTP_401_UNAUTHORIZED,
            "body": {
                "message": "Invalid email or password",
            },
        }

    access_token = create_access_token(
        {"sub": str(user.id), "email": user.email, "role": user.role}
    )

    return {
        "status": status.HTTP_200_OK,
        "body": {
            "message": "Login successful",
            "access_token": access_token,
            "token_type": "bearer",
        },
    }

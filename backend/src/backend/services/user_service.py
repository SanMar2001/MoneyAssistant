from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.security import hash_password, verify_password
from backend.exceptions.user import EmailAlreadyExistsError
from backend.models.user import User
from backend.schemas.user import UserCreate


async def create_user(
    db: AsyncSession,
    user_data: UserCreate,
) -> User:
    result = await db.execute(select(User).where(User.email == user_data.email))

    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise EmailAlreadyExistsError

    user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        full_name=user_data.full_name,
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def get_users(db: AsyncSession) -> list[User]:
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users


async def delete_user(db: AsyncSession, user_id: str) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        return None

    await db.delete(user)
    await db.commit()
    return user


async def authenticate_user(
    db: AsyncSession,
    email: str,
    password: str,
) -> User | None:
    result = await db.execute(select(User).where(User.email == email))

    user = result.scalar_one_or_none()

    if user is None:
        return None

    if not user.active:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user

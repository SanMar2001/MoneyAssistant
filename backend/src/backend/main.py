from fastapi import FastAPI

from backend.api.auth import router as auth_router
from backend.api.users import router as users_router

app = FastAPI(title="MoneyAssistant")


app.include_router(users_router)
app.include_router(auth_router)


@app.get("/health")
async def health():
    return {"status": "ok"}

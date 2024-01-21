from fastapi import FastAPI

from src.routers.contacts_items import router as contacts_router
from src.routers.auth import router as auth


app = FastAPI()
app.include_router(contacts_router, prefix="/contacts")
app.include_router(auth, prefix="/contacts")


@app.get("/healthchecker")
async def healthchecker():
    return {"message": "Hello World!"}

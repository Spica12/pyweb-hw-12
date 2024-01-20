from fastapi import FastAPI

from routers.contacts_items import router as contacts_router


app = FastAPI()
app.include_router(contacts_router, prefix='/contacts')


@app.get("/healthchecker")
async def healthchecker():
    return {"message": "Hello World!"}

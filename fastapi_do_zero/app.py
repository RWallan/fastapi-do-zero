from fastapi import FastAPI

from fastapi_do_zero.routes import auth_router, task_router, user_router

app = FastAPI()


@app.get("/")
async def health_check():
    return {"message": "OK"}


app.include_router(user_router)
app.include_router(auth_router)
app.include_router(task_router)

from fastapi import FastAPI

from fastapi_do_zero.routes import user_router

app = FastAPI()


@app.get("/")
def health_check():
    return {"message": "OK"}


app.include_router(user_router)

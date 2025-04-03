from fastapi import FastAPI
from handlers import routers
import uvicorn

app = FastAPI()

for router in routers:
    app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, log_level="debug", reload=True)
import uvicorn
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from routers import smoke
from config import DEVICE, logger

templates = Jinja2Templates(directory="templates")
app = FastAPI()

app.include_router(smoke.router, prefix="/smoke", tags=["Smoke"])

@app.on_event("startup")
async def startup():
    logger.info("Starting...")
    logger.info("Machine Learning models will run on device: {}".format(DEVICE))


@app.on_event("shutdown")
async def shutdown():
    logger.info("Shutting down...")

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
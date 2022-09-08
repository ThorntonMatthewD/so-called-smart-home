"""
 The main application. Everything plugs up here.
"""
from starlette.responses import FileResponse

from src.config import app


@app.get("/")
async def root():
    """The root route that is basically just used for testing"""
    return {"detail": "Welcome to the Sensor Gateway!"}


@app.get("/favicon.ico")
async def favicon():
    """The favicon"""
    return FileResponse("favicon.ico")

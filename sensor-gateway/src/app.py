"""
 The main application. Everything meets up here.
"""
from starlette.responses import FileResponse
from starlette_prometheus import metrics, PrometheusMiddleware

from src.config import app
from src.routers import metrics_receiver

# Add Middleware
app.add_middleware(PrometheusMiddleware)


# Add Routers
app.include_router(metrics_receiver.router)


# Add Routes
app.add_route("/metrics", metrics)


@app.get("/")
async def root():
    """The root route that is basically just used for testing"""
    return {"detail": "Welcome to the Sensor Gateway!"}


@app.get("/favicon.ico")
async def favicon():
    """The favicon"""
    return FileResponse("favicon.ico")

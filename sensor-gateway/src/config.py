"""
 The configuration for this FastAPI application
"""
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

log = logging.getLogger(__name__)
app = FastAPI(
    title="Sensor Gateway",
    description="A place for sensors to send data for Prometheus to scrape"
)

origins = [
    "http://localhost:9500",
    "http://localhost:9500/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

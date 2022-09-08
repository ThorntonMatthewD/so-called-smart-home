"""Exposes metrics to Prometheus"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from prometheus_client import (
    CollectorRegistry,
    Gauge,
    Histogram,
    Summary,
    Info,
    Enum
)

router = APIRouter()
registry = CollectorRegistry()

metrics_cache = {}


class Metrics(BaseModel):
    """Model for incoming metrics"""
    metric_name: str
    description: str
    type: str
    data: dict


@router.post("/receive_metrics", tags=["Metrics"])
async def receive_metrics(metrics: Metrics):
    """Receiver of metrics from sensors"""

    stored_metric = metrics_cache.get(metrics.metric_name)

    if stored_metric:
        stored_metric.set(metrics.data)
    else:
        new_metric = None

        match metrics.type:
            case "gauge":
                new_metric = Gauge(metrics.metric_name, metrics.description)
            case "summary":
                new_metric = Summary(metrics.metric_name, metrics.description)
            case "histogram":
                new_metric = Histogram(
                    metrics.metric_name, metrics.description
                )
            case "info":
                new_metric = Info(metrics.metric_name, metrics.description)
            case "enum":
                new_metric = Enum(metrics.metric_name, metrics.description)
            case _:
                raise HTTPException(400, f"{metrics.type} is not a valid type")

        metrics_cache[metrics.metric_name] = new_metric

    return {"detail": "Got your metrics! Thanks!"}

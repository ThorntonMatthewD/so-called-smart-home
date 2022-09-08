"""Exposes metrics to Prometheus"""
from typing import List
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
    data: float


@router.post("/receive_metrics", tags=["Metrics"])
async def receive_metrics(metrics: List[Metrics]):
    """Receiver of metrics from sensors"""

    for metric in metrics:
        stored_metric = metrics_cache.get(metric.metric_name)

        if stored_metric:
            stored_metric.set(metric.data)
        else:
            new_metric = None

            match metric.type:
                case "gauge":
                    new_metric = Gauge(
                        metric.metric_name, metric.description
                    )
                case "summary":
                    new_metric = Summary(
                        metric.metric_name, metric.description
                    )
                case "histogram":
                    new_metric = Histogram(
                        metric.metric_name, metric.description
                    )
                case "info":
                    new_metric = Info(metric.metric_name, metric.description)
                case "enum":
                    new_metric = Enum(metric.metric_name, metric.description)
                case _:
                    raise HTTPException(
                        400, f"{metric.type} is not a valid type"
                    )

            metrics_cache[metric.metric_name] = new_metric

    return {"detail": "Got your metrics! Thanks!"}

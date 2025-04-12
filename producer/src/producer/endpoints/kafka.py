import asyncio
import json
from datetime import datetime

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import JSONResponse
from aiokafka import AIOKafkaProducer

from src.producer.schemas import Message
from src.main import app, config

event_loop = asyncio.get_event_loop()


router = APIRouter()

@router.post(
    "/send",
    description="Send message to kafka",
)
async def send_kafka(message: Message, request: Request) -> None:
    message_to_produce = json.dumps(message.model_dump()).encode(encoding="utf-8")
    await request.app.kafka_producer.send(value=message_to_produce, topic=config.KAFKA_TOPIC)
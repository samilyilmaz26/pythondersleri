import asyncio
import json
import logging

import aio_pika

from repo.lookup_repository import LookupRepository
from repo.student_read_model_repository import StudentReadModelRepository

logger = logging.getLogger("events_consumer")

EXCHANGE_NAME = "domain.events"
QUEUE_NAME = "student-read-model-queue"
ROUTING_KEYS = [
    "student.*",
    "city.created",
    "city.updated",
    "city.deleted",
    "department.created",
    "department.updated",
    "department.deleted",
]


class EventsConsumer:
    """Listens to domain.events and keeps the read-model tables in sync.

    Runs as a background asyncio task started at app startup, so it never
    blocks request handling. Uses connect_robust so a dropped connection to
    RabbitMQ is retried automatically instead of killing the consumer.
    """

    def __init__(
        self,
        rabbitmq_url: str,
        read_model_repo: StudentReadModelRepository,
        lookup_repo: LookupRepository,
    ):
        self.rabbitmq_url = rabbitmq_url
        self.read_model_repo = read_model_repo
        self.lookup_repo = lookup_repo
        self._connection = None
        self._task = None

    async def start(self) -> None:
        self._task = asyncio.create_task(self._run())

    async def stop(self) -> None:
        if self._task is not None:
            self._task.cancel()
        if self._connection is not None:
            await self._connection.close()

    async def _run(self) -> None:
        self._connection = await aio_pika.connect_robust(self.rabbitmq_url)
        async with self._connection:
            channel = await self._connection.channel()
            await channel.set_qos(prefetch_count=10)
            exchange = await channel.declare_exchange(EXCHANGE_NAME, aio_pika.ExchangeType.TOPIC, durable=True)
            queue = await channel.declare_queue(QUEUE_NAME, durable=True)
            for routing_key in ROUTING_KEYS:
                await queue.bind(exchange, routing_key=routing_key)

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        self._handle(message.routing_key, json.loads(message.body))

    def _handle(self, routing_key: str, payload: dict) -> None:
        handlers = {
            "student.created": self._on_student_upsert,
            "student.updated": self._on_student_upsert,
            "student.deleted": self._on_student_deleted,
            "city.created": self._on_city_upsert,
            "city.updated": self._on_city_upsert,
            "city.deleted": self._on_city_deleted,
            "department.created": self._on_department_upsert,
            "department.updated": self._on_department_upsert,
            "department.deleted": self._on_department_deleted,
        }
        handler = handlers.get(routing_key)
        if handler is None:
            logger.warning("no handler registered for routing key %s", routing_key)
            return
        handler(payload)

    def _on_student_upsert(self, payload: dict) -> None:
        cityid = payload.get("cityid")
        departmentid = payload.get("departmentid")
        self.read_model_repo.upsert(
            id=payload["id"],
            name=payload.get("name", ""),
            surname=payload.get("surname"),
            street=payload.get("street"),
            number=payload.get("number"),
            cityid=cityid,
            departmentid=departmentid,
            cityname=self.lookup_repo.get_city_name(cityid),
            departmentname=self.lookup_repo.get_department_name(departmentid),
        )

    def _on_student_deleted(self, payload: dict) -> None:
        self.read_model_repo.delete(payload["id"])

    def _on_city_upsert(self, payload: dict) -> None:
        self.lookup_repo.upsert_city(payload["id"], payload["name"])
        self.read_model_repo.update_city_name(payload["id"], payload["name"])

    def _on_city_deleted(self, payload: dict) -> None:
        self.lookup_repo.delete_city(payload["id"])
        self.read_model_repo.clear_city(payload["id"])

    def _on_department_upsert(self, payload: dict) -> None:
        self.lookup_repo.upsert_department(payload["id"], payload["name"])
        self.read_model_repo.update_department_name(payload["id"], payload["name"])

    def _on_department_deleted(self, payload: dict) -> None:
        self.lookup_repo.delete_department(payload["id"])
        self.read_model_repo.clear_department(payload["id"])

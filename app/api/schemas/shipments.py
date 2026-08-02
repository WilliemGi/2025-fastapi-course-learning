from datetime import datetime
from random import randint

from pydantic import BaseModel, Field

from app.database.models import ShipmentStatus

description = ("Weight of the shipment in kilograms(kg)",)


def random_destination():
    return randint(11000, 11999)


class Shipment(BaseModel):
    content: str = Field(description="Contents of the shipment", max_length=30)
    weight: float = Field(
        description="Weight of the shipment in kilograms(kg)", le=25, ge=1
    )
    destination: int | None = Field(
        description="Destination Zipcode, If not provided will be sent off a random number",
        default_factory=random_destination,
    )
    status: ShipmentStatus


class BaseShipment(BaseModel):
    content: str
    weight: float = Field(le=25)
    destination: int


class ShipmentRead(BaseShipment):
    status: ShipmentStatus
    estimated_delivery: datetime


class Order(BaseModel):
    price: int
    title: str
    decription: str


# Test content :"That is the text Let's say we don't want our content to be top quality redwood with ideal fragrance"
class ShipmentCreate(BaseShipment):
    order: Order


class ShipmentUpdate(BaseModel):
    content: str | None = Field(default=None)
    weight: float | None = Field(default=None, le=25)
    destination: int | None = Field(default=None)
    status: ShipmentStatus | None = Field(default=None)
    estimated_delivery: datetime | None = Field(default=None)
    # 呼叫方完全沒有傳遞 status 或 estimated_delivery參數，Pydantic 不會拋出缺失必填欄位的錯誤 (ValidationError)，而是自動將該欄位的值指派給預設的None

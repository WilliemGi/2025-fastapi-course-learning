from enum import StrEnum
from random import randint

from pydantic import BaseModel, Field

description = ("Weight of the shipment in kilograms(kg)",)


def random_destination():
    return randint(11000, 11999)


class ShipmentStatus(StrEnum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"


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
    status: ShipmentStatus | None

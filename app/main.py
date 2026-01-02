from enum import StrEnum, auto
from typing import Any

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

from .schemas import (
    Shipment,
    ShipmentCreate,
    ShipmentRead,
    ShipmentStatus,
    ShipmentUpdate,
)

app = FastAPI(description="Scalar API documentation for the FastAPI application.")

shipments = {
    12701: {"weight": 0.6, "content": "glassware", "status": "placed"},
    12702: {"weight": 1.2, "content": "wooden table", "status": "in transit"},
    12703: {"weight": 2.5, "content": "books", "status": "delivered"},
    12704: {"weight": 0.3, "content": "electronics", "status": "placed"},
    12705: {"weight": 3.8, "content": "furniture set", "status": "in transit"},
    12706: {"weight": 1.1, "content": "clothing", "status": "delivered"},
    12707: {"weight": 0.9, "content": "ceramics", "status": "placed"},
}


@app.get("/shipment/latest")
def get_latest_shipment():
    id = max(shipments.keys())
    return shipments[id]


### Read a shipment by id
@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int):
    # Check for shipment with given id
    if not id:
        id = max(shipments.keys())
        return shipments[id]

    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id is not exist"
        )
    return shipments[id]


### Create a new shipment with content and weight
@app.post("/shipment")
def submit_shipment(shipment: ShipmentCreate) -> dict[str, Any]:
    # Create and assign shipment a new id
    new_id = max(shipments.keys()) + 1
    # Add to shipments dictionary

    shipments[new_id] = {
        **shipment.model_dump(),
        "status": "placed",
    }
    # Return id for later use
    return {"id": new_id}


### Update fields of a shipment
@app.put("/shipment")
def shipment_update(
    id: int, content: str, weight: float, status: str
) -> dict[str, Any]:
    shipments[id] = {
        "content": content,
        "weight": weight,
        "status": status,
    }
    return shipments[id]


@app.get("/shipment/{field}")
def get_shipment_field(field: str, id: int) -> dict[str, Any]:
    return {field: shipments[id][field]}


### Update fields of a shipment
@app.patch("/shipment", response_model=ShipmentRead)
def patch_shipment(id: int, body: ShipmentUpdate):
    # Update the provide fields
    shipments[id].update(body.model_dump(exclude_none=True))

    return shipments[id]


@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, Any]:
    shipments.pop(id)
    return {"detail": f"Shipment with id #{id} is deleted!"}


# Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
def scalar():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )

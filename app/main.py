from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import Any

import fastapi
from scalar_fastapi import get_scalar_api_reference

from app.database.models import Shipment, ShipmentStatus
from app.database.session import SessionDep, create_db_tables

from .database import Database
from .database_origin import save, shipments
from .schemas import (
    ShipmentCreate,
    ShipmentRead,
    ShipmentUpdate,
)


@asynccontextmanager
async def lifespan_handler(app: fastapi.FastAPI):
    create_db_tables()
    # Code to run on startup
    print("Server started...")
    yield
    print("...stoppped")


app = fastapi.FastAPI(lifespan=lifespan_handler)

# shipments = {
#     12701: {"weight": 0.6, "content": "glassware", "status": "placed"},
#     12702: {"weight": 1.2, "content": "wooden table", "status": "in transit"},
#     12703: {"weight": 2.5, "content": "books", "status": "delivered"},
#     12704: {"weight": 0.3, "content": "electronics", "status": "placed"},
#     12705: {"weight": 3.8, "content": "furniture set", "status": "in transit"},
#     12706: {"weight": 1.1, "content": "clothing", "status": "delivered"},
#     12707: {"weight": 0.9, "content": "ceramics", "status": "placed"},
# }

db = Database


@app.get("/shipment/latest")
def get_latest_shipment():
    id = max(shipments.keys())
    return shipments[id]


### Read a shipment by id
@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int, session: SessionDep):
    # Check for shipment with given id
    shipment = session.get(Shipment, id)

    if shipment is None:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="Given id is not exist",
        )
    return shipment


### Create a new shipment with content and weight
@app.post("/shipment")
def submit_shipment(shipment: ShipmentCreate, session: SessionDep) -> dict[str, Any]:
    # Create and assign shipment a new id
    new_shipment = Shipment(
        content=shipment.content,
        weight=shipment.weight,
        destination=shipment.destination,
        status=ShipmentStatus.placed,
        estimated_delivery=datetime.now() + timedelta(days=3),
    )
    session.add(new_shipment)
    session.commit()
    session.refresh(new_shipment)

    # Return id for later use
    return {"id": new_shipment.id}


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
# 部分更新 (Partial Update)，PATCH 請求
# 客戶端只需要發送想要修改的欄位，未發送的即為None，後端邏輯可以藉此判斷「那些欄位不需要被更新」
@app.patch("/shipment", response_model=ShipmentRead)
def patch_shipment(id: int, shipment_update: ShipmentUpdate, session: SessionDep):

    update = shipment_update.model_dump(exclude_none=True)
    # Update data with given fields

    # if the update is empty
    if not update:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="No data provided for update",
        )
    shipment = session.get(Shipment, id)
    shipment.sqlmodel_update(update)

    session.add(shipment)
    session.commit()
    session.refresh(shipment)

    return shipment


### Delete a shipment by id
@app.delete("/shipment")
def delete_shipment(id: int, session: SessionDep) -> dict[str, Any]:
    # Remove from datastore
    session.delete(session.get(Shipment, id))
    session.commit()
    return {"detail": f"Shipment with id #{id} is deleted!"}


# Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
def scalar():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )

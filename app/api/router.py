from datetime import datetime, timedelta
from typing import Any

from fastapi import APIRouter, HTTPException, status

from app.api.schemas import shipments
from app.api.schemas.shipments import ShipmentCreate, ShipmentUpdate
from app.database.models import Shipment, ShipmentStatus
from app.database.session import SessionDep

router = APIRouter()


### Read a shipment by id
@router.get("/shipment", response_model=Shipment)
async def get_shipment(id: int, session: SessionDep):
    # Check for shipment with given id
    shipment = await session.get(Shipment, id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id is not exist",
        )
    return shipment


### Create a new shipment with content and weight
@router.post("/shipment")
async def submit_shipment(
    shipment: ShipmentCreate, session: SessionDep
) -> dict[str, Any]:
    # Create and assign shipment a new id
    new_shipment = Shipment(
        content=shipment.content,
        weight=shipment.weight,
        destination=shipment.destination,
        status=ShipmentStatus.placed,
        estimated_delivery=datetime.now() + timedelta(days=3),
    )
    session.add(new_shipment)
    await session.commit()
    await session.refresh(new_shipment)

    # Return id for later use
    return {"id": new_shipment.id}


### Update fields of a shipment
# 部分更新 (Partial Update)，PATCH 請求
# 客戶端只需要發送想要修改的欄位，未發送的即為None，後端邏輯可以藉此判斷「那些欄位不需要被更新」
@router.patch("/shipment", response_model=Shipment)
async def patch_shipment(id: int, shipment_update: ShipmentUpdate, session: SessionDep):

    update = shipment_update.model_dump(exclude_none=True)
    # Update data with given fields

    # if the update is empty
    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided for update",
        )
    shipment = await session.get(Shipment, id)
    shipment.sqlmodel_update(update)

    session.add(shipment)
    await session.commit()
    await session.refresh(shipment)

    return shipment


### Delete a shipment by id
@router.delete("/shipment")
async def delete_shipment(id: int, session: SessionDep) -> dict[str, Any]:
    # Remove from datastore
    await session.delete(await session.get(Shipment, id))
    await session.commit()
    return {"detail": f"Shipment with id #{id} is deleted!"}


### Update fields of a shipment
@router.put("/shipment")
def shipment_update(
    id: int, content: str, weight: float, status: str
) -> dict[str, Any]:
    shipments[id] = {
        "content": content,
        "weight": weight,
        "status": status,
    }
    return shipments[id]


@router.get("/shipment/{field}")
def get_shipment_field(field: str, id: int) -> dict[str, Any]:
    return {field: shipments[id][field]}

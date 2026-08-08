from typing import Any

from fastapi import APIRouter, HTTPException, status

from app.database.models import Shipment

from ..dependencies import ServiceDep
from ..schemas.shipments import ShipmentCreate, ShipmentUpdate

router = APIRouter()


### Read a shipment by id
@router.get("/shipment", response_model=Shipment)
async def get_shipment(id: int, service: ServiceDep):
    # Check for shipment with given id
    shipment = await service.get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id is not exist",
        )
    return shipment


### Create a new shipment with content and weight
@router.post("/shipment")
async def submit_shipment(shipment: ShipmentCreate, service: ServiceDep) -> Shipment:
    # Create and assign shipment a new id
    return await service.add(shipment)


### Update fields of a shipment
# 部分更新 (Partial Update)，PATCH 請求
# 客戶端只需要發送想要修改的欄位，未發送的即為None，後端邏輯可以藉此判斷「那些欄位不需要被更新」
@router.patch("/shipment", response_model=Shipment)
async def patch_shipment(id: int, shipment_update: dict, service: ServiceDep):

    update = shipment_update.model_dump(exclude_none=True)
    # Update data with given fields

    # if the update is empty
    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided for update",
        )

    shipment = await service.update(id, update)

    return shipment


### Delete a shipment by id
@router.delete("/shipment")
async def delete_shipment(id: int, service: ServiceDep) -> dict[str, Any]:
    # Remove from datastore
    await service.delete(id)

    return {"detail": f"Shipment with id #{id} is deleted!"}
    return {"detail": f"Shipment with id #{id} is deleted!"}

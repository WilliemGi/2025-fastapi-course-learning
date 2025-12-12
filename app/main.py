from typing import Any

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()

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


@app.get("/shipment", status_code=status.HTTP_200_OK)
def get_shipment(id: int) -> dict[str, Any]:
    if not id:
        id = max(shipments.keys())
        return shipments[id]

    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id is not exist"
        )
    return shipments[id]


@app.post("/shipment")
def submit_shipment(data: dict[str, Any]) -> dict[str, Any]:
    content = data["content"]
    weight = data["weight"]
    if weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Maximum weigjht limit : 25kgs",
        )

    new_id = max(shipments.keys()) + 1

    shipments[new_id] = {
        "content": content,
        "weight": weight,
        "status": "placed",
    }
    return {"id": new_id}


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


@app.patch("/shipment")
def patch_shipment(id: int, body: dict[str, Any]):
    shipment = shipments[id]
    # Update the provide fields

    shipment.update(body)

    shipments[id] = shipment
    return shipment


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

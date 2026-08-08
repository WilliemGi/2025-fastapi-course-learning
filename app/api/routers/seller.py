from fastapi import APIRouter

from ..schemas.seller import SellerCreate

router = APIRouter(prefix="/seller")


# Register a seller
@router.post("/signup")
async def register_seller(seller: SellerCreate):
    pass

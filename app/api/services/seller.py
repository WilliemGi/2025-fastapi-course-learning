from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.seller import SellerCreate
from app.database.models import Seller


class Sellerservice:
    def __init__(self, session: AsyncSession):
    # Get database session to perform database operations
        self.session = session
        
    async def add(self, credentials: SellerCreate):
        seller = Seller(
            **credentials.model_dump(exclude=['password'])
        )        )
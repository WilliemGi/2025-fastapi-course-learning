from contextlib import asynccontextmanager

import fastapi
from scalar_fastapi import get_scalar_api_reference

from app.api.router import master_router
from app.database.session import create_db_tables


@asynccontextmanager
async def lifespan_handler(app: fastapi.FastAPI):
    await create_db_tables()
    # Code to run on startup
    print("Server started...")
    yield
    print("...stoppped")


app = fastapi.FastAPI(
    # Server start/stop listener
    lifespan=lifespan_handler
)

# shipments = {
#     12701: {"weight": 0.6, "content": "glassware", "status": "placed"},
#     12702: {"weight": 1.2, "content": "wooden table", "status": "in transit"},
#     12703: {"weight": 2.5, "content": "books", "status": "delivered"},
#     12704: {"weight": 0.3, "content": "electronics", "status": "placed"},
#     12705: {"weight": 3.8, "content": "furniture set", "status": "in transit"},
#     12706: {"weight": 1.1, "content": "clothing", "status": "delivered"},
#     12707: {"weight": 0.9, "content": "ceramics", "status": "placed"},
# }


app.include_router(master_router)


# Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
def scalar():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )

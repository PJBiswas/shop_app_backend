from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.api.v1 import auth, customers, installments, reports, products, purchase, dashboard
from app.core.scheduler import start_scheduler
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)
start_scheduler()
app = FastAPI(
    title="Installment Shop API",
    description="Manage customer registration, installment tracking, and admin reports",
    version="1.0.0"
)

# CORS setup (if frontend is hosted elsewhere)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route registrations
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(customers.router, prefix="/customers", tags=["Customers"])
app.include_router(installments.router, prefix="/installments", tags=["Installments"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(reports.router, prefix="/reports", tags=["Reports"])
app.include_router(purchase.router, prefix="/purchase", tags=["Purchase"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Installment Shop API",
        version="1.0.0",
        description="API for handling installment-based purchases",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

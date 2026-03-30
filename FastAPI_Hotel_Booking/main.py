from fastapi import FastAPI
from routers import rooms, customers, bookings

app = FastAPI(
    title="Hotel Room Booking API",
    description="A complete hotel booking backend built with FastAPI",
    version="1.0.0",
)

app.include_router(rooms.router)
app.include_router(customers.router)
app.include_router(bookings.router)

@app.get("/", tags=["Home"], summary="Home Route")
def home():
    return {
        "message": "Welcome to the Hotel Room Booking API",
        "docs": "http://127.0.0.1:8000/docs",
        "version": "1.0.0",
        "endpoints": {
            "rooms": "/rooms",
            "customers": "/customers",
            "bookings": "/bookings",
        },
    }
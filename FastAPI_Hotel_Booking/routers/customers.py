from fastapi import APIRouter, HTTPException
from database import customers_db, customer_counter
from models import CustomerCreate, CustomerUpdate
from helpers import find_customer

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.post("/", status_code=201, summary="Register Customer")
def create_customer(customer: CustomerCreate):
    for existing in customers_db.values():
        if existing["email"] == customer.email.lower().strip():
            raise HTTPException(status_code=400, detail="Email already registered")
    cid = customer_counter["value"]
    customer_counter["value"] += 1
    new_customer = {"customer_id": cid, **customer.model_dump()}
    customers_db[cid] = new_customer
    return {"message": "Customer registered successfully", "customer": new_customer}

@router.get("/", summary="Get All Customers")
def get_all_customers():
    return {"total_customers": len(customers_db), "customers": list(customers_db.values())}

@router.get("/{customer_id}", summary="Get Customer by ID")
def get_customer(customer_id: int):
    customer = find_customer(customers_db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")
    return customer

@router.put("/{customer_id}", summary="Update Customer")
def update_customer(customer_id: int, updates: CustomerUpdate):
    customer = find_customer(customers_db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")
    update_data = updates.model_dump(exclude_none=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided to update")
    customer.update(update_data)
    return {"message": "Customer updated successfully", "customer": customer}
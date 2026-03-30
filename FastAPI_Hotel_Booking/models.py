from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import date
from enum import Enum

class RoomType(str, Enum):
    single = "single"
    double = "double"
    suite = "suite"
    deluxe = "deluxe"

class BookingStatus(str, Enum):
    confirmed = "confirmed"
    checked_in = "checked_in"
    checked_out = "checked_out"
    cancelled = "cancelled"

class RoomSortField(str, Enum):
    price_per_night = "price_per_night"
    rating = "rating"
    capacity = "capacity"

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"

class RoomCreate(BaseModel):
    room_number: str
    type: RoomType
    price_per_night: float
    capacity: int
    amenities: List[str] = []
    rating: float = 0.0

    @field_validator("price_per_night")
    @classmethod
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Price must be greater than 0")
        return round(v, 2)

    @field_validator("capacity")
    @classmethod
    def capacity_must_be_valid(cls, v):
        if v < 1 or v > 10:
            raise ValueError("Capacity must be between 1 and 10")
        return v

    @field_validator("rating")
    @classmethod
    def rating_range(cls, v):
        if v < 0 or v > 5:
            raise ValueError("Rating must be between 0.0 and 5.0")
        return round(v, 1)

class RoomUpdate(BaseModel):
    price_per_night: Optional[float] = None
    amenities: Optional[List[str]] = None
    is_available: Optional[bool] = None
    rating: Optional[float] = None

class CustomerCreate(BaseModel):
    name: str
    email: str
    phone: str
    id_proof: str

    @field_validator("phone")
    @classmethod
    def phone_must_be_10_digits(cls, v):
        if not v.isdigit() or len(v) != 10:
            raise ValueError("Phone must be a 10-digit number")
        return v

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()

    @field_validator("email")
    @classmethod
    def email_must_have_at(cls, v):
        if "@" not in v or "." not in v:
            raise ValueError("Enter a valid email address")
        return v.lower().strip()

class CustomerUpdate(BaseModel):
    phone: Optional[str] = None
    email: Optional[str] = None

class BookingCreate(BaseModel):
    customer_id: int
    room_id: int
    check_in_date: date
    check_out_date: date
    guests: int

    @field_validator("check_out_date")
    @classmethod
    def checkout_after_checkin(cls, v, info):
        if "check_in_date" in info.data and v <= info.data["check_in_date"]:
            raise ValueError("Check-out date must be after check-in date")
        return v

    @field_validator("guests")
    @classmethod
    def guests_positive(cls, v):
        if v < 1:
            raise ValueError("At least 1 guest is required")
        return v
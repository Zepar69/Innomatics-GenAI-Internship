from fastapi import APIRouter, HTTPException
from datetime import date
from database import bookings_db, rooms_db, customers_db, booking_counter
from models import BookingCreate, BookingStatus
from helpers import find_booking, find_room, find_customer, calculate_total_price, is_room_available, format_invoice

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.get("/", summary="Get All Bookings")
def get_all_bookings():
    return {"total_bookings": len(bookings_db), "bookings": list(bookings_db.values())}

@router.post("/", status_code=201, summary="Create Booking")
def create_booking(booking: BookingCreate):
    customer = find_customer(customers_db, booking.customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer {booking.customer_id} not found")

    room = find_room(rooms_db, booking.room_id)
    if not room:
        raise HTTPException(status_code=404, detail=f"Room {booking.room_id} not found")

    if not is_room_available(room):
        raise HTTPException(status_code=400, detail=f"Room {room['room_number']} is not available")

    if booking.guests > room["capacity"]:
        raise HTTPException(status_code=400, detail=f"Room capacity is {room['capacity']}, requested {booking.guests} guests")

    total_price = calculate_total_price(room["price_per_night"], booking.check_in_date, booking.check_out_date)

    bid = booking_counter["value"]
    booking_counter["value"] += 1
    new_booking = {
        "booking_id": bid,
        "customer_id": booking.customer_id,
        "customer_name": customer["name"],
        "room_id": booking.room_id,
        "room_number": room["room_number"],
        "room_type": room["type"],
        "check_in_date": str(booking.check_in_date),
        "check_out_date": str(booking.check_out_date),
        "guests": booking.guests,
        "total_price": total_price,
        "status": BookingStatus.confirmed,
        "actual_checkin": None,
        "actual_checkout": None,
    }
    bookings_db[bid] = new_booking
    rooms_db[booking.room_id]["is_available"] = False
    return {"message": "Booking confirmed!", "booking": new_booking}

@router.get("/{booking_id}", summary="Get Booking by ID")
def get_booking(booking_id: int):
    booking = find_booking(bookings_db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail=f"Booking {booking_id} not found")
    return booking

@router.delete("/{booking_id}", summary="Cancel Booking")
def cancel_booking(booking_id: int):
    booking = find_booking(bookings_db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail=f"Booking {booking_id} not found")
    if booking["status"] == BookingStatus.checked_in:
        raise HTTPException(status_code=400, detail="Cannot cancel — guest is already checked in")
    if booking["status"] == BookingStatus.checked_out:
        raise HTTPException(status_code=400, detail="Cannot cancel — booking is already completed")
    if booking["status"] == BookingStatus.cancelled:
        raise HTTPException(status_code=400, detail="Booking is already cancelled")
    rooms_db[booking["room_id"]]["is_available"] = True
    booking["status"] = BookingStatus.cancelled
    return {"message": f"Booking {booking_id} cancelled", "booking": booking}

@router.post("/{booking_id}/checkin", summary="Check-In Guest")
def check_in(booking_id: int):
    booking = find_booking(bookings_db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail=f"Booking {booking_id} not found")
    if booking["status"] != BookingStatus.confirmed:
        raise HTTPException(status_code=400, detail=f"Cannot check-in. Current status: {booking['status']}")
    booking["status"] = BookingStatus.checked_in
    booking["actual_checkin"] = str(date.today())
    return {"message": f"Guest checked in to Room {booking['room_number']}", "booking": booking}

@router.post("/{booking_id}/checkout", summary="Check-Out Guest")
def check_out(booking_id: int):
    booking = find_booking(bookings_db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail=f"Booking {booking_id} not found")
    if booking["status"] != BookingStatus.checked_in:
        raise HTTPException(status_code=400, detail=f"Cannot check-out. Current status: {booking['status']}")
    booking["status"] = BookingStatus.checked_out
    booking["actual_checkout"] = str(date.today())
    rooms_db[booking["room_id"]]["is_available"] = True
    room = find_room(rooms_db, booking["room_id"])
    customer = find_customer(customers_db, booking["customer_id"])
    invoice = format_invoice(booking, room, customer)
    return {"message": "Check-out complete!", "invoice": invoice}
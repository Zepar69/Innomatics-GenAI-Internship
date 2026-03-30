from datetime import date
from typing import Optional, List

def find_room(rooms_db, room_id):
    return rooms_db.get(room_id)

def find_customer(customers_db, customer_id):
    return customers_db.get(customer_id)

def find_booking(bookings_db, booking_id):
    return bookings_db.get(booking_id)

def calculate_total_price(price_per_night, check_in, check_out):
    nights = (check_out - check_in).days
    return round(price_per_night * nights, 2)

def is_room_available(room):
    return room.get("is_available", False)

def filter_rooms(rooms, room_type=None, min_price=None, max_price=None, min_capacity=None, keyword=None):
    results = rooms

    if room_type is not None:
        results = [r for r in results if r["type"] == room_type]

    if min_price is not None:
        results = [r for r in results if r["price_per_night"] >= min_price]

    if max_price is not None:
        results = [r for r in results if r["price_per_night"] <= max_price]

    if min_capacity is not None:
        results = [r for r in results if r["capacity"] >= min_capacity]

    if keyword is not None:
        kw = keyword.lower()
        results = [
            r for r in results
            if kw in r["room_number"].lower()
            or kw in r["type"].lower()
            or any(kw in amenity.lower() for amenity in r["amenities"])
        ]

    return results

def sort_rooms(rooms, sort_by, order):
    return sorted(rooms, key=lambda r: r[sort_by], reverse=(order == "desc"))

def paginate(items, page, page_size):
    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size
    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": max(1, -(-total // page_size)),
        "results": items[start:end],
    }

def format_invoice(booking, room, customer):
    check_in = date.fromisoformat(str(booking["check_in_date"]))
    check_out = date.fromisoformat(str(booking["check_out_date"]))
    nights = (check_out - check_in).days
    return {
        "invoice_for": customer["name"],
        "room_number": room["room_number"],
        "room_type": room["type"],
        "nights_stayed": nights,
        "price_per_night": room["price_per_night"],
        "total_amount": booking["total_price"],
        "status": booking["status"],
        "check_in": str(booking["check_in_date"]),
        "check_out": str(booking["check_out_date"]),
        "actual_checkout": booking.get("actual_checkout", "N/A"),
    }
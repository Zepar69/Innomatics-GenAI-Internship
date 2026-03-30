from datetime import date

rooms_db = {
    1: {
        "room_id": 1,
        "room_number": "101",
        "type": "single",
        "price_per_night": 1500.0,
        "capacity": 1,
        "amenities": ["WiFi", "AC"],
        "is_available": True,
        "rating": 4.2,
    },
    2: {
        "room_id": 2,
        "room_number": "102",
        "type": "double",
        "price_per_night": 2500.0,
        "capacity": 2,
        "amenities": ["WiFi", "AC", "TV"],
        "is_available": True,
        "rating": 4.5,
    },
    3: {
        "room_id": 3,
        "room_number": "201",
        "type": "suite",
        "price_per_night": 5000.0,
        "capacity": 4,
        "amenities": ["WiFi", "AC", "TV", "Jacuzzi"],
        "is_available": True,
        "rating": 4.8,
    },
    4: {
        "room_id": 4,
        "room_number": "202",
        "type": "double",
        "price_per_night": 2800.0,
        "capacity": 2,
        "amenities": ["WiFi", "AC"],
        "is_available": True,
        "rating": 4.0,
    },
    5: {
        "room_id": 5,
        "room_number": "301",
        "type": "deluxe",
        "price_per_night": 7500.0,
        "capacity": 3,
        "amenities": ["WiFi", "AC", "TV", "Mini Bar", "Sea View"],
        "is_available": True,
        "rating": 4.9,
    },
}

customers_db = {
    1: {
        "customer_id": 1,
        "name": "John Sekiro",
        "email": "sek@gmail.com",
        "phone": "9876543210",
        "id_proof": "AADHAR-1234",
    },
    2: {
        "customer_id": 2,
        "name": "Elizabeth Danafor",
        "email": "liz@email.com",
        "phone": "9123456789",
        "id_proof": "PAN-ABCDE1234F",
    },
}

bookings_db = {}

room_counter = {"value": 6}
customer_counter = {"value": 3}
booking_counter = {"value": 1}
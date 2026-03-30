# 🏨 Hotel Room Booking API

### 🚀 Complete FastAPI Backend for Hotel Management

---

## 📌 Overview

Hotel Room Booking API is a fully-featured backend system built using **FastAPI**, designed to simulate a real-world hotel booking platform.

This project goes beyond basic CRUD — it incorporates:

* Room availability and management
* Customer registration system
* Multi-step booking lifecycle
* Advanced filtering, search, sorting, and pagination

It's structured to reflect how production-grade backend systems are built.

---

## ⚙️ Tech Stack

* **Backend Framework:** FastAPI
* **Language:** Python
* **Validation:** Pydantic
* **Server:** Uvicorn

---

## 🧠 Core Features

### 🛏️ Room Management

* Create, update, delete rooms
* Filter by type, price, capacity
* Search by keyword or amenity
* Sort and paginate rooms
* Smart browsing with combined filters

---

### 👤 Customer System

* Register new customers
* Duplicate email detection
* Update customer contact info
* View all customers

---

### 📋 Booking Workflow

* Create bookings with full validation:
  * Customer must exist
  * Room must be available
  * Guest count vs room capacity check
  * Automatic total price calculation
* Check-in and check-out lifecycle
* Cancel bookings
* Auto-generated invoice on checkout

---

### 🔍 Advanced API Features

* Combined filtering + sorting + pagination
* Clean validation using Pydantic
* Error handling using HTTPException
* Query parameter handling with optional filters

---

## 📂 Project Structure
```
hotel_booking/
├── main.py
├── models.py
├── database.py
├── helpers.py
├── requirements.txt
├── README.md
├── screenshots/
└── routers/
    ├── __init__.py
    ├── rooms.py
    ├── customers.py
    └── bookings.py
```

---

## 🚀 Getting Started

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Run Server
```bash
uvicorn main:app --reload
```

### 3️⃣ Open API Docs

* Swagger UI: http://127.0.0.1:8000/docs
* ReDoc: http://127.0.0.1:8000/redoc

---

## 📡 API Endpoints

### 🏠 Basic

* `GET /` → Welcome message

---

### 🛏️ Rooms

* `GET /rooms` → Get all rooms
* `GET /rooms/{room_id}` → Get room by ID
* `GET /rooms/available` → Get available rooms
* `POST /rooms` → Create room
* `PUT /rooms/{room_id}` → Update room
* `DELETE /rooms/{room_id}` → Delete room

---

### 🔎 Advanced Room APIs

* `GET /rooms/search` → Keyword + filter search
* `GET /rooms/sorted` → Sort by price, rating, capacity
* `GET /rooms/paginated` → Paginated results
* `GET /rooms/browse` → Combined search + sort + paginate

---

### 👥 Customers

* `GET /customers` → Get all customers
* `GET /customers/{customer_id}` → Get customer by ID
* `POST /customers` → Register customer
* `PUT /customers/{customer_id}` → Update customer

---

### 📋 Bookings

* `GET /bookings` → Get all bookings
* `GET /bookings/{booking_id}` → Get booking by ID
* `POST /bookings` → Create booking
* `DELETE /bookings/{booking_id}` → Cancel booking
* `POST /bookings/{booking_id}/checkin` → Check-in guest
* `POST /bookings/{booking_id}/checkout` → Check-out + invoice

---

## 💡 Business Logic Highlights

### 💰 Pricing Engine

* Total price = price per night × number of nights
* Automatic calculation on booking creation

### 🔐 Validation

* Phone must be exactly 10 digits
* Check-out date must be after check-in date
* Guest count cannot exceed room capacity
* Room must be available before booking
* Duplicate emails rejected on registration

### 🔄 Booking Lifecycle
```
POST /bookings          →    POST /bookings/{id}/checkin    →    POST /bookings/{id}/checkout
   (confirmed)                    (checked_in)                      (checked_out + invoice)
        |
   DELETE /bookings/{id}
      (cancelled)
```

---

## 🧪 Sample Request

### Create Booking
```json
POST /bookings

{
  "customer_id": 1,
  "room_id": 2,
  "check_in_date": "2026-04-01",
  "check_out_date": "2026-04-05",
  "guests": 2
}
```

---

## 📈 Future Improvements

* Database integration (PostgreSQL / MongoDB)
* JWT Authentication & Role-based access
* Payment gateway integration
* Admin dashboard
* Real-time room availability tracking
* Deployment with Docker & CI/CD

---

## 🙌 Final Note

Built with a focus on clarity, scalability, and real-world applicability.
A solid foundation for any production-grade backend system.

---
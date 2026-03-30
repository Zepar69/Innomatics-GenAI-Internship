from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from database import rooms_db, room_counter
from models import RoomCreate, RoomUpdate, RoomType, RoomSortField, SortOrder
from helpers import find_room, filter_rooms, sort_rooms, paginate

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.get("/", summary="Get All Rooms")
def get_all_rooms():
    return {"total_rooms": len(rooms_db), "rooms": list(rooms_db.values())}

@router.get("/available", summary="Get Available Rooms")
def get_available_rooms():
    available = [r for r in rooms_db.values() if r["is_available"]]
    return {"available_count": len(available), "rooms": available}

@router.get("/search", summary="Search Rooms")
def search_rooms(
    keyword: Optional[str] = Query(None),
    type: Optional[RoomType] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    min_capacity: Optional[int] = Query(None, ge=1),
):
    results = filter_rooms(
        rooms=list(rooms_db.values()),
        room_type=type.value if type else None,
        min_price=min_price,
        max_price=max_price,
        min_capacity=min_capacity,
        keyword=keyword,
    )
    return {"count": len(results), "results": results}

@router.get("/sorted", summary="Get Sorted Rooms")
def get_sorted_rooms(
    sort_by: RoomSortField = Query(RoomSortField.price_per_night),
    order: SortOrder = Query(SortOrder.asc),
):
    sorted_rooms = sort_rooms(list(rooms_db.values()), sort_by.value, order.value)
    return {"sort_by": sort_by, "order": order, "rooms": sorted_rooms}

@router.get("/paginated", summary="Get Paginated Rooms")
def get_paginated_rooms(
    page: int = Query(1, ge=1),
    page_size: int = Query(3, ge=1, le=10),
):
    return paginate(list(rooms_db.values()), page, page_size)

@router.get("/browse", summary="Combined Browse")
def browse_rooms(
    keyword: Optional[str] = Query(None),
    type: Optional[RoomType] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    min_capacity: Optional[int] = Query(None, ge=1),
    available_only: bool = Query(False),
    sort_by: RoomSortField = Query(RoomSortField.price_per_night),
    order: SortOrder = Query(SortOrder.asc),
    page: int = Query(1, ge=1),
    page_size: int = Query(3, ge=1, le=10),
):
    rooms = list(rooms_db.values())

    if available_only:
        rooms = [r for r in rooms if r["is_available"]]

    rooms = filter_rooms(
        rooms=rooms,
        room_type=type.value if type else None,
        min_price=min_price,
        max_price=max_price,
        min_capacity=min_capacity,
        keyword=keyword,
    )

    rooms = sort_rooms(rooms, sort_by.value, order.value)
    result = paginate(rooms, page, page_size)
    result["filters_applied"] = {
        "keyword": keyword,
        "type": type,
        "min_price": min_price,
        "max_price": max_price,
        "min_capacity": min_capacity,
        "available_only": available_only,
    }
    result["sort"] = {"sort_by": sort_by, "order": order}
    return result

@router.get("/{room_id}", summary="Get Room by ID")
def get_room(room_id: int):
    room = find_room(rooms_db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail=f"Room {room_id} not found")
    return room

@router.post("/", status_code=201, summary="Create Room")
def create_room(room: RoomCreate):
    room_id = room_counter["value"]
    room_counter["value"] += 1
    new_room = {"room_id": room_id, "is_available": True, **room.model_dump()}
    rooms_db[room_id] = new_room
    return {"message": "Room created successfully", "room": new_room}

@router.put("/{room_id}", summary="Update Room")
def update_room(room_id: int, updates: RoomUpdate):
    room = find_room(rooms_db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail=f"Room {room_id} not found")
    update_data = updates.model_dump(exclude_none=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided to update")
    room.update(update_data)
    return {"message": "Room updated successfully", "room": room}

@router.delete("/{room_id}", summary="Delete Room")
def delete_room(room_id: int):
    room = find_room(rooms_db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail=f"Room {room_id} not found")
    del rooms_db[room_id]
    return {"message": f"Room {room_id} deleted successfully"}
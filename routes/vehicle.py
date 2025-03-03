from fastapi import APIRouter, HTTPException, Query, Request, status, Depends
from typing import Annotated
from models.vehicleType import vehicleBase, VehicleCreate, VehiclePublic, VehicleUpdate
from pymongo.collection import Collection
from pymongo import ReturnDocument
import logging
from utils.utils import validate_object_id
from schemas.vehicleType import vehicle_entity_from_db, vehicle_entities_from_db

ERROR_DETAIL = "Some error occurred: {e}"
NOT_FOUND = "Not found"

async def get_vehicle_collection(request: Request) -> Collection:
    """Returns the vehicle collection from MongoDB"""
    return request.app.database["vehicle"]

VehicleCollection = Annotated[Collection, Depends(get_vehicle_collection)]
logger = logging.getLogger("app_logger")

router = APIRouter()

@router.post("/", 
    response_description="Registers a new Vehicle", 
    status_code=status.HTTP_201_CREATED, response_model=VehiclePublic)
async def create_vehicle(vehicle_collection: VehicleCollection, vehicle: VehicleCreate):
    try:
        vehicle_data = vehicle.model_dump()
        result = vehicle_collection.insert_one(vehicle_data)
        
        if (created := vehicle_collection.find_one({"_id": result.inserted_id})) is None:
            logger.error("Failed to create Vehicle")
            raise HTTPException(500, "Failed to create Vehicle")
            
        logger.info(f"Vehicle created with ID: {result.inserted_id}")
        return vehicle_entity_from_db(created)
    except Exception as e:
        logger.exception("Error creating vehicle")
        raise HTTPException(status_code=500, detail=ERROR_DETAIL.format(e=e))

@router.get("/", 
    response_description="Retrieves Vehicles", 
    response_model=list[VehiclePublic])
async def read_vehicles(
    vehicle_collection: VehicleCollection,
    page: Annotated[int, Query(ge=1, description="Pagination offset starting at 1")] = 1,
    limit: Annotated[int, Query(le=100, ge=1, description="Items per page (1-100)")] = 100
):
    try:
        cursor = vehicle_collection.find().skip((page - 1) * limit).limit(limit)
        vehicles = vehicle_entities_from_db(cursor)
        logger.info(f"Retrieved {len(vehicles)} vehicles")
        return vehicles
    except Exception as e:
        logger.exception("Error retrieving vehicles")
        raise HTTPException(status_code=500, detail=ERROR_DETAIL.format(e=e))

@router.get("/count", response_description="Get total Vehicle count")
async def read_vehicle_count(vehicle_collection: VehicleCollection):
    try:
        count = vehicle_collection.count_documents({})
        logger.info(f"Total vehicle count: {count}")
        return {"count": count}
    except Exception as e:
        logger.exception("Error getting vehicle count")
        raise HTTPException(500, detail=ERROR_DETAIL.format(e=e))

@router.get("/{id}",
    response_description="Retrieves Individual Vehicle by ID", 
    response_model=VehiclePublic)
async def read_vehicle(
    vehicle_collection: VehicleCollection, 
    id: str = Depends(validate_object_id)
):
    try:
        if (vehicle := vehicle_collection.find_one({"_id": id})) is None:
            logger.warning(f"Vehicle with ID {id} not found")
            raise HTTPException(404, detail=NOT_FOUND)
        logger.info(f"Retrieved vehicle with ID: {id}")
        return vehicle_entity_from_db(vehicle)
    except Exception as e:
        logger.exception("Error retrieving vehicle")
        raise HTTPException(status_code=500, detail=ERROR_DETAIL.format(e=e))

@router.patch("/{id}",
    response_description="Partially updates a Vehicle", 
    response_model=VehiclePublic)
async def update_vehicle(
    vehicle_collection: VehicleCollection, 
    vehicle: VehicleUpdate,
    id: str = Depends(validate_object_id)
):
    try:
        update_data = vehicle.model_dump(exclude_unset=True)
        
        updated = vehicle_collection.find_one_and_update(
            {"_id": id},
            {"$set": update_data},
            return_document=ReturnDocument.AFTER
        )
        
        if not updated:
            logger.warning(f"Vehicle with ID {id} not found for update")
            raise HTTPException(404, detail=NOT_FOUND)
            
        logger.info(f"Updated vehicle with ID: {id}")
        return vehicle_entity_from_db(updated)
    except Exception as e:
        logger.exception("Error updating vehicle")
        raise HTTPException(status_code=500, detail=ERROR_DETAIL.format(e=e))

@router.put("/{id}", 
    response_description="Fully update a Vehicle", 
    response_model=VehiclePublic)
async def fully_update_vehicle(
    vehicle_collection: VehicleCollection, 
    vehicle: vehicleBase,
    id: str = Depends(validate_object_id)
):
    try:
        update_data = vehicle.model_dump()
        
        updated = vehicle_collection.find_one_and_update(
            {"_id": id},
            {"$set": update_data},
            return_document=ReturnDocument.AFTER
        )
        
        if not updated:
            logger.warning(f"Vehicle with ID {id} not found for full update")
            raise HTTPException(404, detail=NOT_FOUND)
            
        logger.info(f"Fully updated vehicle with ID: {id}")
        return vehicle_entity_from_db(updated)
    except Exception as e:
        logger.exception("Error fully updating vehicle")
        raise HTTPException(status_code=500, detail=ERROR_DETAIL.format(e=e))

@router.delete("/{id}",
    response_description="Deletes a Vehicle")
async def delete_vehicle(
    vehicle_collection: VehicleCollection, 
    id: str = Depends(validate_object_id)
):
    try:
        result = vehicle_collection.delete_one({"_id": id})
        
        if result.deleted_count == 0:
            logger.warning(f"Vehicle with ID {id} not found for deletion")
            raise HTTPException(404, detail=NOT_FOUND)
            
        logger.info(f"Deleted vehicle with ID: {id}")
        return {"status": "success", "message": "Vehicle deleted successfully"}
    except Exception as e:
        logger.exception("Error deleting vehicle")
        raise HTTPException(status_code=500, detail=ERROR_DETAIL.format(e=e))